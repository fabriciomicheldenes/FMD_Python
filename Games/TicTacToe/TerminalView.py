import os

class TerminalView:
    def display_board(self, board):
        """Exibe o tabuleiro no terminal"""
        rows = []
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in board:
            rows.append(" | ".join(row))
        board_display = "\n---+---+---\n".join(rows)
        print(board_display)

    def display_message(self, message):
        """Exibe uma mensagem no terminal"""
        print(message)

    def get_move(self):
        """Obtém a jogada do jogador"""
        try:
            row = int(input("Digite o número da linha (0, 1, ou 2): "))
            col = int(input("Digite o número da coluna (0, 1, ou 2): "))
            return row, col
        except ValueError:
            print(
                "Entrada inválida! Digite números inteiros.")
            return self.get_move()
