"""Build the explanatory guide; this is documentation tooling, not the Kivi app."""
from pathlib import Path
from html import escape
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
data = json.loads((HERE / "guide-data.json").read_text(encoding="utf-8"))
chapters = data["chapters"]
by_id = {chapter["id"]: chapter for chapter in chapters}

def esc(value):
    return escape(str(value), quote=True)

def flow_html(items):
    return '<div class="flow" style="--count:' + str(len(items)) + '">' + ''.join(
        '<div class="flow-step">' + esc(item) + '</div>' for item in items
    ) + '</div>'

nav = ['<a href="#overview"><span class="nav-num">●</span><span>Overview</span></a>']
options = ['<option value="overview">Overview</option>']
rendered = []
for index, chapter in enumerate(chapters):
    ident = chapter["id"]
    title = chapter["title"]
    status = "Next work · not started" if ident == "10-next" else "Planned · product implementation pending"
    nav.append(f'<a href="#{esc(ident)}"><span class="nav-num">{esc(chapter["number"])}</span><span>{esc(title)}</span></a>')
    options.append(f'<option value="{esc(ident)}">{esc(chapter["number"])} · {esc(title)}</option>')
    previous_id = chapters[index - 1]["id"] if index else "overview"
    previous_title = chapters[index - 1]["title"] if index else "Overview"
    next_id = chapters[index + 1]["id"] if index < len(chapters) - 1 else "overview"
    next_title = chapters[index + 1]["title"] if index < len(chapters) - 1 else "Overview"
    steps = ''.join(f'<li><strong>{esc(label)}</strong><p>{esc(body)}</p></li>' for label, body in chapter["steps"])
    remaining = ''.join(f'<li>{esc(item)}</li>' for item in chapter["remaining"])
    details = ''.join(f'<li>{esc(item)}</li>' for item in chapter["details"])
    related = ''.join(f'<a href="#{esc(item)}">{esc(by_id[item]["number"])} · {esc(by_id[item]["title"])}</a>' for item in chapter["related"])
    rendered.append(f'''<section class="page" id="{esc(ident)}" hidden aria-labelledby="{esc(ident)}-title">
<p class="eyebrow">{esc(chapter["question"])}</p><h2 id="{esc(ident)}-title">{esc(title)}</h2>
<span class="status">{esc(status)}</span><p class="lead">{esc(chapter["summary"])}</p>
{flow_html(chapter["flow"])}
<h3>{"Milestones and completion criteria" if ident == "10-next" else "What happens, step by step"}</h3><ol class="steps">{steps}</ol>
<div class="example"><strong>{"First observable success" if ident == "10-next" else "Illustrative example"}</strong>{esc(chapter["example"])}</div>
<h3>{"Keep these boundaries" if ident == "10-next" else "What remains to build or decide"}</h3><ul class="remaining">{remaining}</ul>
<details><summary>Technical details · open only when needed</summary><ul class="technical-list">{details}</ul></details>
<h3>Related processes</h3><div class="chapter-links">{related}</div>
<p class="source">Canonical reference: <a href="ARCHITECTURE.md">{esc(chapter["source"])}</a> · <a href="BUILD_PLAN.md">Build plan and remaining work</a></p>
<nav class="pager" aria-label="Previous and next topic"><a href="#{esc(previous_id)}">← {esc(previous_title)}</a><a href="#{esc(next_id)}">{esc(next_title)} →</a></nav>
</section>''')

nav = [nav[0], nav[-1], *nav[1:-1]]
options = [options[0], options[-1], *options[1:-1]]
template = (HERE / 'guide-template.html').read_text(encoding='utf-8')
for marker, content in {
    '__NAV__': ''.join(nav), '__OPTIONS__': ''.join(options), '__CHAPTERS__': '\n'.join(rendered),
    '__DATE__': esc(data['snapshot']), '__BASELINE__': esc(data['baseline'])
}.items():
    template = template.replace(marker, content)
(ROOT / 'ARCHITECTURE_GUIDE.html').write_text(template, encoding='utf-8',newline='\n')

print(f"Generated standalone HTML guide with {len(chapters)} topics; canonical Markdown is maintained at the repository root.")
