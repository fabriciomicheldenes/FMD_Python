from Source.TkInterView import TkInterView
from unittest.mock import MagicMock, patch
import tkinter as tk
import pytest
import os
os.environ["TCL_LIBRARY"] = r"E:\Python312\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"E:\Python312\tcl\tk8.6"


@pytest.fixture(scope="session")
def tk_root():
    """
    Cria uma instância única de Tk para todos os testes.
    - Localmente: usa Tk real (janela oculta).
    - CI/CD ou headless: se falhar, usa mock de Tk.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # mantém a janela oculta
        yield root
        root.destroy()
    except tk.TclError:
        # Fallback para ambientes sem GUI (ex.: GitHub Actions)
        with patch("tkinter.Tk") as MockTk:
            root = MockTk()
            yield root


def test_tkinter_view_initialization(tk_root):
    """Testa se a TkInterView inicializa sem erros."""
    fake_controller = MagicMock()
    view = TkInterView(fake_controller, root=tk_root)

    assert isinstance(view, TkInterView)
    assert view.root is tk_root


def test_update_board(tk_root):
    """Testa se o tabuleiro é atualizado ao receber evento."""
    fake_controller = MagicMock()
    view = TkInterView(fake_controller, root=tk_root)

    # Simula tabuleiro
    board = [
        ["X", "O", ""],
        ["", "X", "O"],
        ["O", "", "X"]
    ]

    # Chama método que deveria atualizar os botões
    view.update_board(board)

    # Verifica se os textos dos botões foram atualizados
    assert view.buttons[0][0]["text"] == "X"  # A1
    assert view.buttons[0][1]["text"] == "O"  # B1
    assert view.buttons[2][2]["text"] == "X"  # C3


def test_display_message(tk_root):
    """Testa se mensagens são exibidas no label."""
    fake_controller = MagicMock()
    view = TkInterView(fake_controller, root=tk_root)

    view.display_message("Vez do jogador X")
    assert "Vez do jogador X" in view.message_label["text"]


def test_game_over_disables_buttons(tk_root):
    """Testa se os botões são desabilitados quando o jogo termina."""
    fake_controller = MagicMock()
    view = TkInterView(fake_controller, root=tk_root)

    # Simula fim de jogo
    view.game_over()

    for row in view.buttons:
        for btn in row:
            assert btn["state"] == "disabled"
