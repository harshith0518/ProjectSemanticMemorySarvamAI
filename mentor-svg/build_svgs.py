"""Generate portable, text-based SVG architecture plates. No app behavior implemented."""
from pathlib import Path
from html import escape
import argparse, json, math, re, sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
from tools.font_support import font, svg_font_family
from tools.package_support import write_handoff_archive
OUT = HERE / 'images'
OUT.mkdir(exist_ok=True)
W, M, GAP = 2000, 72, 28
FONT = svg_font_family()
C = dict(bg='#fbfcfa', ink='#17382d', body='#354c41', muted='#5c7065', line='#ccd9cf',
         panel='#f0f5f0', accent='#1d6b54', amber='#fff0cf', amberink='#73501b', white='#ffffff', blue='#e1eff4')

def wrap(text, width, size, bold=False):
    f = font(size, bold)
    lines = []
    for para in str(text).split('\n'):
        line = ''
        for word in para.split():
            if f.getlength(word) > width:
                parts, part = [], ''
                for char in word:
                    if part and f.getlength(part + char) > width:
                        parts.append(part); part = char
                    else: part += char
                parts.append(part)
            else: parts = [word]
            for part in parts:
                trial = (line + ' ' + part).strip()
                if line and f.getlength(trial) > width:
                    lines.append(line); line = part
                else: line = trial
        lines.append(line)
    return lines

class Svg:
    def __init__(self, title, desc):
        self.title, self.desc, self.parts, self.bounds = title, desc, [], []
    def rect(self, x, y, w, h, fill=None, stroke=None, radius=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill or C["white"]}" stroke="{stroke or C["line"]}" stroke-width="1.5"/>')
    def text(self, x, y, text, width, size=24, bold=False, color=None, leading=None):
        leading = leading or size * 1.35
        lines = wrap(text, width, size, bold)
        color = color or C['body']
        self.parts.append(f'<text x="{x}" y="{y+size}" fill="{color}" font-family="{FONT}" font-size="{size}" font-weight="{700 if bold else 400}">')
        for i, line in enumerate(lines):
            self.parts.append(f'<tspan x="{x}" dy="{0 if i == 0 else leading}">{escape(line)}</tspan>')
            assert font(size, bold).getlength(line) <= width + .01, (text, line)
        self.parts.append('</text>')
        h = len(lines) * leading
        self.bounds.append((x, y, x+width, y+h, str(text)[:60]))
        return h
    def path(self, pts, arrow=True, both=False, color=None, dashed=False):
        d = 'M ' + ' L '.join(f'{x},{y}' for x,y in pts)
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color or C["accent"]}" stroke-width="2.5" stroke-linejoin="round" {"stroke-dasharray=\"7 6\"" if dashed else ""} {"marker-end=\"url(#arrow)\"" if arrow else ""} {"marker-start=\"url(#arrow-start)\"" if both else ""}/>')
    def finish(self, height, target):
        for x,y,x2,y2,label in self.bounds:
            assert min(x,y) >= 0 and x2 <= W+1 and y2 <= height+1, (target.name,label,(x,y,x2,y2),height)
        defs=f'''<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{C['accent']}"/></marker><marker id="arrow-start" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{C['accent']}"/></marker></defs>'''
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.desc)}</desc>{defs}<rect width="100%" height="100%" fill="{C["bg"]}"/>' + ''.join(self.parts) + '</svg>'
        target.write_text(svg,encoding='utf-8',newline='\n')
        return {'file':target.name,'title':self.title,'width':W,'height':height,'text_blocks':len(self.bounds)}

def block(svg,x,y,w,title,body,number=None,fill=None,min_h=0):
    title_lines=wrap(title,w-48,27,True)
    h_title=len(title_lines)*35
    h_body=len(wrap(body,w-48,24))*32.4
    h=max(min_h,48+h_title+h_body+(32 if number is not None else 0)+12)
    svg.rect(x,y,w,h,fill=fill or C['panel'])
    at=y+22
    if number is not None:
        svg.text(x+24,at,number,w-48,18,True,C['accent']); at+=32
    at+=svg.text(x+24,at,title,w-48,27,True,C['ink'],35)+10
    svg.text(x+24,at,body,w-48,24,False,C['body'])
    return h

