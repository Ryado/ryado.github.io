// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import imageAttrs from "./integrations/image-attrs.mjs";
import { accessibleTheme } from "./integrations/accessible-theme.mjs";
import githubLight from "@shikijs/themes/github-light";
import githubDarkDimmed from "@shikijs/themes/github-dark-dimmed";
import { readdirSync, readFileSync } from "node:fs";

// Old Jekyll blog lived at /blog/YYYY-MM-DD-slug/. Map each archived
// ryadh.net post to its new home at /writing/<slug>/.
const oldBlogRedirects = Object.fromEntries(
  readdirSync("./src/content/writing")
    .filter((f) => f.endsWith(".md"))
    .map((f) => readFileSync(`./src/content/writing/${f}`, "utf8"))
    .map((text) => text.match(/canonical_url:\s*['"]?https?:\/\/www\.ryadh\.net\/blog\/(\d{4}-\d{2}-\d{2}-([a-z0-9-]+))\/?/))
    .filter(Boolean)
    .map((m) => [`/blog/${m[1]}`, `/writing/${m[2]}/`]),
);

export default defineConfig({
  site: "https://www.ryadh.net",
  trailingSlash: "ignore",
  integrations: [sitemap({ filter: (page) => !page.includes("/blog/") }), imageAttrs()],
  redirects: {
    "/blog": "/#writing",
    "/blog/aboutme": "/",
    "/blog/tags": "/#writing",
    ...oldBlogRedirects,
  },
  markdown: {
    shikiConfig: {
      // Backgrounds match --code-bg in global.css.
      themes: {
        light: accessibleTheme(githubLight, "#ffffff"),
        dark: accessibleTheme(githubDarkDimmed, "#18191d"),
      },
      wrap: false,
    },
  },
  build: { inlineStylesheets: "always" },
});
