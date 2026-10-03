#!/usr/bin/env python3
"""Archive everything Ryadh has written into src/content/writing/.

Sources
  * ClickHouse blog  (author listing pages + explicitly included posts)
  * Medium           (RSS feed first, article page as fallback)
  * ryadh.net/blog   (old Jekyll blog; Markdown source pulled from GitHub)

For each article: extract the main content, convert it to Markdown, download
images to public/writing/<slug>/ and write src/content/writing/<yyyy>-<slug>.md.

Idempotent: a content hash is stored in the frontmatter. Unchanged posts are
skipped, changed posts are rewritten (a hand-edited `summary` or `tags` is kept).

Usage
  pip install -r scripts/requirements.txt
  python scripts/archive.py              # archive everything
  python scripts/archive.py --only agent # only URLs containing "agent"
  python scripts/archive.py --debug      # print page-structure diagnostics
  python scripts/archive.py --playwright # force a headless browser for fetches
"""
from __future__ import annotations

import argparse
import hashlib
import html as htmlmod
import json
import math
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "src" / "content" / "writing"
IMAGE_DIR = ROOT / "public" / "writing"

AUTHOR_SLUG = "ryadh-dahimene"
AUTHOR_NAME = "Ryadh Dahimene"

CLICKHOUSE_LISTINGS = [
    "https://clickhouse.com/blog?author=ryadh-dahimene",
    "https://clickhouse.com/blog?author=ryadh-dahimene&page=2",
    "https://clickhouse.com/authors/ryadh-dahimene",
]
CLICKHOUSE_EXPLICIT = [
    "https://clickhouse.com/blog/cost-predictable-logging-with-clickhouse-vs-datadog-elastic-stack",
]
CLICKHOUSE_EXPECTED = 16  # what the author page said when this script was written

MEDIUM_URLS = [
    "https://medium.com/@ryado/the-engineering-minded-product-manager-80f974dc8801",
]
MEDIUM_FEED = "https://medium.com/feed/@ryado"

RYADH_BLOG = "https://www.ryadh.net/blog/"
RYADH_BLOG_RAW = "https://raw.githubusercontent.com/Ryado/blog/gh-pages"
RYADH_BLOG_API = "https://api.github.com/repos/Ryado/blog/contents/_posts?ref=gh-pages"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0 Safari/537.36"
)
WORDS_PER_MINUTE = 230

DEBUG = False
FORCE_PLAYWRIGHT = False


def log(*a):
    print(*a, flush=True)


def debug(*a):
    if DEBUG:
        print("   [debug]", *a, flush=True)


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

_browser = None


def _playwright_get(url: str) -> str:
    global _browser
    from playwright.sync_api import sync_playwright  # optional dependency

    if _browser is None:
        pw = sync_playwright().start()
        _browser = pw.chromium.launch()
    page = _browser.new_page(user_agent=UA)
    try:
        page.goto(url, wait_until="networkidle", timeout=60_000)
        return page.content()
    finally:
        page.close()


def fetch(url: str, *, binary: bool = False, browser_ok: bool = True, retries: int = 3):
    """GET a URL with retries. Falls back to Playwright for HTML when blocked."""
    if FORCE_PLAYWRIGHT and not binary and browser_ok:
        return _playwright_get(url)
    last = None
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=45)
            if r.status_code == 200:
                return r.content if binary else r.text
            last = f"HTTP {r.status_code}"
            if r.status_code in (401, 403, 404, 410):
                break
        except requests.RequestException as e:
            last = str(e)
        time.sleep(2 ** attempt)
    if not binary and browser_ok:
        try:
            debug(f"falling back to Playwright for {url} ({last})")
            return _playwright_get(url)
        except Exception as e:  # noqa: BLE001
            last = f"{last}; playwright: {e}"
    raise RuntimeError(f"fetch failed for {url}: {last}")


# --------------------------------------------------------------------------- #
# Article model
# --------------------------------------------------------------------------- #


@dataclass
class Article:
    url: str
    source: str  # clickhouse | medium | ryadh.net
    slug: str
    title: str = ""
    date: str = ""  # YYYY-MM-DD
    coauthors: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    body: str = ""  # Markdown
    republished_from: str = ""
    lang: str = "en"


# --------------------------------------------------------------------------- #
# Generic helpers
# --------------------------------------------------------------------------- #


def norm_date(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    for parse in (
        lambda v: datetime.fromisoformat(v.replace("Z", "+00:00")),
        parsedate_to_datetime,
        lambda v: datetime.strptime(v, "%B %d, %Y"),
        lambda v: datetime.strptime(v, "%b %d, %Y"),
        lambda v: datetime.strptime(v, "%d %B %Y"),
        lambda v: datetime.strptime(v, "%d %b %Y"),
        lambda v: datetime.strptime(v, "%b %d %Y"),
    ):
        try:
            return parse(value).strftime("%Y-%m-%d")
        except Exception:  # noqa: BLE001
            continue
    return ""


DATE_TEXT_RE = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? \d{4}\b"
)


