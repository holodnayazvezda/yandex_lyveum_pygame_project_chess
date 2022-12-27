from Figure import Figure


class TempFigure(Figure):
    def __init__(self, x, y, color):
        Figure.__init__(self, x, y, color, 'TempFigure')

    def char(self):
        return 'T'

    def can_move(self, row1, col1, board):
        return [False]