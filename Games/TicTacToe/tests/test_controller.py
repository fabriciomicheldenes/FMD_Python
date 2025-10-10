from  Source.Messages import (
    INVALID_INPUT,
    INVALID_MOVE_OUT_OF_BOUNDS,
    INVALID_MOVE_OCCUPIED,
    WINNER,
    DRAW
)

import pytest
from unittest.mock import MagicMock
from Source.TicTacToeModel import TicTacToeModel
from Source.TicTacToeController import TicTacToeController


@pytest.fixture
def mock_view():
    """Cria uma mock view para testes."""
    view = MagicMock()
    return view


@pytest.fixture
def controller(mock_view):
    """Cria um controlador com um modelo e uma mock view."""
    model = TicTacToeModel()
    return TicTacToeController(model, mock_view)


def test_controller_initialization(controller, mock_view):
    """Testa se o controlador inicializa corretamente."""
    assert controller.model is not None
    assert controller.view is mock_view


def test_play_game_winner(controller, mock_view):
    """
    Testa o fluxo do jogo com um vencedor.
    Simula a jogada:
     X | X | X
    ---|---|---
     O | O |   
    ---|---|---
       |   |
    """
    # Simular jogadas do usuário que levam à vitória de "X"
    mock_view.get_move.side_effect = [
        "A1",  # X
        "A2",  # O
        "B1",  # X
        "B2",  # O
        "C1",  # X - Vitória
    ]

    controller.play_game()

    # Verificar que o tabuleiro foi exibido corretamente
    assert mock_view.display_board.call_count >= 5

    # Verificar mensagem de vitória
    mock_view.display_message.assert_any_call(WINNER.format(winner="X"))


def test_play_game_draw(controller, mock_view):
    """Testa o fluxo do jogo que termina em empate."""
    # Simular jogadas do usuário que resultam em empate
    mock_view.get_move.side_effect = [
        "A1", "B2", "C1",  # X, O, X
        "B1", "C2", "A3",  # O, X, O
        "A2", "C3", "B3",  # X, O, X -> Empate
    ]

    controller.play_game()

    # Verificar que o tabuleiro foi exibido corretamente
    assert mock_view.display_board.call_count >= 9

    # Verificar mensagem de empate
    mock_view.display_message.assert_any_call(DRAW)


def test_invalid_move_format(controller, mock_view):
    """Testa como o controlador lida com jogada em formato inválido (ex: A11, 1A1)."""
    mock_view.get_move.side_effect = [
        "A11",   # inválido
        "A1",    # X válido
        "B1",    # O válido
        "A2",    # X válido
        "B2",    # O válido
        "A3"     # X vence
    ]

    controller.play_game()

    mock_view.display_message.assert_any_call(
        INVALID_INPUT.format(notation="A11")
    )
    mock_view.display_message.assert_any_call(
        WINNER.format(winner="X")
    )


def test_out_of_bounds_move(controller, mock_view):
    """Testa como o controlador lida com jogada fora dos limites (ex: X9)."""
    mock_view.get_move.side_effect = [
        "X9",    # fora dos limites
        "A1",    # X válido
        "B1",    # O válido
        "A2",    # X válido
        "B2",    # O válido
        "A3"     # X vence
    ]

    controller.play_game()

    mock_view.display_message.assert_any_call(
        INVALID_MOVE_OUT_OF_BOUNDS.format(coords="(8, 23)", notation="X9")
    )
    mock_view.display_message.assert_any_call(
        WINNER.format(winner="X")
    )


def test_occupied_position(controller, mock_view):
    """Testa como o controlador lida com jogada em posição já ocupada."""
    mock_view.get_move.side_effect = [
        "A1",  # X válido
        "A1",  # O tenta mesma posição
        "B1",  # O válido
        "A2",  # X válido
        "B2",  # O válido
        "A3"   # X vence
    ]

    controller.play_game()

    mock_view.display_message.assert_any_call(
        INVALID_MOVE_OCCUPIED.format(coords="(0, 0)", notation="A1")
    )
    mock_view.display_message.assert_any_call(
        WINNER.format(winner="X")
    )


def test_alternate_players(controller, mock_view):
    """Testa se os jogadores alternam corretamente."""
    # Simular jogadas alternadas
    mock_view.get_move.side_effect = [
        "A1",  # X
        "A2",  # O
        "B1",  # X
        "B2",  # O
        "C1",  # X - Vitória
    ]

    controller.play_game()

    # Verificar que o controlador alternou os jogadores
    assert controller.model.board[0][0] == "X"  # A1
    assert controller.model.board[1][0] == "O"  # A2