def first_sentence(text: str, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    if len(s) > limit:
        s = s[: limit - 1].rsplit(" ", 1)[0] + "…"
    return s


def markdown_to_text(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"^\s*(#+|>|\*|-|\d+\.)\s*", "", md, flags=re.M)
    md = re.sub(r"[*_`|]", "", md)
    return re.sub(r"\s+", " ", md).strip()


def reading_time(md: str) -> int:
    words = len(re.findall(r"\w+", markdown_to_text(md)))
    code_lines = sum(b.count("\n") for b in re.findall(r"```.*?```", md, flags=re.S))
    return max(1, math.ceil((words + code_lines * 3) / WORDS_PER_MINUTE))


def detect_lang(text: str) -> str:
    words = re.findall(r"[a-zà-ÿ’']+", text.lower())
    fr = sum(w in {"le", "la", "les", "des", "est", "une", "et", "du", "pour", "que", "dans"} for w in words)
    en = sum(w in {"the", "and", "is", "of", "to", "a", "in", "for", "that", "with"} for w in words)
    return "fr" if fr > en else "en"


def titlecase_slug(s: str) -> str:
    return " ".join(w.capitalize() for w in s.split("-") if w)


def is_me(name: str) -> bool:
    n = name.lower()
    return "dahimene" in n or AUTHOR_SLUG in n


def dedupe(seq):
    seen, out = set(), []
    for x in seq:
        k = x.lower() if isinstance(x, str) else x
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


# --------------------------------------------------------------------------- #
# HTML -> Markdown
# --------------------------------------------------------------------------- #

LANG_RE = re.compile(r"(?:language|lang|highlight-source|hljs)-([A-Za-z0-9_+#.-]+)")
LANG_ALIASES = {"sh": "bash", "shell": "bash", "console": "bash", "yml": "yaml", "js": "javascript",
                "ts": "typescript", "py": "python", "text": "", "plaintext": "", "none": ""}


def code_language(pre: Tag) -> str:
    nodes = [pre] + pre.find_all(["code", "div", "span"], limit=3) + [p for p in pre.parents][:3]
    for node in nodes:
        if not isinstance(node, Tag):
            continue
        for attr in ("data-language", "data-lang", "lang"):
            if node.get(attr):
                v = node[attr].lower()
                return LANG_ALIASES.get(v, v)
        for cls in node.get("class", []) or []:
            m = LANG_RE.match(cls)
            if m:
                v = m.group(1).lower()
                return LANG_ALIASES.get(v, v)
    return ""


def code_text(pre: Tag) -> str:
    for junk in pre.select("[class*=linenumber], [class*=line-number], [class*=lineno], button"):
        junk.decompose()
    # Some highlighters render one element per line without newlines between them.
    lines = pre.select("[class~=line], [data-line]")
    if lines and "\n" not in pre.get_text():
        text = "\n".join(l.get_text() for l in lines)
    else:
        text = pre.get_text()
    return text.strip("\n")


class Converter(MarkdownConverter):
    def convert_figure(self, el, text, *args, **kwargs):
        img = el.find("img")
        cap = el.find("figcaption")
        if not img:
            return text
        alt = htmlmod.escape(img.get("alt", "") or "", quote=True)
        src = img.get("src", "")
        caption = cap.get_text(" ", strip=True) if cap else ""
        out = f'<figure>\n  <img src="{src}" alt="{alt}" loading="lazy" />\n'
        if caption:
            out += f"  <figcaption>{htmlmod.escape(caption)}</figcaption>\n"
        return "\n\n" + out + "</figure>\n\n"

    def convert_iframe(self, el, text, *args, **kwargs):
        src = el.get("src", "")
        if not src:
            return ""
        title = el.get("title") or "Embedded content"
        if "youtube" in src:
            m = re.search(r"/embed/([\w-]+)", src)
            if m:
                src = f"https://www.youtube.com/watch?v={m.group(1)}"
                title = el.get("title") or "Video"
        return f"\n\n[▶ {title}]({src})\n\n"


def html_to_markdown(fragment: Tag) -> str:
    # Replace code blocks with placeholders so markdownify can't mangle them.
    blocks: list[str] = []
    for pre in fragment.find_all("pre"):
        lang = code_language(pre)
        body = code_text(pre)
        fence = "````" if "```" in body else "```"
        blocks.append(f"{fence}{lang}\n{body}\n{fence}")
        pre.replace_with(BeautifulSoup(f"<p>CODEBLOCK{len(blocks) - 1}PLACEHOLDER</p>", "html.parser"))

    md = Converter(
        heading_style="ATX",
        bullets="-",
        escape_misc=False,
        escape_asterisks=False,
        escape_underscores=False,
        strip=["script", "style", "noscript", "button", "svg", "form", "input"],
    ).convert_soup(fragment)

    for i, block in enumerate(blocks):
        md = md.replace(f"CODEBLOCK{i}PLACEHOLDER", "\n" + block + "\n")
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip() + "\n"


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #


def real_image_url(src: str, base: str) -> str:
    src = src.strip()
    if not src or src.startswith("data:"):
        return ""
    absolute = urljoin(base, src)
    p = urlparse(absolute)
    # Next.js image optimizer: /_next/image?url=<original>&w=...
    if p.path.endswith("/_next/image"):
        q = parse_qs(p.query).get("url")
        if q:
            return urljoin(base, unquote(q[0]))
    return absolute


def pick_src(img: Tag) -> str:
    for attr in ("data-src", "data-original", "src"):
        v = img.get(attr)
        if v and not v.startswith("data:"):
            return v
    srcset = img.get("srcset") or img.get("data-srcset")
    if srcset:
        # Highest resolution candidate.
        return srcset.split(",")[-1].strip().split(" ")[0]
    return ""


def absolutize_links(fragment: Tag, base_url: str) -> None:
    """Make relative links point at the original site (they would 404 here)."""
    for a in fragment.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        a["href"] = urljoin(base_url, href)


def localize_images(fragment: Tag, base_url: str, slug: str, stats: dict) -> None:
    dest = IMAGE_DIR / slug
    used: dict[str, str] = {}
    for img in fragment.find_all("img"):
        # Drop <picture><source> siblings; the <img> is enough.
        if img.parent and img.parent.name == "picture":
            for s in img.parent.find_all("source"):
                s.decompose()
            img.parent.unwrap()
        url = real_image_url(pick_src(img), base_url)
        if not url:
            img.decompose()
            continue
        if url in used:
            local = used[url]
        else:
            name = Path(unquote(urlparse(url).path)).name or "image"
            name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
            stem, ext = os.path.splitext(name)
            if not ext:
                ext = ".png"
            name = f"{stem[:80]}{ext.lower()}"
            n = 1
            while name in used.values():
                n += 1
                name = f"{stem[:80]}-{n}{ext.lower()}"
            target = dest / name
            if not target.exists() or target.stat().st_size == 0:
                try:
                    data = fetch(url, binary=True, browser_ok=False)
                    dest.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    stats["images"] += 1
                except Exception as e:  # noqa: BLE001
                    log(f"   ! image failed: {url} ({e})")
                    stats["image_failures"].append(url)
                    img["src"] = url  # keep remote link rather than dropping it
                    continue
            local = name
            used[url] = local
        for attr in ("srcset", "data-src", "data-srcset", "sizes", "width", "height",
                     "style", "class", "decoding", "fetchpriority", "data-nimg", "loading"):
            if attr in img.attrs:
                del img[attr]
        img["src"] = f"/writing/{slug}/{local}"


# --------------------------------------------------------------------------- #
# Main-content extraction
# --------------------------------------------------------------------------- #


def p_text_len(node: Tag) -> int:
    return sum(len(p.get_text(" ", strip=True)) for p in node.find_all(["p", "li", "pre", "td"]))


def find_main_content(soup: BeautifulSoup) -> Tag | None:
    candidates = soup.select(
        "article, main, [class*=prose], [class*=markdown], [class*=post-content], "
        "[class*=blog-content], [class*=article-body], [class*=content], [itemprop=articleBody]"
    )
    if not candidates:
        return None
    scored = [(p_text_len(c), c) for c in candidates]
    best = max(s for s, _ in scored)
    if best < 300:
        return None
    # Deepest container that still holds ~all of the text.
    good = [c for s, c in scored if s >= 0.85 * best]
    good.sort(key=lambda c: len(list(c.parents)), reverse=True)
    return good[0]


def readability_content(html: str) -> Tag:
    from readability import Document

    doc = Document(html)
    return BeautifulSoup(doc.summary(html_partial=True), "lxml").body or BeautifulSoup("", "lxml")


JUNK_SELECTORS = [
    "script", "style", "noscript", "nav", "footer", "aside", "form", "button", "svg",
    "[class*=share]", "[class*=newsletter]", "[class*=subscribe]", "[class*=related]",
    "[class*=breadcrumb]", "[class*=toc]", "[class*=table-of-contents]", "[aria-hidden=true]",
    "[class*=copy-button]", "[class*=CopyButton]",
]


def clean_fragment(fragment: Tag, title: str) -> Tag:
    for sel in JUNK_SELECTORS:
        for el in fragment.select(sel):
            # Never remove code blocks or anything holding them.
            if el.name == "pre" or el.find("pre"):
                continue
            el.decompose()
    for h1 in fragment.find_all("h1"):
        h1.decompose()  # title is rendered by the layout
    # Anchor links inside headings (e.g. "#" permalinks)
    for h in fragment.find_all(["h2", "h3", "h4", "h5", "h6"]):
        for a in h.find_all("a"):
            if (a.get("href") or "").startswith("#") or not a.get_text(strip=True):
                a.unwrap() if a.get_text(strip=True) else a.decompose()
    return fragment


def json_ld(soup: BeautifulSoup) -> list[dict]:
    out = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except Exception:  # noqa: BLE001
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data])
        out.extend(i for i in items if isinstance(i, dict))
    return out


