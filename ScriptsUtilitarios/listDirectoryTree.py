#!/usr/bin/env python3
from __future__ import annotations
import argparse
import fnmatch
import os
from pathlib import Path
from datetime import datetime
from typing import Iterable, List, Set

DEFAULT_IGNORES = {
    ".git", "__pycache__", ".venv", "venv", ".mypy_cache", "node_modules",
    ".idea", ".vscode", "dist", "build", ".pytest_cache", ".DS_Store"
}


def load_gitignore(root: Path) -> List[str]:
    gi = root / ".gitignore"
    patterns: List[str] = []
    if gi.exists():
        for line in gi.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def is_ignored(path: Path, root: Path, ignore_set: Set[str], gitignore_patterns: List[str]) -> bool:
    name = path.name
    # ignora por nome direto (pastas comuns)
    if name in ignore_set:
        return True
    # ignora por padrões do .gitignore (bem simples, relativo à raiz)
    rel = str(path.relative_to(root)).replace("\\", "/")
    for pat in gitignore_patterns:
        # suporta diretórios (com barra) e curingas simples
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(name, pat):
            return True
    return False


def walk_tree(root: Path, include_files: bool, max_depth: int | None,
              ignore_set: Set[str], gitignore_patterns: List[str]) -> tuple[List[str], int, int]:
    """
    Retorna (linhas_tree, total_dirs, total_files)
    """
    lines: List[str] = []
    total_dirs = 0
    total_files = 0

    def _children(p: Path) -> List[Path]:
        try:
            return sorted([c for c in p.iterdir()], key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return []

    def _rec(p: Path, prefix: str, depth: int):
        nonlocal total_dirs, total_files
        children = [c for c in _children(p) if not is_ignored(
            c, root, ignore_set, gitignore_patterns)]
        # se não incluir arquivos, retenha apenas diretórios
        if not include_files:
            children = [c for c in children if c.is_dir()]

        for idx, c in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            lines.append(
                f"{prefix}{connector}{c.name}{'/' if c.is_dir() else ''}")
            if c.is_dir():
                total_dirs += 1
                if max_depth is None or depth + 1 <= max_depth:
                    new_prefix = f"{prefix}{'    ' if idx == len(children) - 1 else '│   '}"
                    _rec(c, new_prefix, depth + 1)
            else:
                total_files += 1

    root_display = f"{root.name}/"
    lines.append(root_display)
    _rec(root, "", 1)
    return lines, total_dirs, total_files


def as_markdown(root: Path, tree_lines: List[str], total_dirs: int, total_files: int) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = []
    md.append(f"# Estrutura do Projeto `{root.name}`")
    md.append("")
    md.append(f"_Gerado em {now}_")
    md.append("")
    md.append(f"- Diretórios: **{total_dirs}**")
    md.append(f"- Arquivos: **{total_files}**")
    md.append("")
    md.append("```text")
    md.extend(tree_lines)
    md.append("```")
    md.append("")
    return "\n".join(md)


def as_text(tree_lines: List[str], total_dirs: int, total_files: int) -> str:
    header = [f"Diretórios: {total_dirs}", f"Arquivos: {total_files}", ""]
    return "\n".join(header + tree_lines) + "\n"


def as_json(root: Path, tree_lines: List[str], total_dirs: int, total_files: int) -> str:
    # JSON simples: mantemos a árvore como string (útil p/ tooling)
    import json
    return json.dumps({
        "root": root.name,
        "dirs": total_dirs,
        "files": total_files,
        "tree": "\n".join(tree_lines)
    }, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Gera árvore estruturada do projeto.")
    parser.add_argument("--root", type=str, default=".",
                        help="Raiz do projeto (default: .)")
    parser.add_argument("--output", "-o", type=str, default="docs/PROJECT_TREE.md",
                        help="Arquivo de saída (default: docs/PROJECT_TREE.md)")
    parser.add_argument("--format", "-f", choices=[
                        "md", "text", "json"], default="md", help="Formato de saída (default: md)")
    parser.add_argument("--include-files", action="store_true",
                        help="Incluir arquivos além de diretórios")
    parser.add_argument("--max-depth", type=int, default=None,
                        help="Profundidade máxima (padrão: ilimitada)")
    parser.add_argument("--ignore", action="append", default=[],
                        help="Padrões adicionais para ignorar (pode repetir)")
    parser.add_argument("--no-gitignore", action="store_true",
                        help="Não considerar padrões do .gitignore")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    ignore_set: Set[str] = set(DEFAULT_IGNORES)
    if args.ignore:
        ignore_set.update(args.ignore)

    gitignore_patterns: List[str] = []
    if not args.no_gitignore:
        gitignore_patterns = load_gitignore(root)

    tree_lines, dcount, fcount = walk_tree(
        root, args.include_files, args.max_depth, ignore_set, gitignore_patterns)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "md":
        content = as_markdown(root, tree_lines, dcount, fcount)
    elif args.format == "text":
        content = as_text(tree_lines, dcount, fcount)
    else:
        content = as_json(root, tree_lines, dcount, fcount)

    out_path.write_text(content, encoding="utf-8")
    print(f"[ok] Estrutura gerada em: {out_path}")


if __name__ == "__main__":
    main()
