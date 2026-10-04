# ryadh.net

Personal site of Ryadh Dahimene, built with [Astro](https://astro.build) and deployed to GitHub Pages.

```sh
npm install
npm run dev      # local preview at http://localhost:4321
npm run build    # static output in dist/
```

## Writing archive

Every article lives in `src/content/writing/<yyyy>-<slug>.md`, with images in `public/writing/<slug>/`.
Animated GIFs over 300 KB are converted to looping MP4s (needs `ffmpeg`).
They are produced by `scripts/archive.py`, which pulls posts from the ClickHouse blog, Medium and the old
ryadh.net/blog, and is safe to re-run (unchanged posts are skipped; hand-edited `summary` and `tags` are kept).

```sh
pip install -r scripts/requirements.txt
python scripts/archive.py            # everything
python scripts/archive.py --only kinesis
python scripts/archive.py --inspect <url>   # debug page structure
```

The **Archive writing** workflow runs it weekly (and on demand from the Actions tab), commits any changes,
and the deploy workflow then republishes the site.

Posts listed under *Essays* are named in `ESSAYS` in `src/site.ts`; everything else is listed under *Launches*.

## Deploying

Pushes to `master` are built and deployed by `.github/workflows/deploy.yml`.
In the repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**.
