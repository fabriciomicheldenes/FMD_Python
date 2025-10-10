from Source.Messages import (
    TURN, WINNER, DRAW,
    INVALID_MOVE_OCCUPIED,
    INVALID_MOVE_OUT_OF_BOUNDS,
    INVALID_INPUT
)
from Source.Utils import from_notation


class TicTacToeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.playError = False
        self.errorMessage = " "

    def play_game(self):
        """Gerencia o loop principal do jogo"""
        try:
            while True:
                # Mostrar tabuleiro e vez do jogador
                self.view.display_board(self.model.board)
                self.view.display_message(TURN.format(
                    player=self.model.current_player))

                # Exibir mensagem de erro anterior, se houver
                if self.playError:
                    self.view.display_message(self.errorMessage)
                self.playError = False

                # Obter jogada do jogador (string)
                move_str = self.view.get_move()

                try:
                    row, col, status = from_notation(move_str)
                except ValueError:
                    # Jogada inválida → formato errado
                    self.playError = True
                    self.errorMessage = INVALID_INPUT.format(notation=move_str)
                    continue

                # Fora dos limites
                if status == "out_of_bounds":
                    self.playError = True
                    self.errorMessage = INVALID_MOVE_OUT_OF_BOUNDS.format(
                        coords=f"({row}, {col})", notation=move_str
                    )
                    continue

                # Posição já ocupada
                if not self.model.make_move(row, col):
                    self.playError = True
                    self.errorMessage = INVALID_MOVE_OCCUPIED.format(
                        coords=f"({row}, {col})", notation=move_str
                    )
                    continue

                # Verifica vitória
                winner = self.model.check_winner()
                if winner:
                    self.view.display_board(self.model.board)
                    self.view.display_message(WINNER.format(winner=winner))
                    break

                # Verifica empate
                if self.model.is_draw():
                    self.view.display_board(self.model.board)
                    self.view.display_message(DRAW)
                    break

                # Alterna jogador
                self.model.switch_player()

        finally:
            if hasattr(self.view, "cleanup"):
                self.view.cleanup()
