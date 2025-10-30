# Changelog
Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]
- Em desenvolvimento...

## [0.3.0] - 2025-10-09
### Adicionado
- Implementação do padrão Observer no `TicTacToeController`
- Classe `Event` em `observer.py` para gerenciar subscrições
- Novos eventos: `on_message`, `on_board_update`, `on_game_over`

### Alterado
- `TerminalView` agora atua como observer:
  - Limpa tela a cada atualização de tabuleiro
  - Recebe mensagens via evento `on_message`
  - Encerra jogo via `on_game_over`
- `TicTacToe.py` reorganizado com função `main()` e loop controlado por evento
- `Controller` não depende mais diretamente de nenhuma view → código desacoplado e extensível

## [0.2.0] - 2025-10-09
### Adicionado
- Módulo `messages.py` para centralizar todas as mensagens do jogo.
- Funções `from_notation` e `to_notation` para conversão entre coordenadas e notação estilo xadrez.
- Novos testes cobrindo jogadas inválidas, fora dos limites e posições ocupadas.

### Alterado
- `TicTacToeController.play_game` agora utiliza mensagens centralizadas e diferenciadas.
- `TerminalView.get_move` retorna a jogada como string crua (ex.: "A1"), deixando parsing para o Controller.
- Testes de vitória, empate, alternância de jogadores e exibição de tabuleiro atualizados para refletir a nova lógica.

## [0.1.0] - 2025-10-01
### Adicionado
- Implementação inicial do jogo TicTacToe com padrão MVC.
- Classes: `TicTacToeModel`, `TicTacToeController`, `TerminalView`.
- Testes básicos para jogadas válidas, vitória e empate.
