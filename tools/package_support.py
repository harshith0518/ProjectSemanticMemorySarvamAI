"""Package the portable planning handoff without caches, private data or nested ZIPs."""
from pathlib import Path
import zipfile

ROOT_DOCUMENTS = {"README.md", "ARCHITECTURE.md", "RESEARCH.md", "BUILD_PLAN.md", "AGENTS.md"}
DIRECTORIES = {"guide", "mentor-svg", "mentor-excalidraw", "reference", "tools", "research"}
EXTENSIONS = {".py", ".cjs", ".json", ".html", ".svg", ".png", ".excalidraw", ".pdf", ".txt", ".mmd"}
EXCLUDED = {".git", "node_modules", "__pycache__", ".venv", "venv", ".cache", "tmp", "reference"}
TEXT_EXTENSIONS = EXTENSIONS - {".png", ".pdf"} | {".md"}


def handoff_files(repo):
    repo = Path(repo).resolve()
    paths = []
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(repo)
        parts = relative.parts
        # The two old per-pack reference directories are intentionally omitted.
        if len(parts) > 2 and parts[0] in {"mentor-svg", "mentor-excalidraw"} and parts[1] == "reference":
            continue
        if any(part in EXCLUDED - {"reference"} for part in parts):
            continue
        if len(parts) > 1 and parts[0] not in DIRECTORIES:
            continue
        if path.suffix == ".md":
            if len(parts) == 1 and path.name in ROOT_DOCUMENTS:
                paths.append(path)
        elif path.suffix in EXTENSIONS or relative.as_posix() in {".gitignore", ".gitattributes"}:
            paths.append(path)
    required = ROOT_DOCUMENTS | {"reference/Kivi_Golden_Goose_Task_Final.pdf", "package.json", "package-lock.json", "requirements-docs.txt", "tools/font_support.py", "tools/package_support.py"}
    present = {path.relative_to(repo).as_posix() for path in paths}
    missing = required - present
    assert not missing, f"Missing handoff inputs: {sorted(missing)}"
    return paths


def write_handoff_archive(repo, target):
    repo = Path(repo).resolve()
    paths = handoff_files(repo)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            name = path.relative_to(repo).as_posix()
            if path.suffix in TEXT_EXTENSIONS or name in {".gitignore", ".gitattributes"}:
                payload = path.read_bytes().replace(b"\r\n", b"\n")
                info = zipfile.ZipInfo.from_file(path, name)
                archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED)
            else:
                archive.write(path, name)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert {name for name in names if name.endswith(".md")} == ROOT_DOCUMENTS
        assert not any(name.endswith(".zip") or name.startswith(("/", "../")) for name in names)
    return len(paths)