def meta(soup: BeautifulSoup, *names: str) -> str:
    for n in names:
        el = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n})
        if el and el.get("content"):
            return el["content"].strip()
    return ""


# --------------------------------------------------------------------------- #
# ClickHouse
# --------------------------------------------------------------------------- #

CH_POST_RE = re.compile(r"^(?:https://clickhouse\.com)?/blog/([A-Za-z0-9][A-Za-z0-9._-]+)/?$")
CH_NON_POSTS = {"tag", "category", "author", "authors", "page", "rss.xml"}


def clickhouse_listing(url: str) -> tuple[list[str], int | None, str]:
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    slugs = []
    for a in soup.find_all("a", href=True):
        m = CH_POST_RE.match(a["href"].split("#")[0].split("?")[0])
        if m and m.group(1) not in CH_NON_POSTS:
            slugs.append(m.group(1))
    # Next.js flight data may carry slugs not present as anchors.
    for m in re.finditer(r'\\?"slug\\?"\s*:\s*\\?"([A-Za-z0-9._-]+)\\?"', html):
        slugs.append(m.group(1))
    count = None
    m = re.search(r"(\d+)\s+(?:articles|posts|blog posts)", soup.get_text(" "), re.I)
    if m:
        count = int(m.group(1))
    return dedupe(slugs), count, html


