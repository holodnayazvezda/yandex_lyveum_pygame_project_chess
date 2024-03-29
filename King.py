# файл в котором реализуется логика шахматной фигуры "Король"

from Figure import Figure
from config import NORMAL_MOVE, TAKE_MOVE, CASTLING_MOVE
from Rook import Rook


class King(Figure):  # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'King')  # вызываем конструктор родительского класса

    @staticmethod
    def char():
        return 'K'

    def can_move(self, row1, col1, board):  # функция для проверки, может ли король ходить в клетку row1, col1
        if not 0 <= row1 < 8 and 0 <= col1 < 8:
            return [False]
        if (board.board[row1][col1] is None or board.board[row1][col1].color != self.color) and not isinstance(
                board.board[row1][col1],
                King):
            # проверка состоит из черех частей: 1)) не выходит ли за границы доски, 2) не пытается ли ходить на клетку с
            # фигурой того же цвета, 3) не пытается ли ходить на клетку с королем (это уже реализовано в условие выше)
            # далее необходимо проверить: 2)) находится в ли непосредственно король рядом с этой клеткой
            # 3)) нет ли в радиусе одной клетке короля другого цвета
            # 4)) не находится ли клетка под боем
            # TODO: здесь очень странные при вызове check_check проблемы
            # реализация проверки рокировки
            if not self.was_move():
                if row1 == self.row:
                    if col1 == self.col + 2:
                        if type(board.board[self.row][self.col + 3]) == Rook and not \
                                board.board[self.row][self.col + 3].was_move():
                            if board.board[self.row][self.col + 1] is None and \
                                    board.board[self.row][self.col + 2] is None:
                                if not board.under_attack(self.row, self.col + 1, self.color) and not \
                                        board.under_attack(self.row, self.col + 2, self.color):
                                    return [True, CASTLING_MOVE]
                    elif col1 == self.col - 2:
                        if type(board.board[self.row][self.col - 4]) == Rook and not \
                                board.board[self.row][self.col - 4].was_move():
                            if board.board[self.row][self.col - 1] is None and board.board[self.row][self.col - 2] is \
                                    None and board.board[self.row][self.col - 3] is None:
                                if not board.under_attack(self.row, self.col - 1, self.color) and not \
                                        board.under_attack(self.row, self.col - 2, self.color) and not \
                                        board.under_attack(self.row, self.col - 3, self.color):
                                    return [True, CASTLING_MOVE]
            # проверка 2)) и 3))
            flag = False
            for i in [1, 0, -1]:  # коэффиценты для прибавления к row
                for j in [1, 0, -1]:  # коэффиценты для прибавления к col
                    try:
                        if row1 + i == self.row and col1 + j == self.col:  # если клетка рядом с королем (+- 1 клетка
                            # по всем осям)
                            if not board.under_attack(row1, col1, self.color):  # если клетка не атакуется (при ходе
                                # на нее не будет шаха)
                                # если клетка пустая или на ней фигура другого цвета
                                if board.board[row1][col1] is None or board.board[row1][col1].color != self.color:
                                    flag = True
                    except IndexError:
                        pass
            if flag:
                if board.board[row1][col1] is None:
                    return [True, NORMAL_MOVE]
                else:
                    return [True, TAKE_MOVE]
        return [False]
