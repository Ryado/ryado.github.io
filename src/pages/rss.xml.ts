import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { allWriting } from "../lib";
import { SITE, SOURCES } from "../site";

export async function GET(context: APIContext) {
  const posts = await allWriting();
  return rss({
    title: `${SITE.name} — Writing`,
    description: SITE.description,
    site: context.site!,
    items: posts.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.summary,
      link: `/writing/${p.id}/`,
      categories: [SOURCES[p.data.source].label, ...p.data.tags],
    })),
    customData: "<language>en</language>",
  });
}
