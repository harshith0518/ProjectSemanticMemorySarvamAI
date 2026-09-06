"""Create editable Excalidraw scenes and matching SVG previews. Documentation only."""
from pathlib import Path
from html import escape
import json, math, random, re, sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from tools.font_support import font, svg_font_family

FONT_FAMILY = svg_font_family()
ROOT.mkdir(exist_ok=True)
PREVIEW = ROOT / 'previews'
PREVIEW.mkdir(exist_ok=True)
COL = dict(ink='#203c36', muted='#566b64', line='#647d73', green='#e3f1e8', blue='#e4eff9',
           amber='#fff1cc', purple='#eee8f6', gray='#f0f1f2', white='#ffffff')
RNG = random.Random(6001)
ELEMENTS, FRAMES, AUDIT = [], [], []
CURRENT = None

def wrapped(s, width, size=22):
    f = font(size)
    lines=[]
    for para in s.split('\n'):
        line=''
        for word in para.split():
            assert f.getlength(word) <= width, (word, width)
            trial=(line+' '+word).strip()
            if line and f.getlength(trial)>width:
                lines.append(line); line=word
            else: line=trial
        lines.append(line)
    return '\n'.join(lines)

def base(kind,x,y,w,h,id=None,fill='transparent',stroke=None,group=None):
    e=dict(id=id or f'el-{len(ELEMENTS):04}', type=kind, x=x, y=y, width=w, height=h,
           angle=0, strokeColor=stroke or COL['ink'], backgroundColor=fill,
           fillStyle='solid', strokeWidth=1.6, strokeStyle='solid', roughness=0,
           opacity=100, groupIds=[group] if group else [], frameId=CURRENT,
           roundness={'type':3} if kind=='rectangle' else None,
           seed=RNG.randrange(1,2**30), version=1, versionNonce=RNG.randrange(1,2**30),
           isDeleted=False, boundElements=[], updated=1788652800000, link=None, locked=False)
    ELEMENTS.append(e)
    return e

def text(x,y,s,width,size=22,color=None,group=None,container=None):
    content=wrapped(s,width,size)
    h=len(content.split('\n'))*size*1.25
    e=base('text',x,y,width,h,stroke=color or COL['ink'],group=group)
    e.update(text=content,originalText=content,fontSize=size,fontFamily=2,lineHeight=1.25,
             textAlign='left',verticalAlign='top',containerId=container,autoResize=True)
    if container:
        next(v for v in ELEMENTS if v['id']==container)['boundElements'].append({'id':e['id'],'type':'text'})
    return e

def card(x,y,w,h,title,body='',fill='green',size=21,tag=None):
    group=f'g-{len(ELEMENTS)}'
    r=base('rectangle',x,y,w,h,fill=COL.get(fill,fill),stroke=COL['line'],group=group)
    title_e=text(x+18,y+15,title,w-36,22,group=group)
    title_e['customData']={'role':'card-title'}
    body_y=y+15+title_e['height']+7
    if body:
        t=text(x+18,body_y,body,w-36,size,group=group)
        assert t['y']+t['height']<=y+h-10, (title,body,t['height'],h)
    if tag:r['customData']={'tag':tag}
    AUDIT.append({'rect':r['id'],'title':title})
    return r

def connector(points,start=None,end=None,both=False,dashed=False,color=None):
    x,y=points[0]
    rel=[[px-x,py-y] for px,py in points]
    w=max(p[0] for p in rel)-min(p[0] for p in rel)
    h=max(p[1] for p in rel)-min(p[1] for p in rel)
    e=base('arrow',x,y,w,h,stroke=color or COL['line'])
    e.update(points=rel,lastCommittedPoint=None,startBinding=None,endBinding=None,
             startArrowhead='arrow' if both else None,endArrowhead='arrow',elbowed=False)
    if dashed:e['strokeStyle']='dashed'
    for key,target in [('startBinding',start),('endBinding',end)]:
        if target:
            e[key]={'elementId':target['id'],'focus':0,'gap':8}
            target['boundElements'].append({'id':e['id'],'type':'arrow'})
    return e

def line(x,y,w):
    e=base('line',x,y,w,0,stroke='#cad7d1')
    e.update(points=[[0,0],[w,0]],lastCommittedPoint=None,startBinding=None,endBinding=None,
             startArrowhead=None,endArrowhead=None)

