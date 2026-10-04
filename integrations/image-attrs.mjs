// Post-build pass over the generated HTML: give local <img> tags intrinsic
// width/height (prevents layout shift) and lazy/async loading hints.
import { readFileSync } from "node:fs";
import { readFile, writeFile, readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { imageSize } from "image-size";

async function* htmlFiles(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(p);
    else if (entry.name.endsWith(".html")) yield p;
  }
}

export default function imageAttrs() {
  return {
    name: "image-attrs",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const root = fileURLToPath(dir);
        const cache = new Map();
        let count = 0;
        for await (const file of htmlFiles(root)) {
          const html = await readFile(file, "utf8");
          let seen = 0;
          const out = html.replace(/<img\b([^>]*?)\s*\/?>/g, (tag, attrs) => {
            const src = attrs.match(/\ssrc="(\/[^"]+)"/)?.[1];
            if (!src || src.startsWith("//")) return tag;
            seen += 1;
            let add = "";
            if (!/\swidth=/.test(attrs)) {
              if (!cache.has(src)) {
                try {
                  cache.set(src, imageSize(readFileSync(join(root, decodeURIComponent(src)))));
                } catch {
                  cache.set(src, null);
                }
              }
              const size = cache.get(src);
              if (size?.width && size?.height) add += ` width="${size.width}" height="${size.height}"`;
            }
            // Keep the first image eager: it is often the largest contentful paint.
            if (!/\sloading=/.test(attrs) && seen > 1) add += ` loading="lazy"`;
            if (!/\sdecoding=/.test(attrs)) add += ` decoding="async"`;
            count += 1;
            return `<img${attrs}${add}>`;
          });
          if (out !== html) await writeFile(file, out);
        }
        logger.info(`annotated ${count} image tag(s)`);
      },
    },
  };
}
