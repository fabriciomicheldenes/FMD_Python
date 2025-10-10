from random import choice
from Source.TicTacToeModel import TicTacToeModel
from Source.TicTacToeController import TicTacToeController
from Source.TerminalView import TerminalView
from Source.CursesView import CursesView


def main():
    model = TicTacToeModel()

    # TODO: Escolha a view (Termina, Curses, TKinter ou Qt)
    choice = input("Escolha a interface (1 = Terminal, 2 = Curses): ")
    if choice == "1 (default)":
        view = TerminalView()
    elif choice == "2":
        view = CursesView()
    else:
        view = TerminalView()

    controller = TicTacToeController(model, view)
    controller.play_game()


if __name__ == "__main__":
    main()
