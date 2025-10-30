# messages.py

# Mensagens gerais
TURN = "Vez do jogador {player}"
WINNER = "Parabéns! O jogador {winner} venceu!"
DRAW = "O jogo terminou em empate!"

# Mensagens de erro
# → {notation} é sempre a string digitada pelo jogador (ex.: "A2", "x9")
# → {coords} é o índice (row,col) calculado pelo parser (pode ser válido ou fora dos limites)
INVALID_INPUT = "Jogada inválida: {notation}. Use A1, 1A, B2, etc."
INVALID_MOVE_OUT_OF_BOUNDS = "Posição, {coords} = {notation}, fora dos limites. Tente novamente!"
INVALID_MOVE_OCCUPIED = "Essa posição, {coords} = {notation}, já está ocupada. Escolha outra!"
