// main.ts — copies entry.png to the output directory.
// No network, stdlib only. A pure copy, so two runs are byte-identical.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "IMG_4957.png"), join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
