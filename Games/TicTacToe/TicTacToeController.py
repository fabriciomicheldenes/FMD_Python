class TicTacToeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.playError = False
        self.errorMessage = " "

    def play_game(self):
        """Gerencia o loop principal do jogo"""
        try:
            while True:
                # Style.RESET_ALL
                # {Fore.BLUE if self.model.current_player == "X" else Fore.MAGENTA}
                # {Style.RESET_ALL}
                self.view.display_board(self.model.board)
                self.view.display_message(
                    f"Vez do jogador {self.model.current_player}")
                if (self.playError):  # caso uma jogada errada tenha ocorrido
                    # imprime a mensagem indicando do erro
                    self.view.display_message(self.errorMessage)
                playError = False

                # Obter jogada do jogador
                move = self.view.get_move()
                if not move:
                    self.view.display_message(
                        "Jogada inválida. Tente novamente.")
                    continue
                row, col = move

                if not (0 <= row < 3 and 0 <= col < 3):
                    self.playError = True
                    self.errorMessage = f"A posição {
                        move} está fora dos limites. Tente novamente!"
                    continue

                if not self.model.make_move(row, col):
                    self.playError = True
                    self.errorMessage = f"A posição {
                        move} já está ocupada. Escolha outra!"
                    continue

                # Verifica vitória ou empate
                winner = self.model.check_winner()
                if winner:
                    self.view.display_board(self.model.board)
                    self.view.display_message(
                        f"Parabéns! O jogador {winner} venceu!")
                    break

                if self.model.is_draw():
                    print("Empate detectado no Controller.")
                    self.view.display_board(self.model.board)
                    self.view.display_message("O jogo terminou em empate!")
                    break

                # Alterna jogador
                self.model.switch_player()

        finally:
            if hasattr(self.view, "cleanup"):
                self.view.cleanup()