def frame(num,title,x,y,h,subtitle):
    global CURRENT
    CURRENT=None
    f=base('frame',x,y,1600,h,id=f'frame-{num}')
    f.update(name=f'{num} · {title}',strokeColor='#c7d5cf',roundness=None)
    CURRENT=f['id'];FRAMES.append(f)
    text(x+36,y+32,f'{num}   {title}',1528,36)
    text(x+36,y+88,subtitle,1528,21,COL['muted'])
    text(x+36,y+126,'PLAN / NOT IMPLEMENTED   •   Canonical architecture v1.1   •   6 September 2026',1528,16,COL['muted'])
    return x,y

def note(x,y,w,s,fill='amber',h=96):
    r=base('rectangle',x,y,w,h,fill=COL[fill],stroke='#d0d8d0')
    t=text(x+18,y+16,s,w-36,21)
    assert t['height']<=h-28,(s,t['height'],h)
    return r

def footer(x,y,s):text(x+36,y,s,1528,16,COL['muted'])

def overview():
    x,y=frame('00','Two ways to use Kivi. One memory system.',0,0,1060,
        'Regular Kivi writes what I say. Hey Kivi uses relevant history to help with what I ask.')
    text(36,179,'REGULAR KIVI / existing product context',930,20,COL['muted'])
    a=card(36,219,255,127,'Dictate','“Jaipur hotel budget:\nINR 6,000.”','gray',20)
    b=card(348,219,284,127,'Format faithfully','Recognition + vocabulary / style personalization.','gray',20)
    c=card(690,219,250,127,'Write text','Intended text in the intended destination.','gray',20)
    d=card(1020,219,540,135,'Our demo: import paired history','Raw ASR + formatted text + metadata.\nValidated through MemoryService.\nPaired versions are one observation.','blue',20)
    connector([(299,282),(340,282)],a,b)
    connector([(640,282),(682,282)],b,c)
    connector([(948,282),(1012,282)],c,d,dashed=True)
    text(38,366,'Native ASR and phonetic learning are outside this assignment. Historical text never grants fresh tool authority.',1480,19,COL['muted'])
    text(36,416,'HEY KIVI / the memory-powered experience to build',1490,20,COL['muted'])
    q=card(36,456,255,136,'Ask for help','“Make a Jaipur checklist using our budget.”\nTyped input is enough.','blue',19)
    co=card(348,456,325,136,'Request coordinator','Recall → interpret → commit controls → continue.','blue',20)
    mo=card(739,456,326,136,'Model proposal','DeepSeek: answer, retrieve, clarify or propose controls / tools.','purple',20)
    out=card(1130,456,430,136,'Useful result','Answer or draft; actual tool outcome. Current instructions, evidence and visible uncertainty.','blue',20)
    connector([(299,524),(340,524)],q,co)
    connector([(681,524),(731,524)],co,mo,both=True)
    connector([(610,600),(610,639),(1345,639),(1345,600)],co,out)
    text(719,645,'Code checks freshness before publishing',620,17,COL['muted'])
    worker=card(36,718,255,185,'Background learner','Shared model proposes supported claims. Ordinary answers do not wait.','green',20)
    mem=card(348,718,717,185,'MemoryService = behavior + saved understanding','Learn / recall / inspect / remember / correct / forget.\nApplies evidence, scope, time and permission rules.\nSemantic memory is a logical subsystem in the application.','green',22)
    db=card(1130,718,430,185,'ONE SQLite database','Original history + application state\nAccepted memories + evidence\nRebuildable keyword/vector indexes','amber',22)
    connector([(440,600),(440,710)],co,mem,both=True)
    text(455,671,'recall / controls',210,18,COL['muted'])
    connector([(299,810),(340,810)],worker,mem,both=True)
    connector([(1073,810),(1122,810)],mem,db,both=True)
    connector([(1540,362),(1540,399),(1581,399),(1581,780),(1568,780)],d,db)
    note(36,934,1524,'Core idea: save the evidence; learn qualified meaning; retrieve only what helps; let the user inspect and change it.\nOnly the isolated SQLite probe has passed 12/12 checks. The product, corpus, model integration and evaluation remain unbuilt.',h=93)
    footer(0,1034,'Discuss 00 first. Zoom to 01 storage, 02 CRUD, 03 safeguards, 04 technology rationale and 05 next work.')

