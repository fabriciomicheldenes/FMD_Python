import tkinter as tk
from Source.Utils import to_notation


class TkInterView:
    def __init__(self, controller, root=None):
        self.controller = controller
        self.root = root or tk.Tk()
        self.root.title("Jogo da Velha (TkinterView)")

        # ========================
        # 🔹 CABEÇALHO E MENSAGENS
        # ========================
        self.message_label = tk.Label(
            self.root, text="Bem-vindo ao Jogo da Velha!",
            font=("Arial", 14)
        )
        self.message_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # ========================
        # 🔹 GRADE DE BOTÕES
        # ========================
        self.buttons = []
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 18),
                    width=5,
                    height=2,
                    command=lambda r=r, c=c: self.on_cell_click(r, c)
                )
                btn.grid(row=r + 1, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # ========================
        # 🔹 BOTÕES DE CONTROLE
        # ========================
        self.new_game_btn = tk.Button(
            self.root, text="Novo Jogo", font=("Arial", 12),
            command=self.new_game
        )
        self.new_game_btn.grid(row=4, column=0, pady=(10, 10))

        self.exit_btn = tk.Button(
            self.root, text="Sair", font=("Arial", 12),
            command=self.root.destroy
        )
        self.exit_btn.grid(row=4, column=2, pady=(10, 10))

        # ========================
        # 🔹 EVENTOS DO CONTROLLER
        # ========================
        controller.on_board_update.subscribe(self.update_board)
        controller.on_message.subscribe(self.display_message)
        controller.on_game_over.subscribe(self.game_over)

    # ------------------------------
    # 🔹 CALLBACKS
    # ------------------------------
    def on_cell_click(self, row, col):
        """Chamado quando o jogador clica em uma célula."""
        move_str = to_notation(row, col)
        self.controller.play_turn(move_str)

    def new_game(self):
        """Reinicia o tabuleiro e o modelo."""
        self.controller.reset_game()
        self.display_message("Novo jogo iniciado!")
        self.update_board(self.controller.model.board)
        for row in self.buttons:
            for btn in row:
                btn.config(state="normal")

    # ------------------------------
    # 🔹 MÉTODOS DE INTERFACE
    # ------------------------------
    def update_board(self, board):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = board[r][c]

    def display_message(self, message):
        self.message_label.config(text=message)

    def game_over(self, winner=None):
        """Desativa o tabuleiro e mostra o vencedor."""
        # Desativa apenas os botões do tabuleiro
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

        if winner:
            self.display_message(f"Parabéns! O jogador {winner} venceu!")
        else:
            self.display_message("O jogo terminou em empate!")

        # Mantém 'Novo Jogo' e 'Sair' ativos
        self.new_game_btn.config(state="normal")
        self.exit_btn.config(state="normal")
