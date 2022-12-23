from Figure import Figure
from config import NORMAL_MOVE, TAKE_MOVE, CONVERSION_MOVE, PASSED_TAKE_MOVE
import King


class Pawn(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, row, col, color):
        Figure.__init__(self, row, col, color, "Pawn")  # вызываем конструктор родительского класса

    def char(self):
        return 'P'

    def can_move(self, row, col, board=None):
        direction = -1
        start_row = 6
        # это логическое выражение проверяет базовые принципы клетки. И сразу же вернет False, если на клетке стоит
        # фигура своего же цвета или если на ней стоит король (в целом цвет не важен, любого цвета)
        # TODO: реализовать превращение пешки в другую фигуру при достижении конца доски, а также взятие на проходе
        if (board[row][col] is None or board[row][col].color != self.color) and not isinstance(board[row][col], King.King):
            # ход на 1 клетку
            if self.row + direction == row and self.col == col:
                return [True, NORMAL_MOVE]

            # ход на 2 клетки из начального положения
            if self.row == start_row and self.row + (2 * direction) == row and self.col == col:
                return [True, NORMAL_MOVE]

            try:
                if board[self.row + direction][self.col - 1] is not None and self.row + direction == row and self.col - 1 == col:
                    return [True, TAKE_MOVE]
            except Exception:
                pass

            try:
                if board[self.row + direction][self.col + 1] is not None and self.row + direction == row and self.col + 1 == col:
                    return [True, TAKE_MOVE]
            except Exception:
                pass
        return [False]