def clickhouse_byline(soup: BeautifulSoup) -> tuple[list[str], str]:
    """Authors and date from the byline under the title: "A, B and C  Jan 16, 2026 · 8 minutes read"."""
    h1 = soup.find("h1")
    if not h1:
        return [], ""
    parts = []
    for el in h1.find_all_next(string=True, limit=40):
        t = el.strip()
        if not t:
            continue
        parts.append(t)
        if DATE_TEXT_RE.search(t):
            break
    text = " ".join(parts)
    title = h1.get_text(" ", strip=True)
    if text.startswith(title):
        text = text[len(title):]
    m = DATE_TEXT_RE.search(text)
    if not m:
        return [], ""
    date = norm_date(m.group(0).replace(".", "").replace("Sept", "Sep"))
    who = re.sub(r"\s+", " ", text[: m.start()]).strip(" ,·|")
    names = [n.strip(" ,") for n in re.split(r"\s*,\s*|\s+and\s+|\s*&\s*", who)]
    names = [n for n in names if 2 < len(n) < 50 and not re.search(r"\d", n)]
    return dedupe(names), date


def clickhouse_authors(soup: BeautifulSoup, content: Tag | None) -> list[str]:
    names, _ = clickhouse_byline(soup)
    if names:
        return names
    for item in json_ld(soup):
        a = item.get("author")
        for x in a if isinstance(a, list) else [a] if a else []:
            names.append(x.get("name", "") if isinstance(x, dict) else str(x))
    if not names:
        m = meta(soup, "author", "article:author")
        if m:
            names.extend(re.split(r",\s*|\s+and\s+|\s*&\s*", m))
    if not names:
        # Author links that appear in the page header (before the article body).
        body_pos = None
        if content is not None:
            body_pos = content.sourceline
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r"(?:/authors/|[?&]author=)([a-z0-9-]+)", href)
            if not m:
                continue
            if body_pos and a.sourceline and a.sourceline > body_pos and content is not None \
                    and a not in content.descendants:
                continue  # sidebar / related posts after the article
            text = a.get_text(" ", strip=True)
            names.append(text if 2 < len(text) < 60 else titlecase_slug(m.group(1)))
    return dedupe([n.strip() for n in names if n and n.strip()])


