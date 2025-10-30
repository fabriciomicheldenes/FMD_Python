import pytest
from unittest.mock import patch, MagicMock
from Source.TerminalView import TerminalView


@pytest.fixture
def terminal_view():
    """Fixture para instanciar o TerminalView com um controller falso."""
    fake_controller = MagicMock()
    return TerminalView(fake_controller)


def test_display_board(terminal_view, capsys):
    """Testa se o tabuleiro é exibido corretamente no terminal."""
    board = [
        ['X', 'O', 'X'],
        ['O', 'X', 'O'],
        ['O', 'X', 'X']
    ]

    terminal_view.display_board(board)
    captured = capsys.readouterr()

    # Remove sequências de clear/cls da saída
    output = captured.out.replace("\x1bc", "").replace("\x1b[2J\x1b[H", "")

    expected_output = (
        "    A   B   C\n"
        "1   X | O | X\n"
        "   ---+---+---\n"
        "2   O | X | O\n"
        "   ---+---+---\n"
        "3   O | X | X\n"
    )

    assert output == expected_output


def test_display_message(terminal_view, capsys):
    """Testa a exibição de mensagens no terminal."""
    message = "O jogo terminou em empate!"
    terminal_view.display_message(message)

    captured = capsys.readouterr()
    assert captured.out == message + "\n"


@patch("builtins.input", side_effect=["B2"])
def test_get_move(mock_input, terminal_view):
    """Testa a captura de movimento do jogador."""
    move = terminal_view.get_move()
    assert move == "B2"


@patch("builtins.input", side_effect=["a11", "1a1", "B2"])
def test_get_move_invalid_input(mock_input, terminal_view):
    """Testa se entradas inválidas são retornadas como string crua,
    e a última válida é aceita corretamente."""
    move1 = terminal_view.get_move()
    move2 = terminal_view.get_move()
    move3 = terminal_view.get_move()

    assert move1 == "A11"   # inválido, mas string crua
    assert move2 == "1A1"   # inválido, mas string crua
    assert move3 == "B2"    # válido, string crua
