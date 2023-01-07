from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from config import WHITE, BLACK, OPPONENT_COLOR, TAKE_MOVE
from TempFigure import TempFigure


class Board:
    def __init__(self):
        self.board = []
        self.all_figures = {1: [], 0: []}  # словарь всех фигур 1 - белые фигуры, 0 - черные фигуры
        self.all_moves = []  # список всех ходов, в нем лежат объекты класса Move
        self.positions = []  # список всех позиций доски объект класса list (board.board)
        # генерируем доску по рядам (затем перевернем так как 0 ряд здесь - это седьмой в игре)
        for amount_of_row in range(8):
            row = []  # ряды
            for amount_of_col in range(8):
                # теперь мы задаем фигуры на доске
                if amount_of_row == 0:  # первый ряд в игре белые фигуры
                    if amount_of_col == 0 or amount_of_col == 7:
                        row.append(Rook(0, amount_of_col, WHITE))
                    elif amount_of_col == 1 or amount_of_col == 6:
                        row.append(Knight(0, amount_of_col, WHITE))
                    elif amount_of_col == 2 or amount_of_col == 5:
                        row.append(Bishop(0, amount_of_col, WHITE))
                    elif amount_of_col == 3:
                        row.append(Queen(0, amount_of_col, WHITE))
                    elif amount_of_col == 4:
                        row.append(King(0, amount_of_col, WHITE))
                elif amount_of_row == 1:  # второй ряд в игре белые пешки
                    row.append(Pawn(1, amount_of_col, WHITE))
                elif amount_of_row == 6:  # пятый ряд в игре черные пешки
                    row.append(Pawn(6, amount_of_col, BLACK))
                elif amount_of_row == 7:  # шестой ряд в игре черные фигуры
                    if amount_of_col == 0 or amount_of_col == 7:
                        row.append(Rook(7, amount_of_col, BLACK))
                    elif amount_of_col == 1 or amount_of_col == 6:
                        row.append(Knight(7, amount_of_col, BLACK))
                    elif amount_of_col == 2 or amount_of_col == 5:
                        row.append(Bishop(7, amount_of_col, BLACK))
                    elif amount_of_col == 3:
                        row.append(Queen(7, amount_of_col, BLACK))
                    elif amount_of_col == 4:
                        row.append(King(7, amount_of_col, BLACK))
                else:
                    row.append(None)
            # добавляем ряд в доску
            self.board.append(row)
            # теперь записываем все фигуры из ряда в словарь всех фигур
            for figure in row:
                if figure:
                    self.all_figures[figure.color].append(figure)

    def get_figure(self, row, col):
        return self.board[row][col]

    def get_king(self, color):
        for figure in self.all_figures[color]:
            if isinstance(figure, King):
                return figure

    def check_kings_around(self, row, col, color):   # это функция для проверки, ести ли в радиусе +-=1 клетки.
        # Возвращает True, если есть
        for row_coefficent in [1, 0, -1]:
            for col_coefficent in [1, 0, -1]:
                new_row = row + row_coefficent
                new_col = col + col_coefficent
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    try:
                        if self.board[new_row][new_col] is not None:  # проверка на то, что клетка не пустая
                            if self.board[new_row][new_col].name == 'King' and \
                                    self.board[new_row][new_col].color != color:  # проверка на то, что в клетке
                                # король другого цвета
                                return True
                    except IndexError:
                        pass
        return False

    def under_attack(self, row, col, color):  # проврерка на атаку клетки с координатами row, col цветом color
        current_figure = self.board[row][col]  # запоминаем фигуру, которая стоит на клетке
        self.board[row][col] = TempFigure(row, col, color)  # ставим временную фигуру на клетку, для адекватной
        # проверки на атаку
        for figure in self.all_figures[OPPONENT_COLOR[color]]:
            if type(figure) != King:
                result = figure.can_move(row, col, self)  # возвращает массив - первый элемент - булевое значение (может
            else:
                result = [0]  # один элемент для общей проверки
            # ходить или нет), а второ1 - тип хода
            if result[0] or self.check_kings_around(row, col, color):  # если фигура может ходить на клетку или
                # король может ходить на клетку
                self.board[row][col] = current_figure
                return True
        self.board[row][col] = current_figure
        return False

    def check_check(self, color):
        king = self.get_king(color)
        # вызвать under_attack для всех фигур противника
        return self.under_attack(king.row, king.col, color)

    def check_triple_repetition_of_a_position(self):  # проверка на тройное повторение позиции (по правилам шахмат
        # если одинаковая позиция повторилась 3 раза, то автоматически ничья)
        last_position = self.positions[-1]
        count = 0
        for position in self.positions[:-1]:
            match_counter = 0
            for pos in zip(last_position, position):  # сравниваем две позиции 0 - текущая, 1 - предыдущая
                # print(pos)
                if pos[0] is None and pos[1] is None:
                    match_counter += 1
                elif pos[0] is not None and pos[1] is not None:
                    if pos[0].color == pos[1].color and pos[0].name == pos[1].name:
                        match_counter += 1
            if match_counter == 64:
                count += 1
        if count == 2:
            return True
        return False

    @staticmethod
    def create_queen_for_pawn(row, col, color):
        return Queen(row, col, color)

    def check_mat(self, color):
        # проверка на мат
        moves_of_all_figures = []
        for figure in self.all_figures[color]:
            moves_of_all_figures += figure.get_all_moves(self)
        if not moves_of_all_figures and self.check_check(color):  # если есть шах, то фигура не позволят сделать
            # простой ход, за исключением того, который уберет шах, поэтому если таких ходов нет и есть шах, то мат
            return True
        return False

    def check_pat(self, color):
        # проверка на пат
        moves_of_all_figures = []
        for figure in self.all_figures[color]:
            moves_of_all_figures += figure.get_all_moves(self)
        if not moves_of_all_figures and not self.check_check(color):  # если ни одна фигура не может сделать ход,
            # и при этом нет шаха, то пат
            return True
        return False

    def check_fifty_moves_rule(self):  # проверка на правило 50 ходов в шахматах (если за 50 ходов не было ни одного
        # взятия и ни одна пешка не сходила, то фиксируется ничья)
        if len(self.all_moves) >= 100:
            for move in self.all_moves[-100:]:
                if type(move.figure) == Pawn or move.type_of_move == TAKE_MOVE:
                    return False
            return True
        return False

    def print_board(self):
        for row in self.board:
            string_to_print = '|'
            for figure in row:
                if figure:
                    string_to_print += str(figure.char()) + str(figure.color) + '|'
                else:
                    string_to_print += '--|'
            print(string_to_print)


if __name__ == '__main__':
    board = Board()  # создаем доску белые фигуры
    board1 = Board()  # создаем доску черные фигуры
    x = board.board
    y = board1.board
    print(x == y)
    board.print_board()
    board1.print_board()
    # for move in board.board[1][0].get_all_moves(board):
    #     print(move)
    # print(board.under_attack(7, 7, BLACK))
    # print(board.check_check(BLACK))
    # print(board.check_check(WHITE))
