from Source.Observer import Event
from Source.Messages import (
    TURN, WINNER, DRAW,
    INVALID_MOVE_OCCUPIED,
    INVALID_MOVE_OUT_OF_BOUNDS,
    INVALID_INPUT
)
from Source.Utils import from_notation, to_notation


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
        """Executa uma jogada única (em vez de loop infinito)"""
        try:
            row, col, status = from_notation(move_str)
        except ValueError:
            self.on_message.notify(INVALID_INPUT.format(notation=move_str))
            return

        if status == "out_of_bounds":
            self.on_message.notify(
                INVALID_MOVE_OUT_OF_BOUNDS.format(
                    coords=f"({row}, {col})",
                    notation=move_str
                )
            )
            return

        if not self.model.make_move(row, col):
            self.on_message.notify(
                INVALID_MOVE_OCCUPIED.format(
                    coords=f"({row}, {col})",
                    notation=move_str
                )
            )
            return

        # Atualiza tabuleiro
        self.on_board_update.notify(self.model.board)

        winner = self.model.check_winner()
        if winner:
            self.on_message.notify(WINNER.format(winner=winner))
            self.on_game_over.notify()
            return

        if self.model.is_draw():
            self.on_message.notify(DRAW)
            self.on_game_over.notify()
            return

        self.model.switch_player()
        self.on_message.notify(TURN.format(player=self.model.current_player))
