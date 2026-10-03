import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

// Files are named <yyyy>-<slug>.md; the URL is /writing/<slug>/.
const writing = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/writing",
    generateId: ({ entry }) => entry.replace(/\.md$/, "").replace(/^\d{4}-/, ""),
  }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    source: z.enum(["clickhouse", "medium", "ryadh.net"]),
    canonical_url: z.string().url(),
    coauthors: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    summary: z.string().default(""),
    reading_time: z.number().int().positive(),
    republished_from: z.string().url().optional(),
    lang: z.string().optional(),
    content_hash: z.string().optional(),
  }),
});

export const collections = { writing };
