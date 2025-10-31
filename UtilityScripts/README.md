# 🧰 UtilityScripts

## 📖 Visão Geral

A pasta **`UtilityScripts/`** contém um conjunto de **scripts e miniaplicativos Python genéricos** voltados à automação e produtividade de projetos.

Esses scripts podem ser usados de forma independente (linha de comando) ou integrados posteriormente a um **aplicativo GUI em PySide6**, que oferecerá uma interface unificada para as utilidades do portfólio **FMD_Python**.

---

## 📂 Estrutura Atual

| Script | Função | Status |
|---------|--------|--------|
| `list_tree.py` | Gera uma árvore de diretórios em Markdown, texto ou JSON | ✅ Implementado |
| `list_filetypes.py` | Lista tipos/extensões de arquivos e suas contagens | 🚧 Em planejamento |
| `rename_files.py` | Renomeia arquivos em lote com base em padrões | 🚧 Em planejamento |

---

## 🔧 Uso – `list_tree.py`

O script `list_tree.py` gera uma representação estruturada do repositório.

### Exemplos

```bash
python UtilityScripts/list_tree.py --include-files --max-depth 4 -o docs/PROJECT_TREE.md
Saída padrão:

text
Copiar código
FMD_Python/
├── UtilityScripts/
│   └── list_tree.py
├── GitAutomation/
│   └── update_readme.py
└── docs/
    └── PROJECT_TREE.md
🧩 Integração com Automação Git
Os utilitários desta pasta serão usados pelos scripts da pasta GitAutomation/, que cuidam de automatizar tarefas do repositório, como:

Atualizar o README.md principal a cada modificação no SHORT_DESCRIPTION.md

Regenerar a estrutura de diretórios em docs/PROJECT_TREE.md

Executar verificações e formatações automáticas em pré-commit

🧱 Fluxo de Automação Planejado
text
Copiar código
SHORT_DESCRIPTION.md  →  (trigger)  →  GitAutomation/update_readme.py
                                           ↓
                                   atualiza README.md principal
                                           ↓
                                roda UtilityScripts/list_tree.py
                                           ↓
                                atualiza docs/PROJECT_TREE.md
📋 Próximos Passos
 Criar GitAutomation/update_readme.py

 Criar GitAutomation/pre_commit_hook.sh

 Adicionar suporte a arquivo de configuração (config.yaml)

 Integrar todos os scripts a uma GUI PySide6 (FMD_UtilityApp)

 Criar testes automáticos e workflow no GitHub Actions

✍️ Autor e Licença
Desenvolvido por Fabrício Michel Denes (FMD)
Licença: MIT