from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from config import WHITE, BLACK


class Board:
    def __init__(self, player_side):
        self.board = []
        # генерируем доску по рядам (затем перевернем так как 0 ряд здесь - это седьмой в игре)
        for amount_of_row in range(8):
            row = []  # ряды
            for amount_of_col in range(8):
                if player_side == WHITE:
                    if amount_of_row == 1:
                        row.append(Pawn(amount_of_row, amount_of_col, BLACK))
                    elif amount_of_row == 6:
                        row.append(Pawn(amount_of_row, amount_of_col, WHITE))
                    elif amount_of_row == 0:
                        if amount_of_col == 0 or amount_of_col == 7:
                            row.append(Rook(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 1 or amount_of_col == 6:
                            row.append(Knight(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 2 or amount_of_col == 5:
                            row.append(Bishop(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 3:
                            row.append(Queen(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 4:
                            row.append(King(amount_of_row, amount_of_col, BLACK))
                    elif amount_of_row == 7:
                        if amount_of_col == 0 or amount_of_col == 7:
                            row.append(Rook(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 1 or amount_of_col == 6:
                            row.append(Knight(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 2 or amount_of_col == 5:
                            row.append(Bishop(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 3:
                            row.append(Queen(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 4:
                            row.append(King(amount_of_row, amount_of_col, WHITE))
                    else:
                        row.append(None)
                else:
                    if amount_of_row == 1:
                        row.append(Pawn(amount_of_row, amount_of_col, WHITE))
                    elif amount_of_row == 6:
                        row.append(Pawn(amount_of_row, amount_of_col, BLACK))
                    elif amount_of_row == 0:
                        if amount_of_col == 0 or amount_of_col == 7:
                            row.append(Rook(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 1 or amount_of_col == 6:
                            row.append(Knight(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 2 or amount_of_col == 5:
                            row.append(Bishop(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 3:
                            row.append(Queen(amount_of_row, amount_of_col, WHITE))
                        elif amount_of_col == 4:
                            row.append(King(amount_of_row, amount_of_col, WHITE))
                    elif amount_of_row == 7:
                        if amount_of_col == 0 or amount_of_col == 7:
                            row.append(Rook(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 1 or amount_of_col == 6:
                            row.append(Knight(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 2 or amount_of_col == 5:
                            row.append(Bishop(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 3:
                            row.append(Queen(amount_of_row, amount_of_col, BLACK))
                        elif amount_of_col == 4:
                            row.append(King(amount_of_row, amount_of_col, BLACK))
                    else:
                        row.append(None)
            if player_side == BLACK:
                self.board.append(row[::-1])
            else:
                self.board.append(row)

    def get_figure(self, row, col):
        return self.board[row][col]

    def print_board(self):
        for row in self.board:
            string_to_print = '|'
            for figure in row:
                if figure:
                    string_to_print += str(figure.row) + str(figure.col) + '|'
                else:
                    string_to_print += '--|'
            print(string_to_print)

