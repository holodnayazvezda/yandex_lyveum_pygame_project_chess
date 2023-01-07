from Figure import Figure


class TempFigure(Figure):
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'TempFigure')

    @staticmethod
    def char():
        return 'T'

    @staticmethod
    def can_move(row1, col1, board):
        return [False]