def strip(svg,y,label,body,fill=C['panel']):
    inner=W-2*M-48
    h_body=len(wrap(body,inner,24))*32.4
    h=28+27+h_body+25
    svg.rect(M,y,W-2*M,h,fill=fill)
    svg.text(M+24,y+18,label,inner,18,True,C['accent'])
    svg.text(M+24,y+49,body,inner,24)
    return y+h

def detailed(ch):
    svg=Svg(ch['title'],ch['purpose']+' '+ch['remaining'])
    svg.text(M,35,'GOLDEN GOOSE / MENTOR REVIEW / '+ch['id'][:2],W-2*M,18,True,C['accent'])
    y=75
    y+=svg.text(M,y,ch['title'],W-2*M,44,True,C['ink'],53)+12
    y+=svg.text(M,y,ch['subtitle'],W-2*M,24,False,C['muted'])+18
    svg.rect(M,y,W-2*M,46,C['amber'],C['amber'],7)
    svg.text(M+16,y+8,'STATUS: REVIEWED PLAN • APPLICATION IMPLEMENTATION PENDING • TARGETS ARE NOT MEASURED RESULTS',W-2*M-32,18,True,C['amberink'])
    y+=69
    y+=svg.text(M,y,ch['purpose'],W-2*M,25,False,C['ink'])+27
    parallel=ch['id'].startswith('04-')
    svg.text(M,y,'PARALLEL REPRESENTATIONS' if parallel else 'PROCESS / READ THE NUMBERED STEPS',W-2*M,18,True,C['accent']); y+=38
    n=len(ch['steps']); cols=4 if n in (4,7,8) else 3
    width=(W-2*M-(cols-1)*GAP)/cols
    max_step_h=max(48+len(wrap(s['title'],width-48,27,True))*35+len(wrap(s['body'],width-48,24))*32.4+32+12 for s in ch['steps'])
    positions=[]
    for i,s in enumerate(ch['steps']):
        row=i//cols; order=i%cols; col=order if row%2==0 else cols-1-order
        x=M+col*(width+GAP); sy=y+row*(max_step_h+62)
        block(svg,x,sy,width,s['title'],s['body'],f'{i+1:02}',min_h=max_step_h)
        positions.append((x,sy,width,max_step_h))
    if not parallel:
        for i in range(n-1):
            x1,y1,w1,h1=positions[i];x2,y2,w2,h2=positions[i+1]
            if y1==y2:
                svg.path([(x1+w1,y1+h1/2),(x2,y2+h2/2)] if x2>x1 else [(x1,y1+h1/2),(x2+w2,y2+h2/2)])
            else: svg.path([(x1+w1/2,y1+h1),(x2+w2/2,y2)])
    y+=math.ceil(n/cols)*max_step_h+(math.ceil(n/cols)-1)*62+34
    pw=(W-2*M-2*GAP)/3
    heights=[]
    for p in ch['panels']:
        h=24+len(wrap(p['title'],pw-48,27,True))*35+20
        h+=sum(len(wrap(item,pw-65,23))*31.05+15 for item in p['items'])
        heights.append(h+15)
    ph=max(heights)
    for i,p in enumerate(ch['panels']):
        x=M+i*(pw+GAP);svg.rect(x,y,pw,ph,fill=C['white'])
        yy=y+23+svg.text(x+24,y+23,p['title'],pw-48,27,True,C['ink'],35)+18
        for item in p['items']:
            svg.text(x+23,yy,'•',18,23,True,C['accent'])
            yy+=svg.text(x+43,yy,item,pw-65,23)+15
        assert yy <= y+ph+1
    y+=ph+28
    if ch.get('terms'):
        y=strip(svg,y,'TERMS IN THIS IMAGE',ch['terms'],C['blue'])+20
    y=strip(svg,y,'ILLUSTRATIVE EXAMPLE',ch['example'])+20
    y=strip(svg,y,'REMAINING WORK / DECISION',ch['remaining'],C['amber'])+22
    y+=svg.text(M,y,'MENTOR DISCUSSION  '+ch['mentor_question'],W-2*M,24,True,C['ink'])+27
    svg.path([(M,y),(W-M,y)],arrow=False,color=C['line']);y+=16
    y+=svg.text(M,y,'Source: '+ch['source']+'  |  Canonical plan revision 1.1  |  6 September 2026',W-2*M,17,False,C['muted'])+28
    return svg.finish(math.ceil(y),OUT/(ch['id']+'.svg'))

