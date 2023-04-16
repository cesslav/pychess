# chess v0.0.1


WHITE = 1
BLACK = 2


def main():
    board = Board()
    while True:

        board.print_board(board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    <row> <col> <row1> <row1>     -- ход из клетки (col, row)')
        print('                                          в клетку (col1, row1)')
        print('                                          через пробел напишите ')
        print('                                          координаты начальной и конечной клеток')
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        col, row, col1, row1 = command.split()
        col, row, col1, row1 = board.lit.index(col), int(row) - 1, board.lit.index(col1), int(row1) - 1
        if board.move_piece(row, col, row1, col1):
            print('Успешно')
        else:
            print('Неверный ввод')


class Board:
    def __init__(self):
        self.lit = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def opponent(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def print_board(self, board):
        print('     +----+----+----+----+----+----+----+----+')
        for row in range(8, 0, -1):
            print(' ', row, end='  ')
            for col in range(1, 9):
                print('|', board.cell(row - 1, col - 1), end=' ')
            print('|')
            print('     +----+----+----+----+----+----+----+----+')
        print(end='        ')
        for col in range(1, 9):
            print(self.lit[col - 1], end='    ')
        print()

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if 1 <= row < 9 and 1 <= col < 9:
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        if not 1 <= row < 9 and 1 <= col < 9 or not 1 <= row1 < 9 and 1 <= col1 < 9:
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if piece.__class__.__name__ in {'Rook', 'King'}:
            piece.move()
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = self.opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if self.field[row][col].char() != 'P':
            return False
        piece = self.field[row][col]
        color = self.field[row][col].get_color()
        if piece.can_move(self, row, col, row1, col1) \
                or piece.can_attack(self, row, col, row1, col1):
            self.move_piece(row, col, row1, col1)
            if char == 'Q':
                self.field[row1][col1] = Queen(color)
            elif char == 'R':
                self.field[row1][col1] = Rook(color)
            elif char == 'B':
                self.field[row1][col1] = Bishop(color)
            elif char == 'N':
                self.field[row1][col1] = Knight(color)
            return True
        return False

    def castling0(self):
        if self.color == WHITE:
            if self.field[0][0] is None:
                return False
            if self.field[0][0].char() != 'R':
                return False
            if self.field[0][0].has_moved:
                return False
            if self.field[0][4] is None:
                return False
            if self.field[0][4].char() != 'K':
                return False
            if self.field[0][4].has_moved:
                return False
            if self.field[0][0].can_move(self, 0, 0, 0, 3):
                if self.field[0][3] is not None:
                    return False
                self.move_piece(0, 0, 0, 3)
                self.color = self.opponent(self.color)
                self.move_piece(0, 4, 0, 2)
                return True
        else:
            if self.field[7][0] is None:
                return False
            if self.field[7][0].char() != 'R':
                return False
            if self.field[7][0].has_moved:
                return False
            if self.field[7][4] is None:
                return False
            if self.field[7][4].char() != 'K':
                return False
            if self.field[7][4].has_moved:
                return False
            if self.field[7][0].can_move(self, 7, 0, 7, 3):
                if self.field[7][3] is not None:
                    return False
                self.move_piece(7, 0, 7, 3)
                self.color = self.opponent(self.color)
                self.move_piece(7, 4, 7, 2)
                return True
        return False

    def castling7(self):
        if self.color == WHITE:
            if self.field[0][7] is None:
                return False
            if self.field[0][7].char() != 'R':
                return False
            if self.field[0][7].has_moved:
                return False
            if self.field[0][4] is None:
                return False
            if self.field[0][4].char() != 'K':
                return False
            if self.field[0][4].has_moved:
                return False
            if self.field[0][7].can_move(self, 0, 7, 0, 5):
                if self.field[0][5] is not None:
                    return False
                self.move_piece(0, 7, 0, 5)
                self.color = self.opponent(self.color)
                self.move_piece(0, 4, 0, 6)
                return True
        else:
            if self.field[7][7] is None:
                return False
            if self.field[7][7].char() != 'R':
                return False
            if self.field[7][7].has_moved:
                return False
            if self.field[7][4] is None:
                return False
            if self.field[7][4].char() != 'K':
                return False
            if self.field[7][4].has_moved:
                return False
            if self.field[7][7].can_move(self, 7, 7, 7, 5):
                if self.field[7][5] is not None:
                    return False
                self.move_piece(7, 7, 7, 5)
                self.color = self.opponent(self.color)
                self.move_piece(7, 4, 7, 6)
                return True
        return False

    def __str__(self):
        print('     +----+----+----+----+----+----+----+----+')
        for row in range(8, 0, -1):
            print(' ', row, end='  ')
            for col in range(1, 9):
                print('|', self.cell(row - 1, col - 1), end=' ')
            print('|')
            print('     +----+----+----+----+----+----+----+----+')
        print(end='        ')
        for col in range(1, 9):
            print(col, end='    ')
        print()


class Rook:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def move(self):
        self.has_moved = True

    def opponent(color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

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
            return board.get_piece(row1, col1).get_color() == self.opponent(color)
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def opponent(color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1:
            return board.get_piece(row1, col1) is None
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return board.get_piece(row1, col1) is None
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        if (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1)):
            return board.get_piece(row1, col1).get_color() == self.opponent(self.color)


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def get_color(self):
        return self.color

    def move(self):
        self.has_moved = True

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def opponent(color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        color = board.get_piece(row, col).get_color()
        if abs(row1 - row) == abs(col1 - col) and (row1 != row or col1 != col) \
                or row1 == row and col1 != col or row1 != row and col1 == col:
            row_step = row1 - row
            if row_step != 0:
                row_step //= abs(row_step)
            col_step = col1 - col
            if col_step != 0:
                col_step //= abs(col_step)
            if row_step != 0:
                cur_col = col
                for cur_row in range(row + row_step, row1, row_step):
                    cur_col += col_step
                    if board.get_piece(cur_row, cur_col) is not None:
                        return False
            else:
                cur_row = row
                for cur_col in range(col + col_step, col1, col_step):
                    cur_row += row_step
                    if board.get_piece(cur_row, cur_col) is not None:
                        return False
            if board.get_piece(row1, col1) is not None:
                return board.get_piece(row1, col1).get_color() == self.opponent(color)
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


main()
