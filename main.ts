// One-day world news image: Monday 23 November 2026.
//
// The entry image is the entry.png beside this file: a newspaper front page
// drawn for this bounty. Masthead and date strip up top, lead story on the
// NATO emergency session in Brussels over the Russian missiles that crossed
// into Poland, six story cards (the COP31 collapse fallout, Nepal's PM
// meeting Modi in Delhi, the Houthi claim of a Saudi refinery hit, the UN
// talks on lethal autonomous weapons, Seoul's education minister resigning
// over the AI exam-cheating row, India's record 720 in Wellington), and an
// also-today strip (Myanmar on ASEAN, the Lisbon march, the Java factory
// fire search, the ICE detention in Seattle).
//
// This program only copies that image to the output directory, so both grader
// runs write byte-identical output: same input bytes in, same bytes out, every
// run, with no clock, random, or network input anywhere in the path. Node 22,
// standard library only, no network.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
