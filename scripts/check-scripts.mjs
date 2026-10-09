// Syntax-checks every inline <script> block in dist/index.html without executing it.
// The site has no TypeScript and no build step, so this is the "typecheck" equivalent:
// a parse failure here means the published page would throw before running.
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("../dist/index.html", import.meta.url), "utf8");
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
if (blocks.length === 0) throw new Error("no inline <script> blocks found in dist/index.html");
for (const [i, src] of blocks.entries()) {
  try {
    new Function(src); // parse only; the IIFE body is never invoked
  } catch (e) {
    console.error(`inline script #${i + 1} failed to parse: ${e.message}`);
    process.exit(1);
  }
}
console.log(`inline scripts parsed OK: ${blocks.length} block(s), ${html.length} bytes of HTML`);
