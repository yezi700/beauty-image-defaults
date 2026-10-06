"""Validate repository structure only; behavioral evals require a separate review."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


def validate(root: Path) -> list[str]:
    errors = []
    entry = root / "SKILL.md"
    content = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    if not match:
        errors.append("SKILL.md: missing YAML frontmatter")
    else:
        try:
            meta = yaml.safe_load(match.group(1))
            if not isinstance(meta, dict):
                errors.append("Frontmatter must be a mapping")
            else:
                if meta.get("name") != "beauty-image-defaults":
                    errors.append("Unexpected skill name")
                description = meta.get("description")
                if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                    errors.append("Description must be 1–1024 characters")
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML: {exc}")

    graph = {}
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        graph[path.resolve()] = set()
        fence = None
        prose = []
        for line in text.splitlines():
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if marker:
                token, suffix = marker.groups()
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                    fence = None
            elif fence is None:
                prose.append(line)
        if fence:
            errors.append(f"{path.relative_to(root)}: unclosed code fence")
        if re.search(r"\[TODO:|\bFIXME\b", text):
            errors.append(f"{path.relative_to(root)}: unfinished placeholder")
        # This repository uses inline file links without fragments or reference-style links.
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", "\n".join(prose)):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            resolved = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f"{path.relative_to(root)}: broken/escaping link {target}")
            if url.fragment:
                errors.append(f"{path.relative_to(root)}: anchor needs manual validation: {target}")
            graph[path.resolve()].add(resolved)

    reachable = set()
    pending = [entry.resolve()]
    while pending:
        node = pending.pop()
        if node not in reachable:
            reachable.add(node)
            pending.extend(graph.get(node, ()))
    for path in (root / "references").rglob("*.md"):
        if path.resolve() not in reachable:
            errors.append(f"Unreachable reference: {path.relative_to(root)}")

    routing = (root / "evals/routing.md").read_text(encoding="utf-8")
    behavior = (root / "evals/expected-behavior.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\| (R\d+) \|", routing, re.M)
    ids += re.findall(r"^## (B\d+)$", behavior, re.M)
    expected = {f"R{i:02}" for i in range(1, 21)} | {f"B{i:02}" for i in range(1, 11)}
    if len(ids) != len(set(ids)) or set(ids) != expected:
        errors.append("Eval IDs must be unique R01–R20 and B01–B10")
    return errors


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]
    problems = validate(repo)
    for problem in problems:
        print(f"FAIL: {problem}")
    print("Structure: FAIL" if problems else "Structure: PASS (behavior and image results are not tested)")
    sys.exit(bool(problems))
