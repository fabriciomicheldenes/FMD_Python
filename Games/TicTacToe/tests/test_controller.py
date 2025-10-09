import pytest
from unittest.mock import MagicMock
from TicTacToeModel import TicTacToeModel
from TicTacToeController import TicTacToeController


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
        (0, 0),  # X
        (1, 0),  # O
        (0, 1),  # X
        (1, 1),  # O
        (0, 2),  # X - Vitória
    ]

    controller.play_game()

    # Verificar que o tabuleiro foi exibido corretamente
    assert mock_view.display_board.call_count >= 5

    # Verificar mensagem de vitória
    mock_view.display_message.assert_any_call("Parabéns! O jogador X venceu!")


def test_play_game_draw(controller, mock_view):
    """Testa o fluxo do jogo que termina em empate."""
    # Simular jogadas do usuário que resultam em empate
    mock_view.get_move.side_effect = [
        (0, 0), (1, 1), (2, 0),  # X, X, O
        (1, 0), (1, 2), (0, 2),  # O, O, X
        (0, 1), (2, 2), (2, 1),  # X, X, O  - Empate
    ]

    controller.play_game()

    # Verificar que o tabuleiro foi exibido corretamente
    assert mock_view.display_board.call_count >= 9

    # Imprimir todas as chamadas feitas ao método display_message
    print("Chamadas ao display_message:",
          mock_view.display_message.call_args_list)

    # Verificar mensagem de empate
    mock_view.display_message.assert_any_call("O jogo terminou em empate!")


def test_invalid_move(controller, mock_view):
    """Testa como o controlador lida com uma jogada inválida."""
    # Simular jogadas (uma inválida seguida de válidas que terminam o jogo)
    mock_view.get_move.side_effect = [
        (0, 0),  # X - Válida
        (0, 0),  # O - Inválida (já ocupada)
        (1, 0),  # O - Válida
        (0, 1),  # X
        (1, 1),  # O
        (0, 2),  # X - Vitória
    ]

    controller.play_game()

    # Verificar mensagem de jogada inválida
    mock_view.display_message.assert_any_call(
        "A posição (0, 0) já está ocupada. Escolha outra!")

    # Verificar mensagem de vitória
    mock_view.display_message.assert_any_call("Parabéns! O jogador X venceu!")


def test_out_of_bounds_move(controller, mock_view):
    """Testa como o controlador lida com jogadas fora dos limites do tabuleiro."""
    # Simular jogadas fora dos limites
    mock_view.get_move.side_effect = [
        (3, 3),  # X - Inválido, fora dos limites
        (0, 0),  # X - Válida
        (1, 0),  # O - Válida
        (0, 1),  # X
        (1, 1),  # O
        (0, 2),  # X - Vitória
    ]

    controller.play_game()

    # Verificar mensagem de jogada fora dos limites
    mock_view.display_message.assert_any_call(
        "A posição (3, 3) está fora dos limites. Tente novamente!")


def test_alternate_players(controller, mock_view):
    """Testa se os jogadores alternam corretamente."""
    # Simular jogadas alternadas
    mock_view.get_move.side_effect = [
        (0, 0),  # X
        (1, 0),  # O - Válida
        (0, 1),  # X
        (1, 1),  # O
        (0, 2),  # X - Vitória
    ]

    controller.play_game()

    # Verificar que o controlador alternou os jogadores
    assert controller.model.board[0][0] == "X"
    assert controller.model.board[1][0] == "O"
