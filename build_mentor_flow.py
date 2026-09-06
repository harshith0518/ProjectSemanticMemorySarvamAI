"""Build one self-contained mentor SVG. This is documentation, not product code."""
from pathlib import Path
from html import escape
import json, math
import xml.etree.ElementTree as ET
from tools.font_support import font, svg_font_family

ROOT=Path(__file__).resolve().parent
FONT_FAMILY=svg_font_family()
W,H=2760,2330
C={'ink':'#173c34','body':'#35554b','muted':'#63756e','border':'#cbd9d2',
   'live':'#2563a5','learn':'#23765a','control':'#a56b12','db':'#7060a6',
   'gray':'#f0f3f3','blue':'#edf4fc','green':'#eef7f1','amber':'#fff4db','purple':'#f2eef9'}
layers={k:[] for k in ['bg','edges','boxes','text']}
boxes=[]; bounds=[]; routes=[]

def wrap(s,width,size,bold=False):
    f=font(size,bold);out=[]
    for para in s.split('\n'):
        line=''
        for word in para.split():
            assert f.getlength(word)<=width,(word,width)
            trial=(line+' '+word).strip()
            if line and f.getlength(trial)>width:out.append(line);line=word
            else:line=trial
        out.append(line)
    return out

def text(x,y,s,width,size=24,bold=False,color=None,line_height=None):
    lines=wrap(s,width,size,bold);lead=line_height or size*1.3
    color=C.get(color,color) if color else C['body']
    p=[f'<text x="{x}" y="{y+size}" fill="{color}" font-family="{escape(FONT_FAMILY, quote=True)}" font-size="{size}" font-weight="{700 if bold else 400}">']
    for i,line in enumerate(lines):p.append(f'<tspan x="{x}" dy="{0 if i==0 else lead}">{escape(line)}</tspan>')
    p.append('</text>');layers['text'].append(''.join(p))
    h=len(lines)*lead; bounds.append((x,y,x+width,y+h,s[:75]))
    return h

def rect(x,y,w,h,fill='white',stroke='border',layer='boxes',r=16):
    fill=C.get(fill,fill);stroke=C.get(stroke,stroke)
    layers[layer].append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

def card(id,x,y,w,h,title,body,fill='white',size=24):
    rect(x,y,w,h,fill)
    th=text(x+23,y+17,title,w-46,25,True,'ink')
    by=y+17+th+8;bh=text(x+23,by,body,w-46,size)
    assert by+bh<=y+h-12,(id,title,by+bh,y+h)
    boxes.append({'id':id,'x':x,'y':y,'w':w,'h':h})
    return boxes[-1]

def group(x,y,w,h,fill,title,sub=None,titlew=None):
    rect(x,y,w,h,fill,layer='bg',r=22)
    text(x+28,y+20,title,titlew or w-56,33,True,'ink')
    if sub:text(x+28,y+68,sub,titlew or w-56,22,False,'muted')

def path(id,pts,color='live',both=False,dashed=False):
    d='M '+' L '.join(f'{x},{y}' for x,y in pts)
    marker='small-'+color if '-step-' in id else color
    attr=f'marker-end="url(#{marker})"'
    if both:attr+=f' marker-start="url(#{color})"'
    if dashed:attr+=' stroke-dasharray="10 7"'
    # A white underlay separates crossing arrows; crossings are not junctions.
    layers['edges'].append(f'<path d="{d}" fill="none" stroke="white" stroke-width="8" stroke-linejoin="round"/>')
    layers['edges'].append(f'<path id="{id}" d="{d}" fill="none" stroke="{C[color]}" stroke-width="2.8" stroke-linejoin="round" {attr}/>')
    routes.append({'id':id,'points':pts,'kind':color,'both':both,'background':dashed})

def label(x,y,s,w,color='live',size=21):
    height=len(wrap(s,w,size,True))*size*1.3
    rect(x-7,y-3,w+14,height+6,'white','white',layer='text',r=4)
    text(x,y,s,w,size,True,color)

def steps(x,y,w,items,color):
    for i,(title,body) in enumerate(items):
        card(f'{color}-{i+1}',x,y+i*140,w,128,f'{i+1}  {title}',body,'white',21)
        if i<len(items)-1:path(f'{color}-step-{i+1}',[(x+w/2,y+i*140+128),(x+w/2,y+(i+1)*140)],color)

