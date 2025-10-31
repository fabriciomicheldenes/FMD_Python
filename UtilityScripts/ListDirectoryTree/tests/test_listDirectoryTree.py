import json
# import tempfile
from pathlib import Path
# import shutil
import pytest

from UtilityScripts.ListDirectoryTree.ListDirectoryTree import DirectoryTreeGenerator


@pytest.fixture
def temp_project(tmp_path: Path):
    """
    Cria uma estrutura de diretórios temporária para teste:
    project/
    ├── src/
    │   ├── main.py
    │   └── utils/
    │       └── helper.py
    ├── docs/
    │   └── readme.md
    └── .gitignore
    """
    root = tmp_path / "project"
    (root / "src" / "utils").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (root / "src" / "utils" / "helper.py").write_text("def f(): pass", encoding="utf-8")
    (root / "docs" / "readme.md").write_text("# docs", encoding="utf-8")
    (root / ".gitignore").write_text("__pycache__\n*.tmp\n", encoding="utf-8")
    return root


def test_generate_structure_basic(temp_project: Path):
    """Verifica se a árvore é gerada corretamente."""
    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    lines, dirs, files = gen.generate()

    # deve conter o nome do root
    assert lines[0].startswith("project/")

    # total de diretórios esperados: src, utils, docs
    assert dirs == 3

    # total de arquivos esperados: 4 arquivos "main.py", "helper.py", "readme.md", ".gitignore"
    assert files == 4

    # verificação de presença dos nomes esperados
    tree_str = "\n".join(lines)
    for expected in ["src", "docs", "main.py", "helper.py"]:
        assert expected in tree_str


def test_markdown_output(temp_project: Path):
    """Verifica se o formato markdown contém metadados e código-fence."""
    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    md = gen.to_markdown()

    assert md.startswith("# Estrutura do Projeto")
    assert "```text" in md
    assert "Diretórios:" in md
    assert "Arquivos:" in md


def test_text_output(temp_project: Path):
    """Verifica se o formato texto contém totais e linhas."""
    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    txt = gen.to_text()

    assert "Diretórios:" in txt
    assert "Arquivos:" in txt
    assert "src" in txt


def test_json_output(temp_project: Path):
    """Verifica se o formato JSON retorna dados válidos."""
    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    js = gen.to_json()

    data = json.loads(js)
    assert data["root"] == "project"
    assert data["dirs"] >= 3
    assert "tree" in data


def test_ignore_patterns(temp_project: Path):
    """Verifica se padrões de exclusão funcionam."""
    # cria um diretório que deve ser ignorado
    ignored = temp_project / "__pycache__"
    ignored.mkdir()
    (ignored / "temp.tmp").write_text("x", encoding="utf-8")

    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    lines, _, _ = gen.generate()

    # o diretório ignorado não deve aparecer
    tree_str = "\n".join(lines)
    assert "__pycache__" not in tree_str


def test_save_to_file(temp_project: Path):
    """Verifica se o arquivo de saída é criado."""
    gen = DirectoryTreeGenerator(root=temp_project, include_files=True)
    out_path = temp_project / "out.md"
    gen.save(out_path, fmt="md")

    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")
    assert "Estrutura do Projeto" in content
