from Source.TicTacToeModel import TicTacToeModel
from Source.TicTacToeController import TicTacToeController
from Source.TerminalView import TerminalView

def main():
    model = TicTacToeModel()
    controller = TicTacToeController(model)
    view = TerminalView(controller)

    controller.on_message.notify("Iniciando jogo da velha!")
    controller.on_board_update.notify(model.board)

    running = True

    def stop_game():
        nonlocal running
        running = False
    controller.on_game_over.subscribe(stop_game)

    while running:
        move = view.get_move()
        controller.play_turn(move)

if __name__ == "__main__":
    main()