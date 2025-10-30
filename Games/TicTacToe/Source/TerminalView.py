import os


class TerminalView:
    def __init__(self, controller):
        self.controller = controller
        # Inscreve callbacks
        controller.on_message.subscribe(self.display_message)
        controller.on_board_update.subscribe(self.display_board)
        controller.on_game_over.subscribe(self.cleanup)

    def display_board(self, board):
        # Limpa a tela antes de redesenhar
        os.system('cls' if os.name == 'nt' else 'clear')

        print("    A   B   C")
        for i, row in enumerate(board, start=1):
            print(f"{i}   {' | '.join(row)}")
            if i < 3:
                print("   ---+---+---")

    def display_message(self, message):
        print(message)

    def get_move(self):
        return input("Digite sua jogada (ex: A1, 1a, B2): ").strip().upper()

    def cleanup(self, *args, **kwargs):
        print("Fim de jogo.")
