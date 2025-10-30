from Source.TicTacToeModel import TicTacToeModel
from Source.TicTacToeController import TicTacToeController
from Source.TerminalView import TerminalView
from Source.TkInterView import TkInterView
import tkinter as tk

def main():
    print("Escolha o modo de exibição:")
    print("1 - Terminal")
    print("2 - Tkinter (interface gráfica)")
    choice = input("Digite sua escolha (1 ou 2): ").strip()

    model = TicTacToeModel()
    controller = TicTacToeController(model)

    # -----------------------------
    # 🔹 MODO TERMINAL
    # -----------------------------
    if choice == "1":
        view = TerminalView(controller)

        controller.on_message.notify("Iniciando jogo da velha (modo terminal)!")
        controller.on_board_update.notify(model.board)

        running = True

        def stop_game(*args, **kwargs):
            nonlocal running
            running = False

        controller.on_game_over.subscribe(stop_game)

        while running:
            move = view.get_move()
            controller.play_turn(move)

    # -----------------------------
    # 🔹 MODO TKINTER
    # -----------------------------
    elif choice == "2":
        root = tk.Tk()
        view = TkInterView(controller, root)

        controller.on_message.notify("Iniciando jogo da velha (modo gráfico)!")
        controller.on_board_update.notify(model.board)

        def stop_game(*args, **kwargs):
            root.after(1000, root.destroy)  # Fecha após 1s

        root.mainloop()

    # -----------------------------
    # 🔹 OPÇÃO INVÁLIDA
    # -----------------------------
    else:
        print("Opção inválida! Execute novamente e escolha 1 ou 2.")

if __name__ == "__main__":
    main()