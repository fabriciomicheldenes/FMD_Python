#!/usr/bin/env python3
from __future__ import annotations
import fnmatch
import json
from pathlib import Path
from datetime import datetime
from typing import List, Set, Optional


class DirectoryTreeGenerator:
    """
    Classe para gerar representações estruturadas da árvore de diretórios.

    Funcionalidades:
        - Leitura do .gitignore
        - Exclusão de pastas padrão (node_modules, .git, etc.)
        - Geração nos formatos Markdown, texto e JSON
    """

    DEFAULT_IGNORES = {
        ".git", "__pycache__", ".venv", "venv", ".mypy_cache", "node_modules",
        ".idea", ".vscode", "dist", "build", ".pytest_cache", ".DS_Store"
    }

    def __init__(
        self,
        root: str | Path = ".",
        include_files: bool = False,
        max_depth: Optional[int] = None,
        extra_ignores: Optional[Set[str]] = None,
        use_gitignore: bool = True,
    ):
        self.root = Path(root).resolve()
        self.include_files = include_files
        self.max_depth = max_depth
        self.ignore_set = set(self.DEFAULT_IGNORES)
        if extra_ignores:
            self.ignore_set.update(extra_ignores)
        self.use_gitignore = use_gitignore
        self.gitignore_patterns = self._load_gitignore() if use_gitignore else []

    # ----------------------------------------------------------------------
    # 🔸 Métodos internos
    # ----------------------------------------------------------------------

    def _load_gitignore(self) -> List[str]:
        gi = self.root / ".gitignore"
        patterns: List[str] = []
        if gi.exists():
            for line in gi.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)
        return patterns

    def _is_ignored(self, path: Path) -> bool:
        name = path.name
        if name in self.ignore_set:
            return True
        rel = str(path.relative_to(self.root)).replace("\\", "/")
        for pat in self.gitignore_patterns:
            if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(name, pat):
                return True
        return False

    def _children(self, p: Path) -> List[Path]:
        try:
            return sorted([c for c in p.iterdir()], key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return []

    def _walk(self, p: Path, prefix: str, depth: int, lines: List[str], counts: dict):
        children = [c for c in self._children(p) if not self._is_ignored(c)]
        if not self.include_files:
            children = [c for c in children if c.is_dir()]

        for idx, c in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            lines.append(
                f"{prefix}{connector}{c.name}{'/' if c.is_dir() else ''}")
            if c.is_dir():
                counts["dirs"] += 1
                if self.max_depth is None or depth + 1 <= self.max_depth:
                    new_prefix = f"{prefix}{'    ' if idx == len(children) - 1 else '│   '}"
                    self._walk(c, new_prefix, depth + 1, lines, counts)
            else:
                counts["files"] += 1

    # ----------------------------------------------------------------------
    # 🔸 Métodos públicos
    # ----------------------------------------------------------------------

    def generate(self) -> tuple[List[str], int, int]:
        """Gera a estrutura da árvore e retorna (linhas, total_dirs, total_files)."""
        lines: List[str] = [f"{self.root.name}/"]
        counts = {"dirs": 0, "files": 0}
        self._walk(self.root, "", 1, lines, counts)
        return lines, counts["dirs"], counts["files"]

    def to_markdown(self) -> str:
        """Retorna a árvore em formato Markdown."""
        lines, dcount, fcount = self.generate()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md = [
            f"# Estrutura do Projeto `{self.root.name}`",
            "",
            f"_Gerado em {now}_",
            "",
            f"- Diretórios: **{dcount}**",
            f"- Arquivos: **{fcount}**",
            "",
            "```text",
            *lines,
            "```",
            "",
        ]
        return "\n".join(md)

    def to_text(self) -> str:
        """Retorna a árvore em texto simples."""
        lines, dcount, fcount = self.generate()
        header = [f"Diretórios: {dcount}", f"Arquivos: {fcount}", ""]
        return "\n".join(header + lines) + "\n"

    def to_json(self) -> str:
        """Retorna a árvore em formato JSON."""
        lines, dcount, fcount = self.generate()
        return json.dumps({
            "root": self.root.name,
            "dirs": dcount,
            "files": fcount,
            "tree": "\n".join(lines)
        }, ensure_ascii=False, indent=2)

    def save(self, path: str | Path, fmt: str = "md"):
        """Gera o arquivo de saída no formato especificado (md, text, json)."""
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)

        if fmt == "md":
            content = self.to_markdown()
        elif fmt == "text":
            content = self.to_text()
        elif fmt == "json":
            content = self.to_json()
        else:
            raise ValueError(f"Formato não suportado: {fmt}")

        output.write_text(content, encoding="utf-8")
        print(f"[ok] Estrutura gerada em: {output}")


def _parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Gera árvore estruturada do projeto.")
    parser.add_argument("--root", type=str, default=".",
                        help="Raiz do projeto (default: .)")
    parser.add_argument("--output", "-o", type=str, default="docs/PROJECT_TREE.md",
                        help="Arquivo de saída (default: docs/PROJECT_TREE.md)")
    parser.add_argument("--format", "-f", choices=["md", "text", "json"], default="md",
                        help="Formato de saída (default: md)")
    parser.add_argument("--include-files", action="store_true",
                        help="Incluir arquivos além de diretórios")
    parser.add_argument("--max-depth", type=int, default=None,
                        help="Profundidade máxima (padrão: ilimitada)")
    parser.add_argument("--ignore", action="append", default=[],
                        help="Padrões adicionais para ignorar (pode repetir)")
    parser.add_argument("--no-gitignore", action="store_true",
                        help="Não considerar padrões do .gitignore")

    return parser.parse_args()

### ----------------------------------------------------------------------
# CLI e execução direta
# ----------------------------------------------------------------------
def main():
    args = _parse_args()

    gen = DirectoryTreeGenerator(
        root=args.root,
        include_files=args.include_files,
        max_depth=args.max_depth,
        extra_ignores=set(args.ignore),
        use_gitignore=not args.no_gitignore,
    )

    gen.save(args.output, fmt=args.format)


if __name__ == "__main__":
    main()
