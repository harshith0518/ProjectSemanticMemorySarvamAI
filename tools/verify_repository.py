"""Check portable documentation and exports; not a product test suite.

Standard library only. Run from any working directory. Remote research links
are intentionally not fetched: they are dated citations, not build inputs.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DOCS = {'README.md', 'ARCHITECTURE.md', 'RESEARCH.md', 'BUILD_PLAN.md', 'AGENTS.md'}
SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.cache', 'tmp'}
TEXT_SUFFIXES = {'.md', '.py', '.cjs', '.json', '.svg', '.html', '.txt', '.excalidraw', '.mmd'}
errors = []
checked_links = 0


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


def fail(path, message):
    errors.append(f'{path.relative_to(ROOT).as_posix()}: {message}')


def check_link(source, raw):
    global checked_links
    raw = raw.strip('<>')
    parts = urlsplit(raw)
    if parts.scheme or raw.startswith('//'):
        if parts.scheme == 'file':
            fail(source, f'nonportable local URL {raw}')
        return
    # The authored guide template is inserted into a root-level output file.
    base = ROOT if source.name == 'guide-template.html' else source.parent
    target = (base / unquote(parts.path)).resolve() if parts.path else source
    if not target.is_relative_to(ROOT):
        fail(source, f'link escapes checkout: {raw}')
        return
    if not target.exists():
        fail(source, f'missing local link: {raw}')
        return
    checked_links += 1
    if parts.fragment and target.suffix == '.html' and target.name != 'guide-template.html':
        parsed = Links()
        parsed.feed(target.read_text(encoding='utf-8'))
        if unquote(parts.fragment) not in parsed.ids:
            fail(source, f'missing HTML anchor: {raw}')


files = [p for p in ROOT.rglob('*') if p.is_file() and not any(part in SKIP for part in p.relative_to(ROOT).parts)]
docs = {p.relative_to(ROOT).as_posix() for p in files if p.suffix == '.md'}
if docs != EXPECTED_DOCS:
    errors.append(f'Markdown set differs: extra={sorted(docs-EXPECTED_DOCS)}, missing={sorted(EXPECTED_DOCS-docs)}')

counts = {'markdown': len(docs), 'json': 0, 'svg': 0, 'archives': 0}
for path in files:
    suffix = path.suffix.lower()
    if suffix in {'.json', '.excalidraw'}:
        try:
            json.loads(path.read_text(encoding='utf-8'))
            counts['json'] += 1
        except (ValueError, UnicodeError) as exc:
            fail(path, f'invalid JSON: {exc}')
    if suffix == '.svg':
        try:
            tree = ET.parse(path)
            assert tree.getroot().tag.endswith('svg')
            counts['svg'] += 1
        except (ET.ParseError, AssertionError) as exc:
            fail(path, f'invalid SVG: {exc}')
    if suffix in {'.md', '.html'}:
        content = path.read_text(encoding='utf-8')
        if suffix == '.md':
            content = re.sub(r'^```.*?^```[^\n]*', '', content, flags=re.M | re.S)
            for match in re.finditer(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', content):
                check_link(path, match.group(1))
        else:
            parsed = Links()
            parsed.feed(content)
            for link in parsed.links:
                check_link(path, link)
    if suffix in {'.py', '.cjs', '.json', '.html', '.md', '.excalidraw'} and path != Path(__file__).resolve():
        content = path.read_text(encoding='utf-8')
        # Generic platform font discovery is valid; developer-home paths are not.
        if re.search(r'[A-Za-z]:[/\\]Users[/\\]|/Users/[^/\s]+/|/home/[^/\s]+/|file:///', content):
            fail(path, 'contains a machine-specific home path or file URL')
    if suffix == '.zip':
        counts['archives'] += 1
        with zipfile.ZipFile(path) as archive:
            if archive.testzip():
                fail(path, 'archive CRC failure')
            names = set(archive.namelist())
            if {name for name in names if name.endswith('.md')} != EXPECTED_DOCS:
                fail(path, 'archive does not contain exactly the five canonical Markdown files')
            for name in names:
                if name.startswith(('/', '\\')) or '..' in Path(name).parts or name.endswith('.zip'):
                    fail(path, f'unsafe or nested archive entry: {name}')
                local = ROOT / name
                if local.is_file():
                    bundled, current = archive.read(name), local.read_bytes()
                    if local.suffix in TEXT_SUFFIXES or local.name in {'.gitignore', '.gitattributes'}:
                        # Git normalizes tracked text to LF; editors may use CRLF.
                        bundled, current = (value.replace(b'\r\n', b'\n') for value in (bundled, current))
                    if bundled != current:
                        fail(path, f'stale bundled file: {name}')

board = ROOT / 'mentor-excalidraw/Golden-Goose-Mentor-Board'
if board.with_suffix('.json').read_bytes() != board.with_suffix('.excalidraw').read_bytes():
    errors.append('Full board JSON and Excalidraw scene differ')

print(json.dumps({'status': 'failed' if errors else 'passed', **counts, 'local_links': checked_links, 'errors': errors}, indent=2))
sys.exit(bool(errors))
