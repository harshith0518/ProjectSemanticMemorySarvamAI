"""Verify documentation artifacts; these checks do not exercise the product."""
from pathlib import Path
import json, re, zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parent
records = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
assert len(records) == 16
assert {r['file'][:2] for r in records} == {f'{i:02}' for i in range(16)}
ns = {'svg': 'http://www.w3.org/2000/svg'}
for item in records:
    path = root / 'images' / item['file']
    source = path.read_text(encoding='utf-8')
    svg = ET.fromstring(source)
    assert svg.tag == '{http://www.w3.org/2000/svg}svg'
    assert int(svg.attrib['width']) == item['width']
    assert int(svg.attrib['height']) == item['height']
    assert svg.find('svg:title', ns) is not None and svg.find('svg:desc', ns) is not None
    assert len(svg.findall('svg:text', ns)) == item['text_blocks']
    assert all(word not in source for word in ['<script', '<foreignObject', '<image', 'https://'])
    assert 'APPLICATION IMPLEMENTATION PENDING' in source or 'NOT BUILT:' in source
for filename in ['index.html']:
    content = (root / filename).read_text(encoding='utf-8')
    links = re.findall(r'href="([^"]+)"', content) if filename.endswith('.html') else re.findall(r'\]\(([^)]+)\)', content)
    for link in links:
        parsed = urlsplit(link)
        if not parsed.scheme and parsed.path:
            assert (root / unquote(parsed.path)).exists(), (filename, link)
with zipfile.ZipFile(root / 'Golden-Goose-Mentor-SVG-Pack.zip') as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert len([n for n in names if n.startswith('mentor-svg/images/') and n.endswith('.svg')]) == 16
    for filename in ['README.md', 'ARCHITECTURE.md', 'RESEARCH.md', 'BUILD_PLAN.md', 'AGENTS.md', 'mentor-svg/index.html', 'tools/font_support.py', 'requirements-docs.txt', 'package.json', 'reference/Kivi_Golden_Goose_Task_Final.pdf']:
        assert filename in names
    assert {name for name in names if name.endswith('.md')} == {'README.md', 'ARCHITECTURE.md', 'RESEARCH.md', 'BUILD_PLAN.md', 'AGENTS.md'}
    assert all(not name.startswith(('/', '../')) for name in names)
print(json.dumps({'svg_images': 16, 'xml_and_metadata': 'pass', 'portable_vector_structure': 'pass', 'navigation_links': 'pass', 'archive_integrity': 'pass'}, indent=2))
