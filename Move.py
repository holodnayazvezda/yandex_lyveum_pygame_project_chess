class Move:
    def __init__(self, type_of_move, figure, row, col, taken_figure=None):
        self.figure = figure  # фигура, которая делает ход
        self.row = row  # строка, куда ходит фигура
        self.col = col   # столбец, куда ходит фигура
        self.type_of_move = type_of_move
        self.taken_figure = taken_figure  # фигура, которая съедается. В разных типах ходов может иметь значение None, так как ничего не съедается
        self.rock = None  # рокировка
        self.old_rock_row = None  # рокировка
        self.old_rock_col = None  # рокировка
        self.new_rock_row = None  # рокировка
        self.new_rock_col = None  # рокировка

    def __str__(self):
        return f'{self.type_of_move} {self.row} {self.col}'