def clickhouse_article(slug: str, stats: dict) -> Article | None:
    url = f"https://clickhouse.com/blog/{slug}"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    ld = json_ld(soup)
    if DEBUG:
        debug(f"{slug}: json-ld types={[i.get('@type') for i in ld]}, "
              f"meta author={meta(soup, 'author')!r}, "
              f"published={meta(soup, 'article:published_time')!r}, "
              f"time tags={[t.get('datetime') for t in soup.find_all('time')][:3]}, "
              f"author links={[a['href'] for a in soup.find_all('a', href=True) if 'author' in a['href']][:6]}")

    title = ""
    for item in ld:
        title = title or item.get("headline", "")
    title = title or meta(soup, "og:title") or (soup.h1.get_text(" ", strip=True) if soup.h1 else "")
    title = re.sub(r"\s*[|\-–]\s*ClickHouse\s*$", "", title).strip()

    content = (soup.select_one("article .rich-text") or soup.select_one("article [class*=rich-text]")
               or soup.find("article") or find_main_content(soup))
    authors = clickhouse_authors(soup, content)
    if authors and not any(is_me(a) for a in authors):
        log(f"   - skipping {slug}: authors are {authors}")
        return None
    if not authors and AUTHOR_NAME.lower() not in soup.get_text(" ").lower():
        log(f"   - skipping {slug}: author not found on page")
        return None

    date = ""
    m = re.search(r'\\?"slug\\?"\s*:\s*\\?"' + re.escape(slug) + r'\\?"\s*,\s*\\?"date\\?"\s*:\s*\\?"(\d{4}-\d{2}-\d{2})', html)
    if m:
        date = m.group(1)
    date = date or clickhouse_byline(soup)[1]
    for item in ld:
        date = date or norm_date(item.get("datePublished", ""))
    date = date or norm_date(meta(soup, "article:published_time", "date", "publish_date"))
    if not date:
        t = soup.find("time")
        if t:
            date = norm_date(t.get("datetime") or t.get_text(strip=True))
    if not date:
        header_text = soup.get_text(" ")[: max(4000, len(soup.get_text(" ")) // 5)]
        m = DATE_TEXT_RE.search(header_text)
        if m:
            date = norm_date(m.group(0).replace(".", "").replace("Sept", "Sep"))

    tags = []
    for item in ld:
        kw = item.get("keywords")
        if isinstance(kw, str):
            tags += [k.strip() for k in kw.split(",")]
        elif isinstance(kw, list):
            tags += kw
    tags += [m["content"] for m in soup.find_all("meta", attrs={"property": "article:tag"})]
    for a in soup.find_all("a", href=True):
        m = re.search(r"/blog\?category=([a-z0-9-]+)", a["href"])
        if m:
            tags.append(m.group(1))

    if content is None:
        debug(f"{slug}: no semantic container, using readability")
        content = readability_content(html)
    else:
        debug(f"{slug}: content container <{content.name} class={content.get('class')}>")
    content = clean_fragment(content, title)
    for a in content.select('a[href*="loc=blog-cta"], a[href*="clickhouse.cloud/signUp"]'):
        block = a.find_parent(["p", "div", "li"])
        if block is not None and block is not content and len(block.get_text(" ", strip=True)) < 400:
            block.decompose()
    absolutize_links(content, url)
    localize_images(content, url, slug, stats)
    body = html_to_markdown(content)

    description = meta(soup, "description", "og:description")
    if len(description) < 40:
        description = markdown_to_text(body)
    return Article(
        url=url,
        source="clickhouse",
        slug=slug,
        title=title,
        date=date,
        coauthors=[a for a in authors if not is_me(a)],
        tags=dedupe([t.lower() for t in tags if t])[:6],
        summary=first_sentence(description),
        body=body,
    )


# --------------------------------------------------------------------------- #
# Medium
# --------------------------------------------------------------------------- #


def medium_slug(url: str) -> str:
    last = urlparse(url).path.rstrip("/").split("/")[-1]
    return re.sub(r"-[0-9a-f]{8,12}$", "", last)


def medium_article(url: str, feed_items: dict, stats: dict) -> Article:
    slug = medium_slug(url)
    post_id = url.rstrip("/").rsplit("-", 1)[-1]
    item = feed_items.get(post_id)
    if item:
        debug(f"{slug}: found in RSS feed")
        content = BeautifulSoup(item["html"], "lxml").body
        title, date, tags = item["title"], item["date"], item["tags"]
    else:
        debug(f"{slug}: not in feed, fetching article page")
        html = fetch(url)
        soup = BeautifulSoup(html, "lxml")
        title = meta(soup, "og:title") or (soup.h1.get_text(strip=True) if soup.h1 else slug)
        title = re.sub(r"\s*\|.*$", "", title)
        date = norm_date(meta(soup, "article:published_time"))
        if not date:
            for i in json_ld(soup):
                date = date or norm_date(i.get("datePublished", ""))
        tags = []
        content = soup.find("article") or readability_content(html)
    content = clean_fragment(content, title)
    absolutize_links(content, url)
    # Medium repeats the title/subtitle at the top of the body.
    for h in content.find_all(["h3", "h4"], limit=1):
        if h.get_text(strip=True) == title:
            h.decompose()
    for img in content.find_all("img"):  # tracking pixel
        if "_/stat" in (img.get("src") or ""):
            img.decompose()
    localize_images(content, url, slug, stats)
    body = html_to_markdown(content)
    return Article(
        url=url, source="medium", slug=slug, title=title, date=date, tags=tags,
        summary=first_sentence(markdown_to_text(body)), body=body,
    )


def medium_feed() -> dict:
    items = {}
    try:
        xml = fetch(MEDIUM_FEED, browser_ok=False)
    except Exception as e:  # noqa: BLE001
        log(f"   ! Medium feed unavailable: {e}")
        return items
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    root = ET.fromstring(xml.encode("utf-8"))
    for it in root.iter("item"):
        link = (it.findtext("link") or "").split("?")[0]
        post_id = link.rstrip("/").rsplit("-", 1)[-1]
        items[post_id] = {
            "link": link,
            "title": it.findtext("title") or "",
            "date": norm_date(it.findtext("pubDate") or ""),
            "tags": [c.text for c in it.findall("category") if c.text],
            "html": it.findtext("content:encoded", namespaces=ns) or "",
        }
    log(f"   Medium feed: {len(items)} item(s)")
    return items


# --------------------------------------------------------------------------- #
# ryadh.net/blog (Jekyll)
# --------------------------------------------------------------------------- #

RB_POST_RE = re.compile(r"/blog/(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)/?$")


def ryadh_blog_posts() -> list[str]:
    ids = []
    try:
        html = fetch(RYADH_BLOG, browser_ok=False)
        page = RYADH_BLOG
        while True:
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                m = RB_POST_RE.search(urljoin(page, a["href"]))
                if m:
                    ids.append(m.group(1))
            nxt = soup.select_one(".pager .next a, a[rel=next]")
            if not nxt:
                break
            page = urljoin(page, nxt["href"])
            html = fetch(page, browser_ok=False)
    except Exception as e:  # noqa: BLE001
        log(f"   ! {RYADH_BLOG} unavailable ({e}); listing posts from GitHub instead")
        try:
            listing = json.loads(fetch(RYADH_BLOG_API, browser_ok=False))
            ids = [f["name"][:-3] for f in listing if f["name"].endswith(".md")]
        except Exception:  # noqa: BLE001
            # Last resort: the committed Jekyll build of the index page.
            html = fetch(f"{RYADH_BLOG_RAW}/_site/index.html", browser_ok=False)
            ids = [m.group(1) for m in re.finditer(r'href="[^"]*?(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)/?"', html)]
    return dedupe(ids)


def ryadh_blog_article(post_id: str, stats: dict) -> Article:
    raw = fetch(f"{RYADH_BLOG_RAW}/_posts/{post_id}.md", browser_ok=False)
    _, fm_text, body = raw.split("---", 2)
    fm = yaml.safe_load(fm_text) or {}
    slug = post_id[11:]
    date = post_id[:10]

    # Kramdown attribute lists and Liquid
    body = re.sub(r"^\{:.*\}\s*$", "", body, flags=re.M)
    body = body.replace("{{ site.baseurl }}", "")

    # "Repris ici, cet article est originellement paru sur: [url](url)"
    republished = ""
    m = re.search(r"\n[^\n]*originellement paru sur:\s*\[[^\]]*\]\(([^)]+)\)[^\n]*", body)
    if m:
        republished = m.group(1)
        body = body[: m.start()] + body[m.end():]

    # Images: /img/foo.jpg -> /writing/<slug>/foo.jpg
    def repl(mm):
        alt, path = mm.group(1), mm.group(2)
        name = Path(path).name
        target = IMAGE_DIR / slug / name
        if not target.exists():
            for base in (f"{RYADH_BLOG.rstrip('/')}", RYADH_BLOG_RAW):
                try:
                    data = fetch(f"{base}{path}", binary=True, browser_ok=False)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    stats["images"] += 1
                    break
                except Exception:  # noqa: BLE001
                    continue
            else:
                stats["image_failures"].append(path)
                return mm.group(0)
        return f"![{alt}](/writing/{slug}/{name})"

    body = re.sub(r"!\[([^\]]*)\]\((/img/[^)\s]+)\)", repl, body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    text = markdown_to_text(body)
    summary = fm.get("subtitle") or first_sentence(text)

    return Article(
        url=f"{RYADH_BLOG}{post_id}/",
        source="ryadh.net",
        slug=slug,
        title=str(fm.get("title", slug)).strip(),
        date=date,
        tags=[str(t) for t in fm.get("tags", []) if t],
        summary=summary,
        body=body,
        republished_from=republished,
        lang=detect_lang(text),
    )


# --------------------------------------------------------------------------- #
# Writing files
# --------------------------------------------------------------------------- #


def existing_index() -> dict[str, tuple[Path, dict, str]]:
    idx = {}
    for p in CONTENT_DIR.glob("*.md"):
        text = p.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        _, fm, body = text.split("---", 2)
        data = yaml.safe_load(fm) or {}
        if data.get("canonical_url"):
            idx[data["canonical_url"].rstrip("/")] = (p, data, body)
    return idx


def content_hash(a: Article) -> str:
    payload = json.dumps([a.title, a.date, a.coauthors, a.body, a.republished_from, a.lang], ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def write_article(a: Article, index: dict, report: dict) -> None:
    h = content_hash(a)
    key = a.url.rstrip("/")
    prev = index.get(key)
    if prev and prev[1].get("content_hash") == h:
        report["unchanged"].append(a.url)
        return

    fm = {
        "title": a.title,
        "date": a.date,
        "source": a.source,
        "canonical_url": a.url,
        "coauthors": a.coauthors,
        "tags": a.tags,
        "summary": a.summary,
        "reading_time": reading_time(a.body),
    }
    if a.republished_from:
        fm["republished_from"] = a.republished_from
    if a.lang != "en":
        fm["lang"] = a.lang
    if prev:  # keep hand-edited fields
        for k in ("summary", "tags", "title_override"):
            if prev[1].get(k):
                fm[k] = prev[1][k]
    fm["content_hash"] = h

    year = (a.date or "0000")[:4]
    path = CONTENT_DIR / f"{year}-{a.slug}.md"
    if prev and prev[0] != path:
        prev[0].unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n" + a.body
    path.write_text(text, encoding="utf-8")
    report["updated" if prev else "new"].append(a.url)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def inspect(url: str) -> None:
    """Print page-structure diagnostics for one URL (used to tune selectors)."""
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    log(f"\n######## INSPECT {url} ({len(html)} bytes)")
    for item in json_ld(soup):
        log("json-ld:", json.dumps(item, ensure_ascii=False)[:700])
    for m in soup.find_all("meta"):
        k = m.get("property") or m.get("name")
        if k and any(x in k for x in ("date", "time", "author", "description", "tag")):
            log(f"meta {k} = {m.get('content', '')[:150]!r}")
    log("date-like strings:", DATE_TEXT_RE.findall(soup.get_text(" "))[:12])
    log("time tags:", [(t.get("datetime"), t.get_text(strip=True)) for t in soup.find_all("time")][:6])
    log("next data:", bool(soup.find("script", id="__NEXT_DATA__")), "| flight chunks:", html.count("self.__next_f.push"))
    for key in ("publishedAt", "published_at", "datePublished", "publishDate", "createdAt"):
        i = html.find(key)
        if i >= 0:
            log(f"raw {key}: …{html[max(0, i - 80): i + 120]!r}")
    h1 = soup.find("h1")
    if h1:
        log("h1:", h1.get_text(" ", strip=True)[:120])
        log("h1 parent chain:", [f"{p.name}.{'.'.join(p.get('class') or [])[:60]}" for p in list(h1.parents)[:5]])
        after = []
        for el in h1.find_all_next(string=True, limit=60):
            t = el.strip()
            if t:
                after.append(t)
        log("text after h1:", " | ".join(after)[:900])
    scored = sorted(((p_text_len(c), c) for c in soup.find_all(["article", "main", "div", "section"])),
                    key=lambda x: -x[0])[:8]
    for n, c in scored:
        log(f"container {n:>6} <{c.name} id={c.get('id')} class={' '.join(c.get('class') or [])[:90]}> depth={len(list(c.parents))}")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    log("author links:", [h for h in links if "author" in h][:20])
    log("page links:", sorted({h for h in links if "page=" in h})[:20])
    log("blog links:", len([h for h in links if "/blog/" in h]), [h for h in links if "/blog/" in h][:40])
    for m in re.finditer(r"\d+\s+(?:articles|posts)", soup.get_text(" "), re.I):
        log("count text:", soup.get_text(" ")[max(0, m.start() - 60): m.end() + 30])


def main() -> int:
    global DEBUG, FORCE_PLAYWRIGHT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="only process URLs containing this substring")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--playwright", action="store_true", help="always fetch HTML with a headless browser")
    ap.add_argument("--inspect", nargs="+", metavar="URL", help="print page-structure diagnostics and exit")
    ap.add_argument("--skip", nargs="*", default=[], choices=["clickhouse", "medium", "ryadh.net"])
    args = ap.parse_args()
    DEBUG, FORCE_PLAYWRIGHT = args.debug, args.playwright
    if args.inspect:
        for u in args.inspect:
            try:
                inspect(u)
            except Exception as e:  # noqa: BLE001
                log(f"inspect failed for {u}: {e}")
        return 0

    report = {"found": [], "new": [], "updated": [], "unchanged": [], "failed": [], "skipped": []}
    stats = {"images": 0, "image_failures": []}
    index = existing_index()
    jobs: list[tuple[str, str, object]] = []  # (source, url, thunk)

    # --- discover ---------------------------------------------------------
    if "clickhouse" not in args.skip:
        log("Collecting ClickHouse articles…")
        slugs: list[str] = []
        declared = None
        for listing in CLICKHOUSE_LISTINGS:
            try:
                found, count, _ = clickhouse_listing(listing)
                log(f"   {listing}: {len(found)} candidate link(s)" + (f", page says {count}" if count else ""))
                slugs += found
                declared = declared or count
            except Exception as e:  # noqa: BLE001
                log(f"   ! {listing}: {e}")
        # Follow further pages until no new candidates appear.
        page = 3
        while True:
            url = f"https://clickhouse.com/blog?author={AUTHOR_SLUG}&page={page}"
            try:
                found, _, _ = clickhouse_listing(url)
            except Exception:  # noqa: BLE001
                break
            new = [s for s in found if s not in slugs]
            if not new:
                break
            log(f"   {url}: {len(new)} new candidate link(s)")
            slugs += new
            page += 1
        for u in CLICKHOUSE_EXPLICIT:
            slugs.append(CH_POST_RE.match(u).group(1))
        slugs = dedupe(slugs)
        for s in slugs:
            jobs.append(("clickhouse", f"https://clickhouse.com/blog/{s}", lambda s=s: clickhouse_article(s, stats)))
        report["ch_declared"] = declared

    if "medium" not in args.skip:
        log("Collecting Medium articles…")
        feed = medium_feed()
        urls = list(MEDIUM_URLS)
        for it in feed.values():
            if it["link"] and it["link"].rsplit("-", 1)[-1] not in [u.rsplit("-", 1)[-1] for u in urls]:
                urls.append(it["link"])
        for u in urls:
            jobs.append(("medium", u, lambda u=u: medium_article(u, feed, stats)))

    if "ryadh.net" not in args.skip:
        log("Collecting ryadh.net/blog posts…")
        for pid in ryadh_blog_posts():
            jobs.append(("ryadh.net", f"{RYADH_BLOG}{pid}/", lambda pid=pid: ryadh_blog_article(pid, stats)))

    if args.only:
        jobs = [j for j in jobs if args.only in j[1]]

    # --- process ----------------------------------------------------------
    log(f"\nProcessing {len(jobs)} candidate(s)…")
    ch_archived = []
    for source, url, thunk in jobs:
        log(f" • {url}")
        try:
            art = thunk()
            if art is None:
                report["skipped"].append(url)
                continue
            if not art.title or not art.date or len(art.body) < 200:
                raise RuntimeError(f"incomplete extraction (title={bool(art.title)}, "
                                   f"date={art.date!r}, body={len(art.body)} chars)")
            report["found"].append(url)
            if source == "clickhouse":
                ch_archived.append(art)
            write_article(art, index, report)
        except Exception as e:  # noqa: BLE001
            log(f"   ! FAILED: {e}")
            report["failed"].append((url, str(e)))

    # --- report -----------------------------------------------------------
    log("\n================ Archive report ================")
    for k in ("found", "new", "updated", "unchanged", "skipped"):
        log(f"{k:>10}: {len(report[k])}")
    log(f"{'failed':>10}: {len(report['failed'])}")
    for url, why in report["failed"]:
        log(f"            - {url}: {why}")
    log(f"{'images':>10}: {stats['images']} downloaded, {len(stats['image_failures'])} failed")
    for u in stats["image_failures"]:
        log(f"            - {u}")
    if "clickhouse" not in args.skip and not args.only:
        declared = report.get("ch_declared")
        expected = max(filter(None, [declared, CLICKHOUSE_EXPECTED]))
        n = len(ch_archived)
        log(f"ClickHouse: {n} archived (author page declares {declared or 'n/a'}; "
            f"expected at least {expected} + explicit includes)")
        if n < expected:
            log(f"   ! {expected - n} ClickHouse article(s) missing — check the listing pages")
        for a in sorted(ch_archived, key=lambda a: a.date, reverse=True):
            log(f"   {a.date}  {a.title}" + (f"  (with {', '.join(a.coauthors)})" if a.coauthors else ""))
    if _browser is not None:
        _browser.close()
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
