// News-image entry for Friday 20 November 2026.
//
// The front page itself is drawn ahead of time as entry.png, and this
// program has one job only: put that exact image at /output/entry.png
// for the grader. Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
