import pytest
from Source.TicTacToeModel import TicTacToeModel


@pytest.fixture
def new_game():
    """Cria um novo jogo para os testes."""
    return TicTacToeModel()


def test_initial_board_is_empty(new_game):
    """Testa se o tabuleiro está vazio no início do jogo."""
    assert all(cell == " " for row in new_game.board for cell in row)


def test_initial_player_is_x(new_game):
    """Testa se o jogador inicial é 'X'."""
    assert new_game.current_player == "X"


def test_make_move(new_game):
    """Testa se um jogador consegue fazer uma jogada válida."""
    assert new_game.make_move(0, 0) is True
    assert new_game.board[0][0] == "X"


def test_make_move_invalid(new_game):
    """Testa se uma jogada inválida (célula ocupada) é rejeitada."""
    new_game.make_move(0, 0)
    assert new_game.make_move(0, 0) is False  # Posição já ocupada


def test_switch_player(new_game):
    """Testa se o jogador alterna corretamente após uma jogada."""
    new_game.switch_player()
    assert new_game.current_player == "O"
    new_game.switch_player()
    assert new_game.current_player == "X"


def test_check_X_winner_row(new_game):
    """Testa se a vitória de X é detectada em uma linha."""
    new_game.board = [
        ["X", "X", "X"],
        [" ", " ", " "],
        [" ", " ", " "],
    ]
    assert new_game.check_winner() == "X"


def test_check_O_winner_row(new_game):
    """Testa se a vitória de O é detectada em uma linha."""
    new_game.board = [
        ["O", "O", "O"],
        [" ", " ", " "],
        [" ", " ", " "],
    ]
    assert new_game.check_winner() == "O"


def test_check_winner_column(new_game):
    """Testa se a vitória é detectada em uma coluna."""
    new_game.board = [
        ["X", " ", " "],
        ["X", " ", " "],
        ["X", " ", " "],
    ]
    assert new_game.check_winner() == "X"


def test_check_winner_diagonal(new_game):
    """Testa se a vitória é detectada em uma diagonal."""
    new_game.board = [
        ["X", " ", " "],
        [" ", "X", " "],
        [" ", " ", "X"],
    ]
    assert new_game.check_winner() == "X"


def test_check_no_winner(new_game):
    """Testa se o jogo reconhece que não há vencedor."""
    new_game.board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]
    assert new_game.check_winner() is None


def test_is_draw(new_game):
    """Testa se o jogo reconhece um empate."""
    new_game.board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]
    assert new_game.is_draw() is True


def test_not_draw_with_empty_cells(new_game):
    """Testa se o jogo reconhece que não é empate quando há células vazias."""
    new_game.board = [
        ["X", "O", " "],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]
    assert new_game.is_draw() is False
