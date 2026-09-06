// Documentation QA only: render SVG plates without changing their contents.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
async function main() {
  const qa = path.join(__dirname, 'qa');
  fs.mkdirSync(qa, { recursive: true });
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'), 'utf8'));
  for (const item of manifest) {
    await sharp(path.join(__dirname, 'images', item.file))
      .resize({ width: 1600 }).png()
      .toFile(path.join(qa, item.file.replace('.svg', '.png')));
  }
  for (let page = 0; page < 4; page++) {
    const tiles = [];
    for (let j = 0; j < 4; j++) {
      const item = manifest[page * 4 + j];
      const input = await sharp(path.join(qa, item.file.replace('.svg', '.png')))
        .resize({ width: 720, height: 800, fit: 'contain', background: '#ffffff' }).png().toBuffer();
      tiles.push({ input, left: (j % 2) * 740, top: Math.floor(j / 2) * 820 });
    }
    await sharp({ create: { width: 1480, height: 1640, channels: 3, background: '#dde5df' } })
      .composite(tiles).png().toFile(path.join(qa, `contact-${page + 1}.png`));
  }
  process.stdout.write(`Rendered ${manifest.length} SVGs and 4 contact sheets.\n`);
}
main().catch(err => { process.stderr.write(String(err)); process.exitCode = 1; });
