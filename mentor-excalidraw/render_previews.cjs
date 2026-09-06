const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
async function main(){
  const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'),'utf8'));
  const tiles=[];
  for(let i=0;i<manifest.frames.length;i++){
    const f=manifest.frames[i];
    const src=path.join(__dirname,'previews',f.file);
    await sharp(src).png().toFile(src.replace('.svg','.png'));
    const input=await sharp(src).resize({width:800,height:1000,fit:'contain',background:'#fff'}).png().toBuffer();
    tiles.push({input,left:(i%2)*820,top:Math.floor(i/2)*1020});
  }
  await sharp({create:{width:1640,height:3060,channels:3,background:'#d7e2dd'}}).composite(tiles).png().toFile(path.join(__dirname,'previews','contact-sheet.png'));
  process.stdout.write('Rendered all 6 frames and a contact sheet.\n');
}
main().catch(e=>{process.stderr.write(String(e));process.exitCode=1;});
