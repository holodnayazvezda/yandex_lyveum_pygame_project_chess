import King
from Figure import Figure
from config import NORMAL_MOVE, TAKE_MOVE


class Knight(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'Knight')  # вызываем конструктор родительского класса

    @staticmethod
    def char():
        return 'N'

    def can_move(self, row1, col1, board):  # board - это объект класса Board, а board.board - это двумерный массив
        # клеток
        if (not 0 <= row1 < 8 and 0 <= col1 < 8) or (row1 == self.row and col1 == self.col):
            return [False]
        to_return = [False]
        if (board.board[row1][col1] is None or board.board[row1][col1].color != self.color) and not\
                isinstance(board.board[row1][col1], King.King):
            if (self.row + 2, self.col + 1) == (row1, col1) \
                    and 0 <= self.row + 2 < 8 and 0 <= self.col + 1 < 8:
                to_return[0] = True
            if (self.row + 2, self.col - 1) == (row1, col1) \
                    and 0 <= self.row + 2 < 8 and 0 <= self.col - 1 < 8:
                to_return[0] = True
            if (self.row - 2, self.col + 1) == (row1, col1) \
                    and 0 <= self.row - 2 < 8 and 0 <= self.col + 1 < 8:
                to_return[0] = True
            if (self.row - 2, self.col - 1) == (row1, col1) \
                    and 0 <= self.row - 2 < 8 and 0 <= self.col - 1 < 8:
                to_return[0] = True
            if (self.row + 1, self.col + 2) == (row1, col1) \
                    and 0 <= self.row + 1 < 8 and 0 <= self.col + 2 < 8:
                to_return[0] = True
            if (self.row - 1, self.col + 2) == (row1, col1) \
                    and 0 <= self.row - 1 < 8 and 0 <= self.col + 2 < 8:
                to_return[0] = True
            if (self.row + 1, self.col - 2) == (row1, col1) \
                    and 0 <= self.row + 1 < 8 and 0 <= self.col - 2 < 8:
                to_return[0] = True
            if (self.row - 1, self.col - 2) == (row1, col1) \
                    and 0 <= self.row - 1 < 8 and 0 <= self.col - 2 < 8:
                to_return[0] = True
            if to_return[0]:
                if board.board[row1][col1] is not None:
                    to_return.append(TAKE_MOVE)
                else:
                    to_return.append(NORMAL_MOVE)
        return to_return