def main():
    layers['bg'].append(f'<rect width="{W}" height="{H}" fill="#fcfdfb"/>')
    text(60,35,'Kivi → useful history → trustworthy assistance',2640,51,True,'ink')
    text(60,104,'One product story: dictate a trip budget, use it later, change it, inspect it and forget it.',2640,27)
    text(60,157,'PROPOSED ARCHITECTURE  •  App unbuilt  •  Only the isolated SQLite probe has passed 12/12 checks',2640,21,True,'muted')

    group(60,225,850,475,'gray','A  REGULAR KIVI','Write what the person intends; existing product context.')
    card('dictate',88,345,238,156,'Dictate','“Jaipur trip:\ntotal hotel budget\nINR 6,000.”','white',21)
    card('format',362,345,250,156,'Format faithfully','Words, spelling\nand writing style.','white',23)
    card('destination',648,345,232,156,'Write text','To the intended\ndestination.','white',23)
    path('dictate-format',[(326,410),(362,410)],'muted')
    path('format-output',[(612,410),(648,410)],'muted')
    card('paired-history',166,545,650,132,'Paired historical record','Raw ASR + formatted text + available metadata. Our demo imports / replays these records.','white',23)
    path('paired-copy',[(487,501),(487,545)],'muted',dashed=True)
    label(505,509,'capture / replay',275,'muted',19)

    group(970,225,1730,475,'blue','B  HEY KIVI','Help with the current request, using relevant permitted history.')
    card('request',1000,345,325,175,'Ask for help','“Jaipur checklist, using our budget.”\nTyped request.','white',23)
    card('coordinator',1400,335,600,315,'Request coordinator · Python',
         'Accept private input; hold its learning job.\n① Recall evidence → model proposal.\n② Validate + commit proposed controls.\n③ Release only permitted learning.\n④ Continue → check freshness → persist.','white',25)
    card('answer',2090,345,565,165,'Useful, inspectable result','Answer, draft, focused question or honest unknown. Apply current instructions; show supporting sources.','white',23)
    card('model',1010,555,340,132,'DeepSeek · NVIDIA','HTTPX: bounded calls.\nProposes meaning.','purple',22)
    card('tool',2100,535,545,140,'Optional authorized tool','Validate authority + target. Observe result; reconcile unknown outcomes.','purple',22)
    path('request-coordinator',[(1325,430),(1400,430)],'live')
    path('publish-result',[(2000,408),(2090,408)],'live')
    label(2010,368,'publish',76,'live',18)
    path('model-roundtrip',[(1350,615),(1400,615)],'live',both=True)
    path('tool-roundtrip',[(2000,594),(2100,594)],'live',both=True)
    label(2008,520,'action ↔\noutcome',88,'live',17)

    # The service is one logical subsystem. All columns share the DB below.
    group(60,900,2640,800,'green','C  SEMANTIC MEMORY · MemoryService',
          'Application rules + durable understanding. All routes use the same permission, source and revision checks.',titlew=795)
    for x in [100,1000,1900]:rect(x,1030,760,578,'white',layer='bg')
    text(126,1050,'CREATE / LEARN',700,29,True,'learn')
    text(1026,1050,'READ / RECALL',700,29,True,'live')
    text(1926,1050,'UPDATE / FORGET / INSPECT',700,29,True,'control')
    steps(130,1115,700,[
        ('Persist evidence first','Validate import; save exact source revision + durable job. Permitted source search is independent of extraction.'),
        ('Propose useful small claims','Background worker uses the shared model. Keep speaker, subject, scope, time, negation and exact support.'),
        ('Validate and admit','Add / revise / link / no-op / preserve conflict / reject. Commit accepted memory, evidence and index jobs together.')
    ],'learn')
    steps(1030,1115,700,[
        ('Define the permitted question','Check trusted user, scope, relevant time and current exclusions. Include the current input privately.'),
        ('Search originals + memories','FTS5 keywords first. Optional vectors help with meaning; supported relationships can connect records.'),
        ('Return a supported evidence bundle','Inspect exact spans; combine and deduplicate. Include sources, conflicts, coverage and a freshness token.')
    ],'live')
    steps(1930,1115,700,[
        ('Resolve intent and exact target','Remember / correct / change / forget / delete source. Check scope, time and expected version; clarify ambiguity.'),
        ('Commit compatible changes together','Knowledge, exclusions, permitted text, affected indexes / links, revision and actual receipt change atomically.'),
        ('Enforce every future use','Suppress affected derivatives, jobs and replay; rebuild from surviving evidence. Source deletion has a separate boundary.')
    ],'control')
    text(130,1541,'Routine learning is background work.\nExplicit “remember” must commit before “saved”.',700,22,True,'learn')
    text(1030,1541,'Source fallback covers missed memories.\nFull lists and counts need completeness checks.',700,22,True,'live')
    text(1930,1541,'A real-world change preserves earlier history.\nForget also blocks known supporting spans.',700,22,True,'control')
    text(100,1625,'MEMORY RECORD = attributed claim + subject / scope + time + exact source evidence + status / revision.\nExample: Jaipur trip · total hotel budget · 6000 INR · original supporting phrase. Twelve categories are labels on shared records.',2560,23,True,'ink')

    # External routes are routed through empty gutters. Arrow labels name both directions.
    path('history-import',[(480,677),(480,783),(31,783),(31,1175),(130,1175)],'learn')
    label(65,740,'Import permitted history',380,'learn',23)
    path('recall-request',[(1490,650),(1490,817),(1300,817),(1300,1030)],'live')
    label(1195,837,'① retrieval request ↓',330,'live',22)
    path('evidence-return',[(1570,1030),(1570,763),(1750,763),(1750,650)],'live')
    label(1585,785,'↑ evidence + versions',315,'live',21)
    path('control-roundtrip',[(1920,650),(1920,813),(2185,813),(2185,1030)],'control',both=True)
    label(2210,799,'② controls ↓ / receipts ↑',420,'control',22)
    path('release-learning',[(1430,650),(1430,723),(950,723),(950,1345),(830,1345)],'learn',dashed=True)
    label(978,727,'③ after controls: release only\nsurviving text; otherwise hold',480,'learn',21)
    path('learner-model',[(830,1295),(912,1295),(912,621),(1010,621)],'learn',both=True,dashed=True)
    label(770,865,'background\nmodel call',145,'learn',19)

    # All three round trips terminate at the same storage boundary.
    path('learn-store',[(480,1700),(480,1780)],'db',both=True)
    path('recall-store',[(1380,1700),(1380,1780)],'db',both=True)
    path('control-store',[(2280,1700),(2280,1780)],'db',both=True)
    label(80,1730,'Read sources ↔ commit claims + jobs',800,'db',22)
    label(990,1730,'Query sources + memories + indexes',800,'db',22)
    label(1875,1730,'Read targets ↔ commit controls + receipt',800,'db',22)
    group(60,1780,2640,282,'amber','D  ONE REGULAR PRODUCT DATABASE · SQLite',
          'Shared storage and transaction boundary. MemoryService gives these records their learning, retrieval and control behavior.')
    card('db-general',100,1900,810,134,'General product + source data','Original records / revisions · requests / conversations\nJobs / runs / operation outcomes / control receipts','white',23)
    card('db-memory',970,1900,820,134,'Semantic-memory data','Accepted claims / versions · evidence / dependencies\nSubjects / scope / time · supported aliases / relationships','white',23)
    card('db-indexes',1850,1900,810,134,'Rebuildable search representations','FTS5 source + memory indexes · optional local vectors\nVectors locate candidates; evidence supports answers.','white',23)

    # Short supporting notes keep the technology and trust story in the same image.
    text(70,2090,'WHY THIS STACK',750,22,True,'ink')
    text(70,2125,'Python: explicit request order. Pydantic: data-shape checks.\nSQLite: related changes commit together. HTTPX: bounded model calls.',840,21)
    text(970,2090,'WHY THIS STAYS CORRECT',840,22,True,'ink')
    text(970,2125,'Exact evidence; qualified meaning; one exclusion boundary.\nShort transactions, repeat-safe keys, stale-worker rejection and fresh publication.',850,21)
    text(1870,2090,'WHAT REMAINS TO PROVE',800,22,True,'ink')
    text(1870,2125,'Build the real UI + backend, corpus and model integration.\nMeasure quality, latency, failures and cost; vectors remain optional.',800,21)
    rect(60,2210,2640,68,'blue')
    text(85,2226,'ONE EXAMPLE: dictate INR 6,000 → learn trip-scoped budget → draft with evidence → change to INR 8,000 → inspect → forget across all retrieval routes.',2590,23,True,'ink')
    text(60,2290,'Arrow colors: blue = live request / evidence; green = learning (dashed = background); amber = controls; purple = shared DB access.  Sources: ARCHITECTURE.md v1.1 §§0–12; Golden Goose brief.  6 Sep 2026.',2640,17,False,'muted')

    for x,y,x2,y2,desc in bounds:assert 0<=x<x2<=W and 0<=y<y2<=H,(desc,x,y,x2,y2)
    defs='<defs>'+''.join(f'<marker id="{prefix}{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{C[k]}"/></marker>' for prefix,size in [('',8),('small-',4)] for k in ['live','learn','control','db','muted'])+'</defs>'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">Kivi: complete memory architecture and flow</title><desc id="desc">Regular dictation provides history. Hey Kivi coordinates private input, recall, model proposals, controls and checked results. MemoryService learns, retrieves and controls evidence-backed knowledge over the same SQLite database as ordinary application data. All product components are planned.</desc>{defs}'+''.join(''.join(layers[k]) for k in ['bg','edges','boxes','text'])+'</svg>'
    ET.fromstring(svg)
    target=ROOT/'KIVI_COMPLETE_FLOW.svg';target.write_text(svg,encoding='utf-8',newline='\n')
    report={'svg':target.name,'width':W,'height':H,'text_blocks':len(bounds),'process_boxes':len(boxes),'directed_routes':len(routes),'xml':'pass','text_containment':'pass','external_assets':False,'routes':routes}
    (ROOT/'KIVI_COMPLETE_FLOW.validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k!='routes'},indent=2))

if __name__=='__main__':main()
