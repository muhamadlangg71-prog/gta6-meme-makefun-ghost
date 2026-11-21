// GTA 6 meme entry (Node 22, standard library only).
// Copies POST.json (the X post's address) from the repository to /output.
// The post itself is the entry: the house reads it from X.
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const post = join(here, 'POST.json');
if (!existsSync(post)) {
  process.stderr.write('gta6 meme: no POST.json at the repository root: post the meme on X first, then write its URL into POST.json\n');
  process.exit(2);
}
mkdirSync(out, { recursive: true });
copyFileSync(post, join(out, 'POST.json'));
process.stdout.write(`gta6 meme: copied POST.json to ${join(out, 'POST.json')}\n`);