def anatomy():
    x,y=frame('01','Semantic memory inside the general database',1780,0,1100,
        'The database holds durable records. MemoryService decides what they mean, what is allowed and how to use them.')
    card(x+36, y+188, 480, 210,'A · General app / source records',
         'Exact source revisions and metadata\nRequests, conversation, runs, outcomes\nJobs, operation keys and control receipts\nOriginal history survives skipped extraction.','amber',21)
    card(x+560,y+188,480,210,'B · Accepted memory records',
         'Attributed assertions + earlier revisions\nExact evidence links and dependencies\nSubjects, scope, time and lifecycle\nSupported entities / aliases / relationships','green',21)
    card(x+1084,y+188,480,210,'C · Search representations',
         'FTS5 source and memory documents\nOptional vectors of permitted text\nSupported relationship projections\nRebuildable; not the only saved knowledge.','blue',21)
    text(x+36,y+427,'All three groups share ONE SQLite file and ONE permission boundary. No required graph server or separate vector database.',1520,22)
    line(x+36,y+477,1528)
    text(x+36,y+501,'WORKED EXAMPLE / one source becomes a qualified claim',1500,24)
    source=card(x+36,y+555,435,250,'Exact original source','“For the Jaipur trip, our total hotel budget is INR 6,000.”\n\nKeep the original field, source ID, revision and exact character span.','amber',23)
    claim=card(x+542,y+555,540,250,'Accepted assertion','Subject / scope: that Jaipur trip\nPredicate: total hotel budget\nValue / unit: 6000 / INR\nCategory: constraint; form: semantic\nSpeaker, time, polarity, status, revision\nEvidence: original source + exact span','green',22)
    query=card(x+1153,y+555,410,250,'What Hey Kivi can do','Recall this trip’s budget.\nApply it to a checklist.\nShow the original evidence.\nLater change or forget it.\n\nIt does not imply a nightly budget.','blue',22)
    connector([(x+479,y+680),(x+534,y+680)],source,claim)
    connector([(x+1090,y+680),(x+1145,y+680)],claim,query)
    note(x+36,y+838,1528,'Memory anatomy: who said it + who it concerns + claim + scope + time + evidence + version.\nA plan stays a plan; a belief stays attributed; unknown identity or time stays unknown. Current and historical values stay distinguishable.',h=112)
    text(x+36,y+977,'12 labels organize shared records: entities, relationships, preferences, constraints, routines, goals, plans/tasks, decisions, progress/issues, beliefs/ideas, vocabulary, resources. Labels are not isolated search routes.',1528,20)
    footer(x,y+1071,'Source: ARCHITECTURE.md §§1–5, 9–10. Accepted interpretations are durable; indexes and supported relationship projections can be rebuilt.')

