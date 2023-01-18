# файл, в котором реализован логика базовой фигуры (класса - родителя всех шахматных фигур)

import pygame
from config import WHITE, NORMAL_MOVE, TAKE_MOVE, CASTLING_MOVE, PASSED_TAKE_MOVE, CONVERSION_MOVE
from Move import Move


class Figure(pygame.sprite.Sprite):
    def __init__(self, row, col, color, name, directory='sprites/', ext='.png'):
        pygame.sprite.Sprite.__init__(self)
        self.row, self.col = row, col
        self.color = color
        self.name = name
        self.amount_of_moves = 0
        self.x = None
        self.y = None
        try:
            self.image = pygame.image.load(directory + ('white' if color == WHITE else 'black') + name + ext)   # name с 
            # большой буквы 
        except Exception:
            self.image = None

    def set_position(self, row, col):
        self.x = row
        self.y = col

    def get_color(self):
        if self.color == WHITE:
            return 238, 232, 170
        else:
            return 160, 82, 45

    def get_all_moves(self, board):   # не список, а объект класса board
        moves = []
        for amount_of_row in range(8):
            for amount_of_col in range(8):
                result = self.can_move(amount_of_row, amount_of_col, board)  # передаю объект класса Board
                if result[0]:  # TODO: реализовать действие при шахе
                    if result[1] == NORMAL_MOVE:
                        moves.append(self.create_normal_move(amount_of_row, amount_of_col))
                    elif result[1] == TAKE_MOVE:
                        moves.append(self.create_take_move(amount_of_row, amount_of_col, 
                                                           board.board[amount_of_row][amount_of_col]))
                    elif result[1] == CONVERSION_MOVE:
                        moves.append(self.create_conversion_move(amount_of_row, amount_of_col, board))
                    elif result[1] == PASSED_TAKE_MOVE:
                        moves.append(
                            self.create_passed_take_move(amount_of_row, amount_of_col, board.board[
                                amount_of_row + (-1 if self.color == WHITE else 1)][amount_of_col])
                        )
                    if result[1] == CASTLING_MOVE:
                        if board.under_attack(board.get_king(self.color).row, 
                                              board.get_king(self.color).col, self.color):  # проверка на шах при 
                            # рокировке 
                            continue
                        moves.append(self.create_castling_move(amount_of_row, amount_of_col, board))
                    # проверка на шах после хода (если он есть, или если он появляется после хода)
                    now_move = moves[-1]  # выбираем последний ход
                    now_move.apply_move(board)  # применяем ход
                    if board.check_check(self.color):  # если после применения хода есть шах, то
                        moves.pop()  # удаляем ход из списка (если шаха нет, то ход остается)
                    now_move.undo_move(board)  # в любом случае отменяем ход
        return moves

    def create_normal_move(self, new_row, new_col):
        move = Move(NORMAL_MOVE, self, new_row, new_col)
        return move

    def create_take_move(self, new_row, new_col, taken_figure):
        move = Move(TAKE_MOVE, self, new_row, new_col, taken_figure)
        return move

    def create_conversion_move(self, new_row, new_col, board):
        move = Move(CONVERSION_MOVE, self, new_row, new_col, board.board[new_row][new_col])
        return move

    def create_passed_take_move(self, new_row, new_col, taken_figure):
        move = Move(PASSED_TAKE_MOVE, self, new_row, new_col, taken_figure)
        return move

    def create_castling_move(self, new_row, new_col, board):
        if self.col < new_col:
            rook = board.board[self.row][7]  # берем ладью так смело, потому что мы проверили, что она там есть
        else:
            rook = board.board[self.row][0]  # берем ладью так смело, потому что мы проверили, что она там есть
        # DEBUG: ладья ищется корректно
        move = Move(CASTLING_MOVE, self, new_row, new_col, rook)
        return move

    def was_move(self):  # Функция для проверки того, ходила ли фигура. Полезно при реализации рокировки и взятия на
        # проходе
        if self.amount_of_moves == 0:
            return False
        return True

    @staticmethod
    def is_valid_move(row, col, board):
        return 0 <= row < 8 and 0 <= col < 8 and board[row][col] is None