def overview():
    svg=Svg('Golden Goose — overall architecture','Two entry routes share one application and a source-backed MemoryService. All product components are planned and unbuilt. The only executed evidence is an isolated storage probe.')
    svg.text(72,35,'GOLDEN GOOSE / MENTOR REVIEW / 00',1856,18,True,C['accent'])
    svg.text(72,76,'The complete architecture, at a glance',1856,44,True,C['ink'])
    svg.text(72,139,'Recall useful history → understand supported changes → apply context → inspect and control.',1856,25,False,C['body'])
    for x,w,fill,txt in [(72,568,C['panel'],'DOCUMENTED: architecture + research'),(660,566,C['blue'],'EXECUTED: isolated SQL probe, 12/12'),(1246,682,C['amber'],'NOT BUILT: application, corpus, model integration, evaluation')]:
        svg.rect(x,190,w,48,fill,fill,8);svg.text(x+14,201,txt,w-28,18,True,C['ink'])
    # Shared service is drawn first so connectors never disappear behind its background.
    svg.rect(1080,270,848,1020,C['white'],C['line'],18)
    svg.text(1110,289,'MEMORYSERVICE · one logical subsystem',788,28,True,C['ink'])
    svg.text(1110,331,'One SQLite file · trusted user scope · evidence and revision checks',788,21,False,C['muted'])
    block(svg,72,300,390,'Historical transcripts','Raw ASR + formatted output + available metadata. One paired observation. [01–02]',min_h=185)
    block(svg,540,300,460,'Validate and import','Persist permitted original sources before learning. Account for rows, revisions and jobs. [02]',min_h=185)
    block(svg,1120,390,768,'Durable source and memory store','Original revisions + supported interpretations + exact evidence + entity/time links. Source and memory indexes remain independent. [04–05, 11]',min_h=206)
    block(svg,72,670,390,'Hey Kivi request','Typed request through the final UI or intermediate CLI. Current input is immediately private to its run. [07, 12]',min_h=215)
    block(svg,540,670,460,'Request coordinator','Retrieve → interpret → commit controls → release allowed learning → continue → validate and publish. [07]',min_h=215)
    block(svg,1120,670,370,'Background learner','Use the shared model adapter to extract supported claims from permitted sources. Record outcomes off the ordinary answer path. [03, 10]',min_h=285)
    block(svg,1518,670,370,'Evidence retrieval','Search sources and memories; verify spans, combine records and report gaps. Vectors are optional; benefit unmeasured. [06]',min_h=285)
    block(svg,1120,1030,768,'Inspect, remember, correct, forget or delete','Apply current controls atomically. Every history read, source fallback, worker completion and replay must respect current exclusions. [09]',min_h=189)
    block(svg,72,1050,390,'User-visible result','Supported answer/draft, focused question, honest unknown or observed action outcome; sources available. [08, 12]',min_h=225)
    block(svg,540,1040,460,'Model and tool adapters','NVIDIA/DeepSeek interprets; code validates. Only currently authorized tools execute and produce receipts. [10]',min_h=235)
    # Essential data flow; supporting mechanisms are explained in focused plates.
    svg.path([(462,391),(540,391)])
    svg.path([(1000,391),(1050,391),(1050,455),(1120,455)])
    svg.path([(1305,596),(1305,670)],both=True)
    svg.path([(1703,596),(1703,670)])
    svg.path([(462,777),(540,777)])
    svg.path([(1000,741),(1035,741),(1035,630),(1703,630),(1703,670)])
    svg.text(1053,603,'query',125,18,True,C['accent'])
    svg.path([(1703,955),(1703,994),(1038,994),(1038,825),(1000,825)])
    svg.text(1245,967,'permitted evidence + freshness token',455,18,True,C['accent'])
    svg.path([(540,836),(510,836),(510,1163),(462,1163)])
    svg.path([(770,885),(770,1040)],both=True)
    svg.text(791,948,'proposals / observations',243,18,False,C['accent'])
    svg.path([(1000,863),(1059,863),(1059,1101),(1120,1101)])
    svg.path([(1888,1090),(1911,1090),(1911,551),(1888,551)])
    svg.text(1114,1237,'All saved knowledge and source fallback obey one permitted-text boundary.',790,21,True,C['accent'])
    y=1335
    y=strip(svg,y,'CROSS-CUTTING PROOF AND OPERATIONS','Short transactions, durable jobs, idempotency, checked freshness and bounded retries [11]. Trace actual decisions and measure the complete pipeline [13]. Ship reproducible setup, new-corpus import and reset [14].')+24
    y=strip(svg,y,'NEXT / WHAT TO ASK YOUR MENTOR','Select one worthwhile journey and its failure states. Build persistent source search and one cited-answer path with controls. Add memory complexity through measured comparisons. Review open product, model and evaluation choices in [15].',C['amber'])+26
    svg.text(M,y,'Reading order: 00 overview → 01 purpose → 02–11 mechanisms → 12 experience → 13 proof → 14 review path → 15 next decisions.',W-2*M,20,True,C['ink']);y+=50
    svg.text(M,y,'Planning visualization, not a working Kivi product. Sources: Golden Goose brief pp.2–7 and ARCHITECTURE.md revision 1.1 · 6 September 2026',W-2*M,17,False,C['muted']);y+=56
    return svg.finish(math.ceil(y),OUT/'00-overall-architecture.svg')

