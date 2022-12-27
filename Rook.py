from Figure import Figure
import King
from config import NORMAL_MOVE, TAKE_MOVE


class Rook(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'Rook')  # вызываем конструктор родительского класса

    def char(self):
        return 'R'

    def can_move(self, row, col, board):  # board - это объект класса board, а board.board - это двумерный массив клеток
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if (not 0 <= row < 8 and 0 <= col < 8) or (row == self.row and col == self.col):
            return [False]
        to_return = [False]
        if (board.board[row][col] is None or board.board[row][col].color != self.color) and not isinstance(board.board[row][col], King.King):
            x, y = self.row, self.col
            dop = []  # это массив, в который мы при помощи циклов будем записывать информацию о возможных ходах
            # это цикл, который проверяет возможность двигаться вправа (ОТНОСИТЕЛЬНО МАССИВА board.board)
            while x >= 0:
                x -= 1
                if x >= 0:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            # это цикл, который проверяет возможность двигаться влева (ОТНОСИТЕЛЬНО МАССИВА board.board)
            while x < 8:
                x += 1
                if x < 8:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            # это цикл, который проверяет возможность двигаться вверх (ОТНОСИТЕЛЬНО МАССИВА board.board)
            while y >= 0:
                y -= 1
                if y >= 0:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            x, y = self.row, self.col
            # это цикл, который проверяет возможность двигаться вниз (ОТНОСИТЕЛЬНО МАССИВА board.board)
            while y < 8:
                y += 1
                if y < 8:
                    if (board.board[x][y] is None or board.board[x][y].color != self.color) and not isinstance(board.board[x][y], King.King):
                        dop.append((x, y))
                        if board.board[x][y] is not None:
                            break
                    else:
                        break
            if (row, col) in dop:
                to_return[0] = True
                if board.board[row][col] is not None:
                    to_return.append(TAKE_MOVE)
                else:
                    to_return.append(NORMAL_MOVE)
        return to_return
