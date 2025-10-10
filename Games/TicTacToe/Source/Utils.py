import re


def to_notation(row, col):
    """Converte (row, col) em notação de tabuleiro tipo A1"""
    col_letter = chr(ord('A') + col)
    row_number = row + 1
    return f"{col_letter}{row_number}"


def from_notation(text: str):
    """
    Converte notação 'A1'/'1A' (case-insensitive, com ou sem espaços) para (row, col) 0-based.
    Retorna (row, col, status) onde status pode ser:
        - "valid": dentro dos limites
        - "out_of_bounds": formato válido mas fora do tabuleiro
    Levanta ValueError se o formato for inválido.
    """
    if not text:
        raise ValueError("Entrada vazia.")

    s = text.strip().upper()

    # Aceita formatos LE+NU ou NU+LE, mas só uma letra e um número
    pattern = r"^([A-Z])([0-9])$|^([0-9])([A-Z])$"
    m = re.fullmatch(pattern, s)
    if not m:
        raise ValueError("Formato inválido. Use A1 ou 1A.")

    if m.group(1) and m.group(2):  # "A1"
        col_letter = m.group(1)
        row_number = m.group(2)
    else:                          # "1A"
        row_number = m.group(3)
        col_letter = m.group(4)

    col = ord(col_letter) - ord('A')
    row = int(row_number) - 1

    # Dentro do tabuleiro?
    if 0 <= row < 3 and 0 <= col < 3:
        return row, col, "valid"
    else:
        return row, col, "out_of_bounds"
