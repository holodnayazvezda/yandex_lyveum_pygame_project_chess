from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from config import WHITE, BLACK, OPPONENT_COLOR, TAKE_MOVE, NORMAL_MOVE, CONVERSION_MOVE, PASSED_TAKE_MOVE, CASTLING_MOVE
from TempFigure import TempFigure


class Board:
    def __init__(self, player_side):
        self.board = []
        self.all_figures = {1: [], 0: []}  # словарь всех фигур 1 - белые фигуры, 0 - черные фигуры
        self.all_moves = []  # список всех ходов, в нем лежат объекты класса Move
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

    def under_attack(self, row, col, color):  # проврерка на атаку клетки с координатами row, col цветом color
        current_figure = self.board[row][col]  # запоминаем фигуру которая стоит на клетке
        self.board[row][col] = TempFigure(row, col, color)  # ставим временную фигуру на клетку, для адекватной
        # проверки на атаку
        for figure in self.all_figures[OPPONENT_COLOR[color]]:
            result = figure.can_move(row, col, self)  # возвращает массив - первый элемент - булевое значение (может
            # ходить или нет), а второ1 - тип хода
            if result[0]:
                self.board[row][col] = current_figure
                return True
        self.board[row][col] = current_figure
        return False

    def check_check(self, color):
        king = self.get_king(color)
        # вызвать under_attack для всех фигур противника
        return self.under_attack(king.row, king.col, color)

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
    board = Board(0)  # создаем доску белые фигуры
    board.print_board()
    # for move in board.board[1][0].get_all_moves(board):
    #     print(move)
    print(board.under_attack(7, 7, BLACK))
    print(board.check_check(BLACK))
    print(board.check_check(WHITE))
    print(len(board.check_mat(WHITE)))