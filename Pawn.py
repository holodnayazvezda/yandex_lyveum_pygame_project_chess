from Figure import Figure
from config import NORMAL_MOVE, TAKE_MOVE, CONVERSION_MOVE, WHITE, PASSED_TAKE_MOVE
import King


class Pawn(Figure):   # наследуемся от класса Sprite для того, чтобы хранить объекты в самом себе.
    def __init__(self, row, col, color):
        Figure.__init__(self, row, col, color, "Pawn")  # вызываем конструктор родительского класса

    @staticmethod
    def char():
        return 'P'

    def can_move(self, row, col, board):  # board - это объект класса Board, а board.board - это двумерный массив клеток
        if (not 0 <= row < 8 and 0 <= col < 8) or (row == self.row and col == self.col):  # проверка на то, что ход
            # не за пределы доски
            return [False]
        to_return = [False]
        if self.color == WHITE:
            start_row = 1
            direction = 1
            transformation_row = 7
        else:
            start_row = 6
            direction = -1
            transformation_row = 0
        # создаем обычные ходы и ход конверсию (превращение пешки в другую фигуру) при обычнои ходе без взятия
        if (row == self.row + direction or (row == self.row + (direction * 2) and self.row == start_row and
                                            board.board[self.row + direction][col] is None)) and col == self.col and \
                board.board[row][col] is None:  # 1 проверка на то, что ход вперед и на клетки нет другой фигуры
            to_return[0] = True
            if row != transformation_row:
                to_return.append(NORMAL_MOVE)
            else:
                to_return.append(CONVERSION_MOVE)
        # создаем ходы взятия и ход конверсию (превращение пешки в другую фигуру) при взятии
        if row == self.row + direction and (col == self.col + 1 or col == self.col - 1) and \
                board.board[row][col] is not None and board.board[row][col].color != self.color:  # проверка на то,
            # что ход на 1 клетку вперед и в бок. Также проверка на то, что на клетке есть фигура и она
            # противоположного цвета
            to_return[0] = True
            if row != transformation_row:
                to_return.append(TAKE_MOVE)
            else:
                to_return.append(CONVERSION_MOVE)
        # создаем ход - взятие на проходе
        if row == self.row + direction and (col == self.col + 1 or col == self.col - 1) and \
                board.board[row][col] is None and board.board[self.row][col] is not None and \
                board.board[self.row][col].color != self.color and \
                board.board[self.row][col].name == "Pawn" and board.board[self.row][col] == \
                board.all_moves[-1].figure and abs(board.all_moves[-1].row - board.all_moves[-1].basic_row) == 2:
            # Проверка на то, что ход на 1 клетку вперед и в бок. Также проверка на то, что на клетке есть фигура и она
            # противоположного цвета и это пешка, которая сделала ход на 2 клетки вперед и это последний ход
            to_return[0] = True
            to_return.append(PASSED_TAKE_MOVE)
        return to_return
