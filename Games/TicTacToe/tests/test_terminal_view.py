import pytest
from unittest.mock import patch
from TerminalView import TerminalView


@pytest.fixture
def terminal_view():
    """Fixture para instanciar o TerminalView."""
    return TerminalView()


def test_display_board(terminal_view, capsys):
    """Testa se o tabuleiro é exibido corretamente no terminal."""
    # Configuração de um tabuleiro de exemplo
    board = [
        ['X', 'O', 'X'],
        ['O', 'X', 'O'],
        ['O', 'X', 'X']
    ]

    # Exibe o tabuleiro
    terminal_view.display_board(board)

    # Captura a saída do terminal
    captured = capsys.readouterr()

    print(captured)

    # Verifica se o tabuleiro foi impresso corretamente
    expected_output = (
        'X | O | X\n'
        '---+---+---\n'
        'O | X | O\n'
        '---+---+---\n'
        'O | X | X\n'
    )
    assert captured.out == expected_output


def test_display_message(terminal_view, capsys):
    """Testa a exibição de mensagens no terminal."""
    message = "O jogo terminou em empate!"
    terminal_view.display_message(message)

    # Captura a saída do terminal
    captured = capsys.readouterr()

    # Verifica se a mensagem foi exibida corretamente
    assert captured.out == message + "\n"


@patch("builtins.input", side_effect=[0, 1])  # Simula entrada do jogador
def test_get_move(mock_input, terminal_view):
    """Testa a captura de movimento do jogador."""
    move = terminal_view.get_move()

    # Verifica se a entrada foi interpretada corretamente
    assert move == (0, 1)


# Simula entradas inválida, inválida e válida
@patch("builtins.input", side_effect=["a", 1, 1, 1])
def test_get_move_invalid_input(mock_input, capfd):
    """Testa se o método get_move lida corretamente com entradas inválidas e exibe mensagem de erro."""
    terminal_view = TerminalView()

    move = terminal_view.get_move()

    # Captura a saída padrão (stdout)
    captured = capfd.readouterr()
    print(captured)

    # Verifica se a mensagem de erro foi exibida
    assert "Entrada inválida! Digite números inteiros." in captured.out

    # Verifica se a entrada válida foi capturada corretamente
    assert move == (1, 1)
