import { getCollection, type CollectionEntry } from "astro:content";

export type Post = CollectionEntry<"writing">;

/** All writing, newest first. */
export async function allWriting(): Promise<Post[]> {
  const posts = await getCollection("writing");
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** Original publication URL, or undefined for posts whose home is this site. */
export function originalUrl(p: Post): string | undefined {
  return p.data.source === "ryadh.net" ? undefined : p.data.canonical_url;
}
