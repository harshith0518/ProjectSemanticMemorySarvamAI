"""Check exported drawing structure and package portable deliverables."""
from pathlib import Path
from collections import Counter
import json, math, re, sys, zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

root=Path(__file__).resolve().parent
repo=root.parent
sys.path.insert(0, str(repo))
from tools.package_support import write_handoff_archive
report={}
for name,expected_frames in [('Golden-Goose-Mentor-Board.excalidraw',6),('Golden-Goose-Compact-Overview.excalidraw',1)]:
    scene=json.loads((root/name).read_text(encoding='utf-8'))
    assert scene['type']=='excalidraw' and scene['version']==2 and scene['files']=={}
    els=scene['elements']; ids={e['id']:e for e in els}
    assert len(ids)==len(els)
    frames=[e for e in els if e['type']=='frame']
    assert len(frames)==expected_frames
    for e in els:
        for key in ['x','y','width','height','angle']:
            assert isinstance(e[key],(int,float)) and math.isfinite(e[key])
        assert e['width']>=0 and e['height']>=0 and not e['isDeleted']
        assert e['type'] in ['frame','rectangle','text','line','arrow']
        if e['frameId']:
            f=ids[e['frameId']];assert f['type']=='frame'
            if e['type'] in ['rectangle','text']:
                assert f['x']<=e['x'] and f['y']<=e['y']
                assert e['x']+e['width']<=f['x']+f['width'] and e['y']+e['height']<=f['y']+f['height']
        if e['type']=='text':
            assert isinstance(e['text'],str) and e['fontFamily']==2 and e['lineHeight']==1.25
        if e['type'] in ['line','arrow']:
            assert len(e['points'])>=2 and e['points'][0]==[0,0]
            for key in ['startBinding','endBinding']:
                if e[key]:
                    target=ids[e[key]['elementId']]
                    assert target['frameId']==e['frameId']
                    assert {'id':e['id'],'type':'arrow'} in target['boundElements']
        for b in e['boundElements']:
            assert b['id'] in ids
    groups=Counter(g for e in els for g in e['groupIds'])
    assert all(n>=2 for n in groups.values())
    report[name]={'elements':len(els),'frames':len(frames),'groups':len(groups),'structure':'pass'}
assert (root/'Golden-Goose-Mentor-Board.json').read_bytes()==(root/'Golden-Goose-Mentor-Board.excalidraw').read_bytes()
for svg in (root/'previews').glob('*.svg'):ET.parse(svg)
for doc in ['index.html']:
    content=(root/doc).read_text(encoding='utf-8')
    links=re.findall(r'(?:href|src)="([^"]+)"',content) if doc.endswith('html') else re.findall(r'\]\(([^)]+)\)',content)
    for link in links:
        parsed = urlsplit(link)
        if parsed.scheme or not parsed.path or parsed.path.endswith('.zip'):continue
        assert (root/unquote(parsed.path)).exists(),(doc,link)
report['preview_review']='Six frame previews rendered; native import not exercised end to end.'
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
write_handoff_archive(repo, root/'Golden-Goose-Excalidraw-Pack.zip')
with zipfile.ZipFile(root/'Golden-Goose-Excalidraw-Pack.zip') as archive:
    assert archive.testzip() is None
    assert {name for name in archive.namelist() if name.endswith('.md')} == {'README.md', 'ARCHITECTURE.md', 'RESEARCH.md', 'BUILD_PLAN.md', 'AGENTS.md'}
print(json.dumps(report,indent=2))
