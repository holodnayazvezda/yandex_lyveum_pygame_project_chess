from Figure import Figure
import King
from config import NORMAL_MOVE, TAKE_MOVE


class Rook(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'Rook')  # вызываем конструктор родительского класса

    def char(self):
        return 'R'

    def can_move(self, row, col, board=None):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if not 0 <= row < 8 and 0 <= col < 8:
            return [False]
        to_return = [False]
        if (board[row][col] is None or board[row][col].color != self.color) and not isinstance(board[row][col],
                                                                                               King.King):
            x, y = self.row, self.col
            dop = []
            while x <= 7:
                x += 1
                if x <= 7 and y <= 7:
                    if (board[x][y] is None or board[x][y].color != self.color) and not isinstance(board[x][y], King.King):
                        dop.append((x, y))
                        if board[x][y] is not None:
                            break
                    else:
                        break
            while y <= 7:
                y += 1
                if x <= 7 and y <= 7:
                    if (board[x][y] is None or board[x][y].color != self.color) and not isinstance(board[x][y],
                                                                                                   King.King):
                        dop.append((x, y))
                        if board[x][y] is not None:
                            break
                    else:
                        break
            if (row, col) in dop:
                to_return[0] = True
                if board[row][col] is not None:
                    to_return.append(TAKE_MOVE)
                else:
                    to_return.append(NORMAL_MOVE)
        return to_return
