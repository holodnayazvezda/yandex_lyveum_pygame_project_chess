import pygame
from config import WHITE, NORMAL_MOVE, TAKE_MOVE, CASTLING_MOVE, PASSED_TAKE_MOVE, CONVERSION_MOVE
from Move import Move


class Figure(pygame.sprite.Sprite):
    def __init__(self, row, col, color, name, dir='sprites/', ext='.png'):
        pygame.sprite.Sprite.__init__(self)
        self.row, self.col = row, col
        self.color = color
        self.image = pygame.image.load(dir + ('white' if color == WHITE else 'black') + name + ext)   # name с большой буквы

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
                result = self.can_move(amount_of_row, amount_of_col, board.board)
                if result[0]:
                    if result[1] == NORMAL_MOVE:
                        moves.append(self.create_normal_move(amount_of_row, amount_of_col))
                    elif result[1] == TAKE_MOVE:
                        moves.append(self.create_take_move(amount_of_row, amount_of_col, board[amount_of_row][amount_of_col]))
        return moves

    def create_normal_move(self, new_row, new_col):
        move = Move(NORMAL_MOVE, self, new_row, new_col)
        return move

    def create_take_move(self, new_row, new_col, taken_figure):
        move = Move(TAKE_MOVE, self, new_row, new_col, taken_figure)
        return move

    @staticmethod
    def is_valid_move(row, col, board):
        return 0 <= row < 8 and 0 <= col < 8 and board[row][col] is None
