from Source.Observer import Event
from Source.Messages import (
    TURN, WINNER, DRAW,
    INVALID_MOVE_OCCUPIED,
    INVALID_MOVE_OUT_OF_BOUNDS,
    INVALID_INPUT
)
from Source.Utils import from_notation


class TicTacToeController:
    def __init__(self, model):
        self.model = model

        # Eventos (Observer pattern)
        self.on_message = Event()
        self.on_board_update = Event()
        self.on_game_over = Event()

        self.playError = False
        self.errorMessage = " "

    def play_turn(self, move_str):
        try:
            row, col, _ = from_notation(move_str)
        except ValueError:
            self.on_message.notify(INVALID_INPUT.format(notation=move_str))
            return

        # Verifica se o movimento está dentro dos limites
        if not (0 <= row < 3 and 0 <= col < 3):
            self.on_message.notify(
                INVALID_MOVE_OUT_OF_BOUNDS.format(
                    coords=f"({row}, {col})", notation=move_str
                )
            )
            return

        # Tenta realizar a jogada
        if not self.model.make_move(row, col):
            self.on_message.notify(
                INVALID_MOVE_OCCUPIED.format(
                    coords=f"({row}, {col})", notation=move_str)
            )
            return

        # Atualiza o tabuleiro
        self.on_board_update.notify(self.model.board)

        # Verifica vitória
        winner = self.model.check_winner()
        if winner:
            self.on_message.notify(f"Parabéns! O jogador {winner} venceu!")
            self.on_game_over.notify(winner)
            return

        # Verifica empate
        if self.model.is_draw():
            self.on_message.notify("O jogo terminou em empate!")
            self.on_game_over.notify(None)
            return

        # 🔹 Alterna jogador e só depois envia mensagem de turno
        self.model.switch_player()
        self.on_message.notify(f"Vez do jogador {self.model.current_player}")

    def reset_game(self):
        """Reinicia o modelo e atualiza a view."""
        self.model.__init__()  # Reinicia o tabuleiro e jogador atual
        self.on_board_update.notify(self.model.board)
        self.on_message.notify(
            f"Novo jogo! Vez do jogador {self.model.current_player}")
