class Rook:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def move(self):
        self.has_moved = True

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        color = board.get_piece(row, col).get_color()
        if row != row1 and col != col1:
            return False

        if row == row1 and col == col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        if board.get_piece(row1, col1) is not None:
            return board.get_piece(row1, col1).get_color() == opponent(color)
        return True
