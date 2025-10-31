# 🧰 FMD_Python Utilities – `list_tree.py`

## 📖 Visão Geral

O script **`list_tree.py`** é um utilitário desenvolvido em Python para gerar automaticamente uma **visão estruturada** do repositório `FMD_Python`, em formato **Markdown**, **texto** ou **JSON**.

Seu principal objetivo é **documentar a estrutura de diretórios e arquivos** do projeto, permitindo que o **README.md principal** do repositório seja atualizado automaticamente sempre que a árvore de diretórios mudar.

Este script faz parte da iniciativa de padronização e automação do portfólio `FMD_Python`, centralizando a geração de documentação técnica e estrutural.

---

## ⚙️ Funcionalidades

- Gera a **árvore de diretórios** do projeto (`docs/PROJECT_TREE.md`)  
- Pode incluir ou não arquivos individuais (`--include-files`)
- Permite definir a **profundidade máxima** da árvore (`--max-depth`)
- Ignora pastas comuns e respeita o `.gitignore`
- Suporta diferentes formatos de saída:
  - `md` → Markdown (para README)
  - `text` → Texto simples (para logs)
  - `json` → Estruturado (para automações futuras)
- Compatível com hooks de pré-commit ou GitHub Actions

---

## 🧩 Integração com o README.md do Projeto

O arquivo gerado (`docs/PROJECT_TREE.md`) será **inserido automaticamente** dentro do `README.md` principal do repositório **FMD_Python**, mantendo a seção de estrutura sempre atualizada.

Essa automação permitirá que o README exiba a árvore de pastas mais recente sem necessidade de edição manual.

Exemplo de trecho no `README.md` principal:

```markdown
## 📂 Estrutura do Projeto

> *Esta seção é atualizada automaticamente pelo script `tools/list_tree.py`.*

<!-- START:PROJECT_TREE -->
(conteúdo do docs/PROJECT_TREE.md é inserido aqui automaticamente)
<!-- END:PROJECT_TREE -->
```

## Como usar
```
python tools/list_tree.py --include-files --max-depth 4 -o docs/PROJECT_TREE.md
```

🔧 Opções principais
Parâmetro	Descrição
--root	Define a pasta raiz do projeto (padrão: .)
--output	Caminho do arquivo de saída (padrão: docs/PROJECT_TREE.md)
--include-files	Inclui arquivos individuais na árvore
--max-depth	Limita a profundidade da árvore
--ignore	Adiciona padrões extras para ignorar
--format	Define o formato de saída (md, text, json)
--no-gitignore	Ignora o .gitignore do projeto
Exemplo prático
python tools/list_tree.py --include-files --max-depth 3 -f md -o docs/PROJECT_TREE.md


Resultado gerado (exemplo):

FMD_Python/
├── tools/
│   └── list_tree.py
├── src/
│   ├── core/
│   └── utils/
└── docs/
    └── PROJECT_TREE.md

🔄 Automação com Git Hooks (opcional)

Para manter o arquivo atualizado antes de cada commit, adicione um hook:

.githooks/pre-commit

#!/usr/bin/env bash
python tools/list_tree.py --include-files --max-depth 4 -o docs/PROJECT_TREE.md >/dev/null
git add docs/PROJECT_TREE.md


Ativar o hook:

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

🧱 Estrutura do Repositório
FMD_Python/
├── tools/
│   └── list_tree.py
├── docs/
│   └── PROJECT_TREE.md
├── README.md
└── ...

🏁 Próximos Passos

 Integrar list_tree.py ao fluxo de atualização automática do README.md

 Criar workflow no GitHub Actions para executar a geração da árvore em cada push

 Adicionar testes e validações de integridade para garantir consistência

 Publicar o utilitário como pacote interno (fmd_utils)

✍️ Autor e Licença

Desenvolvido por Fabrício Michel Denes (FMD)
Licença: MIT
Projeto: FMD_Python Utilities