def crud():
    x,y=frame('02','Memory CRUD: what actually happens underneath',0,1260,1340,
        'CRUD = create, read, update, delete. Language requests become validated operations, evidence changes and real receipts.')
    lanes=[
      ('C · CREATE','Learn or explicitly remember','green',[
        ('Keep the source','Save exact record + revision; enqueue learning durably.'),
        ('Propose small claims','Model proposes attribution, meaning and evidence. Worker handles routine learning.'),
        ('Validate + decide','Check support and scope. Add, revise, link, no-op, preserve conflict or reject.'),
        ('Commit together','Memory + evidence + decisions + queued indexes. Acknowledge explicit remember only after commit.')],
       'Routine learning is background work. An explicit “remember” is a foreground control; skipped extraction still leaves source search.'),
      ('R · READ','Recall for a real task','blue',[
        ('Apply eligibility','Trusted user, current scope/time, visibility and exclusions govern every route.'),
        ('Find candidates','Keyword sources + memories; optional vectors and supported links add candidates.'),
        ('Inspect + assemble','Read original spans. Deduplicate; pack decisive evidence, conflicts and coverage.'),
        ('Answer + recheck','Use current request + evidence. Refresh stale knowledge before publishing.')],
       'Complete lists, counts and change histories need enumeration plus source fallback. A nearest-match list cannot prove completeness.'),
      ('U · UPDATE','Correction versus change','purple',[
        ('Resolve the target','Identify subject, property, scope/time and expected revision. Clarify meaningful ambiguity.'),
        ('Preserve meaning','“Now 8,000” = change. “I meant 8,000” = correction of an earlier mistake.'),
        ('Append + invalidate','Save revised interpretation and evidence; update head; invalidate dependent links/indexes.'),
        ('Commit + refresh','Record receipt + knowledge revision. Future reads use the qualified updated state.')],
       'A real-world change preserves the old INR 6,000 historically. Latest import time and name similarity never justify overwrite.'),
      ('D · DELETE','Forget or delete source','amber',[
        ('Resolve the boundary','Choose information and known supporting spans. Source deletion is a separate explicit choice.'),
        ('Stage the changes','Resolve exclusions, permitted text and requested in-app source removal; identify affected derivatives.'),
        ('Commit + invalidate','Commit exclusions, affected derivatives, revision and receipt together. Queue rebuilding from surviving evidence.'),
        ('Enforce on all reads','Source fallback, worker completion, inspection and replay recheck current exclusions.')],
       'Forget can retain original history while blocking use. Delete-source removes selected in-app originals; exports/backups/provider retention are separate.')
    ]
    for i,(verb,sub,fill,steps,explain) in enumerate(lanes):
        sy=y+190+i*275
        text(x+36,sy+15,verb,190,27)
        text(x+36,sy+59,sub,190,21,COL['muted'])
        nodes=[]
        for j,(title,body) in enumerate(steps):
            xx=x+253+j*328
            nodes.append(card(xx,sy,300,200,f'{j+1}. {title}',body,fill,20))
        for j in range(3):
            a,b=nodes[j:j+2]
            connector([(a['x']+a['width']+5,sy+84),(b['x']-5,sy+84)],a,b)
        text(x+253,sy+215,explain,1284,18,COL['muted'])
    footer(x,y+1311,'Source: ARCHITECTURE.md §§4–9. Model proposals cannot grant ownership, force unsupported changes, invent receipts or bypass controls.')

