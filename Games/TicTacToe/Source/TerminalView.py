import os


class TerminalView:
    def display_board(self, board):
        """Exibe o tabuleiro no terminal com coordenadas estilo xadrez"""
        os.system('cls' if os.name == 'nt' else 'clear')

        # Cabeçalho das colunas
        header = "    A   B   C"
        print(header)

        # Cada linha numerada
        for i, row in enumerate(board, start=1):
            row_display = " | ".join(row)
            print(f"{i}   {row_display}")
            if i < 3:
                print("   ---+---+---")

    def display_message(self, message):
        """Exibe uma mensagem no terminal"""
        print(message)

    def get_move(self):
        """Obtém a jogada do jogador no formato estilo xadrez (ex: A1, 1a, etc.)"""
        move = input("Digite sua jogada (ex: A1, 1a, b2): ").strip()

        # Normaliza para maiúsculas
        move = move.upper()

        return move
