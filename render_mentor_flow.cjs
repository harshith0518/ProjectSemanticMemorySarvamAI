const path=require('node:path');
const sharp=require('sharp');
(async()=>{
 await sharp(path.join(__dirname,'KIVI_COMPLETE_FLOW.svg')).png().toFile(path.join(__dirname,'KIVI_COMPLETE_FLOW.png'));
 process.stdout.write('Rendered the single SVG for visual review.\n');
})().catch(e=>{process.stderr.write(String(e));process.exitCode=1});