def safeguards():
    x,y=frame('03','Why the design should stay correct',1780,1260,1240,
        'These are proposed engineering guarantees to implement and test. Each exists because a plausible shortcut fails.')
    data=[
      ('1 · Evidence before abstraction','Problem: extraction misses useful history.\nApproach: save originals; search permitted sources independently; preserve exact support.\nTest: an unclassified record still answers a supported question.'),
      ('2 · Qualified, versioned meaning','Problem: wrong person, stale value or invented fact.\nApproach: attribution + scope + time + modality + evidence; preserve conflicts and supported history.\nTest: “might visit” never becomes “visited”.'),
      ('3 · One permitted-text boundary','Problem: forgotten meaning returns through fallback or vectors.\nApproach: all reads and stale completions apply current exclusions and span mappings.\nTest: source search and replay cannot recover it.'),
      ('4 · Hold live input before learning','Problem: “forget my INR 6,000 budget” relearns the budget.\nApproach: private current source + held job; resolve controls; release surviving text only.\nTest: no new eligible copy from the forget request.'),
      ('5 · Atomic + repeat-safe operations','Problem: partial writes or retries duplicate state.\nApproach: short transactions, stable operation keys, expected revisions and fenced worker attempts.\nTest: stale worker cannot replace a newer correction.'),
      ('6 · Fresh answers + real tool outcomes','Problem: correction races an answer, or a timeout hides an executed effect.\nApproach: recheck publication; code verifies authority and receipts; reconcile unknown effects.\nTest: no false “saved” or duplicate blind retry.')
    ]
    for i,(title,body) in enumerate(data):
        xx=x+36+(i%3)*518; yy=y+191+(i//3)*317
        card(xx,yy,488,286,title,body,'green' if i<3 else 'blue',21)
    note(x+36,y+846,1528,'LIVE ORDER: private input + held job → retrieve → model proposal → commit controls → release only allowed learning → continue → check freshness + save answer → deliver / current-eligible replay.',h=94)
    text(x+36,y+966,'Freshness token = the knowledge versions used for an answer. Any meaning-changing write requires refresh. A narrow service-only exception covers publishing unchanged, already-seen input; it is not a general bypass.',1528,21)
    text(x+36,y+1043,'Operation key = one logical request. Same key + same payload reuses its receipt; changed payload conflicts. Fencing token = attempt identity that blocks a replaced worker. Model/tool calls stay outside database transactions.',1528,21)
    note(x+36,y+1120,1528,'Limits and uncertainty: bounded model/read/effect attempts; ask a focused question for a material gap; otherwise give supported partial help. Previously delivered bytes cannot be recalled.',h=84)
    footer(x,y+1212,'Source: ARCHITECTURE.md §§5–8, 10–11. These guarantees still need actual backend, concurrency, recovery and model tests.')

def tech():
    x,y=frame('04','Technology choices: job, reason and tradeoff',0,2700,1580,
        'Keep one small local application; add complexity only when it improves the chosen task in measured comparisons.')
    rows=json.loads((ROOT/'technology-content.json').read_text(encoding='utf-8'))
    sy=y+244
    for i,row in enumerate(rows):
        # Compact table gives a comparison rather than thirteen disconnected diagrams.
        statuses=['Baseline','Baseline; probe only','Baseline','Baseline','Baseline','User choice; endpoint open','Optional; unmeasured','Baseline; expansion optional','Baseline','CLI milestone','Required; undecided','Local first; MCP deferred','Deferred']
        status=statuses[i]+'\n'+row['limit']
        rh=max(len(wrapped(s,w,sz).split('\n'))*sz*1.25 for s,w,sz in [(row['technology'],300,21),(row['use'],350,20),(row['why'],380,20),(status,390,18)])+24
        if i%2==0:base('rectangle',x+36,sy-9,1528,rh-5,fill='#f0f5f2',stroke='#f0f5f2')
        text(x+49,sy,row['technology'],300,21)
        text(x+368,sy,row['use'],350,20)
        text(x+742,sy,row['why'],380,20)
        text(x+1150,sy,status,390,18,COL['muted'])
        sy+=rh
    for xx,w,label in [(49,300,'TECHNOLOGY'),(368,350,'JOB IN THIS PRODUCT'),(742,380,'WHY THIS STARTING CHOICE'),(1150,390,'STATUS / TRADEOFF')]:
        text(x+xx,y+187,label,w,19)
    line(x+36,y+224,1528)
    note(x+36,sy+12,1528,'Decision rule: prove a cited answer from persisted sources first. Compare full permitted history, keyword sources, hybrid sources and typed memories before making optional retrieval complexity the default.',h=84)
    footer(x,sy+113,'Source: ARCHITECTURE.md §2. Reasons are design rationale, not benchmark results. Exact dependency/model versions still need pinning.')
    FRAMES[-1]['height']=sy+152-y

def next_work():
    x,y=frame('05','What we need next — and what to ask a mentor',1780,2700,1150,
        'The next useful result is one real cited answer from persisted history, with inspection and working controls.')
    card(x+36,y+190,480,226,'Exists today','Reviewed architecture + research\n16 detailed SVG reference diagrams\nIsolated SQLite contract probe: 12/12\n\nThat probe does not establish product semantics, real concurrency or speed.','gray',22)
    card(x+560,y+190,480,226,'Must build','Importer + migrations + source search\nMemoryService, worker, controls\nModel adapter + coordinator + traces\nUsable interface and evidence view\nCorpus, evaluation and tested runbook','green',22)
    card(x+1084,y+190,480,226,'Still a decision','First recurring user journey\nAdmission / sensitive-data policy\nUI + application adapter framework\nExact DeepSeek deployment\nEmbedding default and quality gates','amber',22)
    text(x+36,y+446,'BUILD ORDER / each milestone produces inspectable evidence',1510,24)
    labels=[('1 · Define behavior','One useful journey plus ambiguous, corrected, forgotten and failed cases.'),
            ('2 · Source-first core','Persist, import, inspect and keyword-search. Prove restart and reimport.'),
            ('3 · Real answer + controls','Connect model; cite sources; correct/forget; show actual saved status.'),
            ('4 · Add measured memory','Selective extraction and qualified updates; compare optional vector recall.'),
            ('5 · Finish and verify','Final UI; justified tool; ~500 records; frozen evaluation; clean-checkout review.')]
    nodes=[]
    for i,(t,b) in enumerate(labels):nodes.append(card(x+36+i*311,y+496,285,200,t,b,'blue',20))
    for a,b in zip(nodes,nodes[1:]):connector([(a['x']+a['width']+4,y+588),(b['x']-4,y+588)],a,b)
    note(x+36,y+713,1528,'MENTOR DECISIONS\n1. Which recurring task is valuable enough to lead?  2. What should be learned, ignored or clarified?\n3. Which errors would break trust?  4. What measured gain justifies vectors or richer relationship retrieval?',h=130)
    card(x+36,y+874,746,180,'Proof the assignment expects','Approximately 500 paired history records; unfamiliar-corpus import; sources, failures, quality, latency, growth and cost; final normal-user UI. A CLI is an intermediate step.','green',21)
    card(x+817,y+874,747,180,'Reproducible submission','README + exact RUN.md; schema/migrations/seed; generated results; tested setup/import/query/inspect/evaluate/reset; repository URL + final commit SHA.','green',21)
    text(x+36,y+1080,'Part One position/vision must be independently formed and written by the applicant before Part Two. This AI-assisted board is technical planning material.',1528,18,COL['muted'])
    footer(x,y+1123,'Source: assignment brief pp.2–7; ARCHITECTURE.md §§0.3, 12, 14–16. Examples are illustrative, not a finalized product narrative.')

def scene(elements,overview_only=False):
    return {'type':'excalidraw','version':2,'source':'https://excalidraw.com','elements':elements,
        'appState':{'viewBackgroundColor':'#ffffff','gridSize':None,'theme':'light','zoom':{'value':0.65},
                    'scrollX':35,'scrollY':35,'currentItemFontFamily':2,'frameRendering':{'enabled':True,'clip':True,'name':True,'outline':True}},'files':{}}

def svg_preview(frame):
    x,y,w,h=[frame[k] for k in ('x','y','width','height')]
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}"><title>{escape(frame["name"])}</title><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#647d73"/></marker></defs>']
    children=[e for e in ELEMENTS if e['frameId']==frame['id']]
    for e in children:
        t=e['type'];cx=e['x'];cy=e['y']
        if t=='rectangle':p.append(f'<rect x="{cx}" y="{cy}" width="{e["width"]}" height="{e["height"]}" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" rx="12"/>')
        elif t=='text':
            size=e['fontSize']
            p.append(f'<text x="{cx}" y="{cy+size}" fill="{e["strokeColor"]}" font-family="{escape(FONT_FAMILY, quote=True)}" font-size="{size}">')
            for i,s in enumerate(e['text'].split('\n')):p.append(f'<tspan x="{cx}" dy="{0 if i==0 else size*1.25}">{escape(s)}</tspan>')
            p.append('</text>')
        elif t in ('arrow','line'):
            pts=' '.join(f'{cx+px},{cy+py}' for px,py in e['points'])
            attrs='marker-end="url(#a)"' if t=='arrow' else ''
            if e.get('startArrowhead'):attrs+=' marker-start="url(#a)"'
            if e['strokeStyle']=='dashed':attrs+=' stroke-dasharray="7 5"'
            p.append(f'<polyline points="{pts}" fill="none" stroke="{e["strokeColor"]}" stroke-width="1.6" {attrs}/>')
    p.append('</svg>')
    name=frame['id'].replace('frame-','')+'-'+re.sub('[^a-z0-9]+','-',frame['name'].split('·')[1].strip().lower()).strip('-')+'.svg'
    (PREVIEW/name).write_text(''.join(p),encoding='utf-8',newline='\n')
    return name

def main():
    overview();anatomy();crud();safeguards();tech();next_work()
    for e in ELEMENTS:
        if not e['frameId']:continue
        f=next(f for f in FRAMES if f['id']==e['frameId'])
        if e['type'] in ('rectangle','text'):
            assert e['x']>=f['x'] and e['y']>=f['y'] and e['x']+e['width']<=f['x']+f['width'] and e['y']+e['height']<=f['y']+f['height'],(e['id'],e.get('text'),f['id'])
    data=scene(ELEMENTS)
    for name in ['Golden-Goose-Mentor-Board.excalidraw','Golden-Goose-Mentor-Board.json']:
        (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    one=[e for e in ELEMENTS if e['id']=='frame-00' or e['frameId']=='frame-00']
    (ROOT/'Golden-Goose-Compact-Overview.excalidraw').write_text(json.dumps(scene(one,True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    previews=[{'id':f['id'],'name':f['name'],'file':svg_preview(f)} for f in FRAMES]
    (ROOT/'manifest.json').write_text(json.dumps({'elements':len(ELEMENTS),'frames':previews,'native_images':0},indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'elements':len(ELEMENTS),'frames':len(FRAMES),'previews':[p['file'] for p in previews]},indent=2))

if __name__=='__main__':main()
