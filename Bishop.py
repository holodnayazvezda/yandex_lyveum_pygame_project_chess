# файл в котором реализуется логика шахматной фигуры "слон"

from Figure import Figure
import King
from config import NORMAL_MOVE, TAKE_MOVE


class Bishop(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'Bishop')  # вызываем конструктор родительского класса

    @staticmethod
    def char():
        return 'B'

    def can_move(self, row1, col1, board):  # board - это объект класса board, а board.board - это двумерный массив
        # клеток
        if (not 0 <= row1 < 8 and 0 <= col1 < 8) or (row1 == self.row and col1 == self.col):
            return [False]
        to_return = [False]
        if (board.board[row1][col1] is None or board.board[row1][col1].color != self.color) and not \
                isinstance(board.board[row1][col1], King.King):
            x, y = self.row, self.col
            dop = []
            while x >= 0 and y <= 7:
                x -= 1
                y += 1
                if x >= 0 and y <= 7:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not \
                            isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            while x >= 0 and y >= 0:
                x -= 1
                y -= 1
                if x >= 0 and y >= 0:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not \
                            isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            while x <= 7 and y <= 7:
                x += 1
                y += 1
                if x <= 7 and y <= 7:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not \
                            isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            while x <= 7 and y >= 0:
                x += 1
                y -= 1
                if x <= 7 and y >= 0:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not \
                            isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            if (row1, col1) in dop:
                to_return[0] = True
                if board.board[row1][col1] is not None:
                    to_return.append(TAKE_MOVE)
                else:
                    to_return.append(NORMAL_MOVE)
        return to_return