def main():
    chapters=[]
    for name in ['core-panels.json','memory-panels.json','backend-panels.json']:
        chapters += json.loads((HERE/name).read_text(encoding='utf-8'))
    chapters.sort(key=lambda x:x['id'])
    assert len(chapters)==15 and len({x['id'][:2] for x in chapters})==15
    for chapter in chapters:
        for step in chapter['steps']:
            step['title'] = re.sub(r'^\d+\s*·\s*', '', step['title'])
    records=[overview()]+[detailed(ch) for ch in chapters]
    (HERE/'manifest.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    package_existing(records)


def package_existing(records):
    gallery=''.join(f'<article id="p{r["file"][:2]}"><a href="images/{r["file"]}"><img src="images/{r["file"]}" alt="{escape(r["title"])}" loading="lazy"/></a><h2>{r["file"][:2]} · {escape(r["title"])}</h2><a href="images/{r["file"]}" download>Download SVG</a></article>' for r in records)
    index='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Golden Goose · mentor SVG pack</title><style>body{margin:0;background:#f7faf7;color:#193a2c;font:16px/1.6 Arial,sans-serif}header,main{max-width:1400px;margin:auto;padding:28px}h1{margin:0;font-size:30px}header p{max-width:1000px}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#245c46}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:30px}article{border-top:1px solid #ccd9cf;padding-top:20px}img{width:100%;height:auto;background:white}h2{font-size:19px;margin:8px 0}article:first-child{grid-column:1/-1}article:first-child img{max-width:1200px;display:block;margin:auto}@media(max-width:760px){main{grid-template-columns:1fr;padding:18px}header{padding:18px}article:first-child{grid-column:auto}}</style></head><body><header><h1>Golden Goose · mentor SVG pack</h1><p>One architecture overview and 15 focused diagrams. Each SVG stands alone and includes process detail, examples, safeguards, remaining work and a mentor discussion question. Start with 00; open a specific image for full-size reading.</p><p><strong>Status:</strong> reviewed plan; product implementation remains. Only the isolated storage experiment has recorded 12/12 passing checks.</p><nav><a href="Golden-Goose-Mentor-SVG-Pack.zip" download>Download complete SVG pack</a><a href="../README.md">Reading order and notes</a><a href="../BUILD_PLAN.md">Problem-statement coverage and build plan</a></nav></header><main>'''+gallery+'</main></body></html>'
    index=index.replace('</nav></header>', '</nav><nav aria-label="Diagram groups" style="margin-top:16px"><a href="#p00">Overview</a><a href="#p01">Assignment</a><a href="#p02">Memory and evidence</a><a href="#p07">Live requests and backend</a><a href="#p12">Interface, evaluation and next steps</a></nav></header>')
    (HERE/'index.html').write_text(index,encoding='utf-8',newline='\n')
    write_handoff_archive(REPO, HERE/'Golden-Goose-Mentor-SVG-Pack.zip')
    print(json.dumps({'images':len(records),'largest_height':max(x['height'] for x in records),'files':[r['file'] for r in records]},indent=2))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack-only', action='store_true', help='Refresh navigation/archive using existing SVG files without regenerating diagrams.')
    args = parser.parse_args()
    if args.pack_only:
        package_existing(json.loads((HERE/'manifest.json').read_text(encoding='utf-8')))
    else:
        main()
