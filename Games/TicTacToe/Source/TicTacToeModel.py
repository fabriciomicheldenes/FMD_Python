class TicTacToeModel:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def make_move(self, row, col):
        """Realiza uma jogada no tabuleriro"""
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            return True
        return False

    def check_winner(self):
        """Verifica se ha um vencedor no jogo."""
        # Verifica linhas
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]

        # Verifica colunas
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]

        # Verifica diagonais
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]

        return None

    def is_draw(self):
        """Verifica se o jogo terminou em empate"""
        for row in self.board:
            if " " in row:
                return False

        return True

    def switch_player(self):
        # Troca de jogador
        self.current_player = "O" if self.current_player == "X" else "X"
