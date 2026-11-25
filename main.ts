// news-image-20261125 — THE WORLD TODAY, Tuesday 25 November 2026.
// One 1024x1024 front page with 50 world-news stories, every one verified
// against a live source before it was drawn. The drawing itself lives in
// render_frontpage.py (Pillow); this file only hands the finished PNG to
// the grader, unchanged, at /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing beside main.ts');
}
const bytes = statSync(src).size;
if (bytes === 0 || bytes > 1024 * 1024) {
  throw new Error(`entry.png must be a non-empty PNG of at most 1 MiB, got ${bytes} bytes`);
}
const out = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(src, out);
console.log(`copied entry.png (${bytes} bytes) to ${out}`);
