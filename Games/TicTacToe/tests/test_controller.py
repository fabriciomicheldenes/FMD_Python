import pytest
from unittest.mock import MagicMock

from Source.Messages import (
    INVALID_INPUT,
    INVALID_MOVE_OUT_OF_BOUNDS,
    INVALID_MOVE_OCCUPIED,
    WINNER,
    DRAW,
)
from Source.TicTacToeModel import TicTacToeModel
from Source.TicTacToeController import TicTacToeController


@pytest.fixture
def controller():
    """Cria um controlador com um modelo."""
    model = TicTacToeModel()
    return TicTacToeController(model)


def test_controller_initialization(controller):
    """Testa se o controlador inicializa corretamente."""
    assert controller.model is not None


def test_play_game_winner(controller):
    """Testa o fluxo do jogo com um vencedor (X vence)."""
    messages = []
    controller.on_message.subscribe(messages.append)

    moves = ["A1", "A2", "B1", "B2", "C1"]  # Vitória de X
    for move in moves:
        controller.play_turn(move)

    assert WINNER.format(winner="X") in messages


def test_play_game_draw(controller):
    """Testa o fluxo do jogo que termina em empate."""
    messages = []
    controller.on_message.subscribe(messages.append)

    moves = [
        "A1", "B2", "C1",  # X, O, X
        "B1", "C2", "A3",  # O, X, O
        "A2", "C3", "B3",  # X, O, X -> Empate
    ]
    for move in moves:
        controller.play_turn(move)

    assert DRAW in messages


def test_invalid_move_format(controller):
    """Testa como o controlador lida com jogada em formato inválido (ex: A11)."""
    messages = []
    controller.on_message.subscribe(messages.append)

    moves = ["A11", "A1", "B1", "A2", "B2", "A3"]  # Vitória de X
    for move in moves:
        controller.play_turn(move)

    assert INVALID_INPUT.format(notation="A11") in messages
    assert WINNER.format(winner="X") in messages


def test_out_of_bounds_move(controller):
    """Testa como o controlador lida com jogada fora dos limites (ex: X9)."""
    messages = []
    controller.on_message.subscribe(messages.append)

    moves = ["X9", "A1", "B1", "A2", "B2", "A3"]  # Vitória de X
    for move in moves:
        controller.play_turn(move)

    assert INVALID_MOVE_OUT_OF_BOUNDS.format(
        coords="(8, 23)", notation="X9") in messages
    assert WINNER.format(winner="X") in messages


def test_occupied_position(controller):
    """Testa como o controlador lida com jogada em posição já ocupada."""
    messages = []
    controller.on_message.subscribe(messages.append)

    moves = ["A1", "A1", "B1", "A2", "B2", "A3"]  # Vitória de X
    for move in moves:
        controller.play_turn(move)

    assert INVALID_MOVE_OCCUPIED.format(
        coords="(0, 0)", notation="A1") in messages
    assert WINNER.format(winner="X") in messages


def test_alternate_players(controller):
    """Testa se os jogadores alternam corretamente."""
    moves = ["A1", "A2", "B1", "B2", "C1"]  # Vitória de X
    for move in moves:
        controller.play_turn(move)

    assert controller.model.board[0][0] == "X"  # A1
    assert controller.model.board[1][0] == "O"  # A2
