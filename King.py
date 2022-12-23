from Figure import Figure
from config import NORMAL_MOVE, TAKE_MOVE, CASTLING_MOVE


class King(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'King')  # вызываем конструктор родительского класса

    def char(self):
        return 'K'

    def can_move(self, row1, col1, board):
        if not 0 <= row1 < 8 and 0 <= col1 < 8:
            return [False]
        if (board[row1][col1] is None or board[row1][col1].color != self.color) and not isinstance(board[row1][col1],
                                                                                                   King):
            # проверка состоит из черех частей: 1)) не выходит ли за границы доски, 2) не пытается ли ходить на клетку с
            # фигурой того же цвета, 3) не пытается ли ходить на клетку с королем (это уже реализовано в условие выше)
            # далее необходимо проверить: 2)) находится в ли непосредственно король рядом с этой клеткой
            # 3)) нет ли в радиусе одной клетке короля другого цвета
            # 4)) не находится ли клетка под боем
            # TODO: 1) реализовать рокировку и метод для проверки возможности рокировки

            # проверка 2)) и 3))
            flag = False
            for i in [1, 0, -1]:  # коэффиценты для прибавления к row
                for j in [1, 0, -1]:  # коэффиценты для прибавления к col
                    try:
                        if board[row1 + i][col1 + j] is not None and isinstance(board[row1 + i][col1 + j],  # 3))
                                                                                       King) and \
                                board[row1 + i][col1 + j].color != self.color:
                            return [False]
                        if row1 + i == self.row and col1 + j == self.col:  # 2))
                            flag = True
                    except IndexError:
                        pass
            if flag:
                if board[row1][col1] is None:
                    return [True, NORMAL_MOVE]
                else:
                    return [True, TAKE_MOVE]
                # TODO: сдесь надо проверить не находится ли клетка под боем (условие4) ПОКА НЕ РЕАЛИЗОВАНО
        return [False]
