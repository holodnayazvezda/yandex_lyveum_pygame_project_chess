# файл в котором реализуется логика шахматной фигуры "Ферзь" (Королева)

from Figure import Figure
from config import TAKE_MOVE, NORMAL_MOVE
import King


class Queen(Figure):  # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'Queen')  # вызываем конструктор родительского класса

    @staticmethod
    def char():
        return 'Q'

    def can_move(self, row1, col1, board):  # board - это объект класса board, а board.board - это двумерный массив
        # клеток
        if not (0 <= row1 < 8 and 0 <= col1 < 8):
            return [False]
        if self.row == row1 and self.col == col1:
            return [False]
        to_return = [False]
        if (board.board[row1][col1] is None or board.board[row1][col1].color != self.color) and not \
                isinstance(board.board[row1][col1], King.King):
            can = []
            for x in range(self.row + 1, 8):
                d = board.board[x][self.col]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, self.col))
                        break
                    break
                can.append((x, self.col))
            for x in range(self.row - 1, -1, -1):
                d = board.board[x][self.col]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, self.col))
                        break
                    break
                can.append((x, self.col))
            for y in range(self.col + 1, 8):
                d = board.board[self.row][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((self.row, y))
                        break
                    break
                can.append((self.row, y))
            for y in range(self.col - 1, -1, -1):
                d = board.board[self.row][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((self.row, y))
                        break
                    break
                can.append((self.row, y))
            # диагонали
            x, y = self.row, self.col
            while x < 7 and y < 7:
                x, y = x + 1, y + 1
                d = board.board[x][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, y))
                        break
                    break
                can.append((x, y))
            x, y = self.row, self.col
            while x < 7 and y > 0:
                x, y = x + 1, y - 1
                d = board.board[x][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, y))
                        break
                    break
                can.append((x, y))
            x, y = self.row, self.col
            while x > 0 and y < 7:
                x, y = x - 1, y + 1
                d = board.board[x][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, y))
                        break
                    break
                can.append((x, y))
            x, y = self.row, self.col
            while x > 0 and y > 0:
                x, y = x - 1, y - 1
                d = board.board[x][y]
                if d:
                    if d.get_color() == self.get_color():
                        break
                    elif d.get_color() != self.get_color():
                        can.append((x, y))
                        break
                    break
                can.append((x, y))

            if (row1, col1) in can:
                to_return[0] = True
                if board.board[row1][col1] is not None:
                    to_return.append(TAKE_MOVE)
                else:
                    to_return.append(NORMAL_MOVE)
        return to_return
