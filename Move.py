from config import NORMAL_MOVE, TAKE_MOVE, CASTLING_MOVE, CONVERSION_MOVE, PASSED_TAKE_MOVE


class Move:
    def __init__(self, type_of_move, figure, row, col, taken_figure=None):
        self.figure = figure  # фигура, которая делает ход
        self.row = row  # Строка, куда ходит фигура. Важно! При ходе - конверсии (превращении пешки) на поле с этой
        # координатой встанет ферзь
        self.col = col   # Столбец, куда ходит фигура. Важно! При ходе - конверсии (превращении пешки) на поле с этой
        # координатой встанет ферзь
        self.basic_row = figure.row  # строка, с которой ходит фигура
        self.basic_col = figure.col  # столбец, с которой ходит фигура
        self.type_of_move = type_of_move
        self.taken_figure = taken_figure  # фигура, которая съедается. В разных типах ходов может иметь значение
        # None, так как ничего не съедается
        self.basic_taken_figure_row = self.taken_figure.row if self.taken_figure else None  # строка, с которой
        # съедается фигура
        self.basic_taken_figure_col = self.taken_figure.col if self.taken_figure else None  # столбец, с которой
        # съедается фигура

    def __str__(self):
        return f'{self.type_of_move} {self.row} {self.col}'

    def apply_move(self, board):
        self.figure.amount_of_moves += 1  # увеличиваем количество ходов фигуры
        board.all_moves.append(self)
        if self.type_of_move == NORMAL_MOVE:
            board.board[self.row][self.col] = self.figure
            board.board[self.basic_row][self.basic_col] = None
            self.figure.row = self.row
            self.figure.col = self.col
        elif self.type_of_move == TAKE_MOVE:
            board.board[self.row][self.col] = self.figure  # поставили фигуру на место сединой фигуры
            self.figure.row = self.row  # фигура, которая съела, стала на место съеденной фигуры
            self.figure.col = self.col  # фигура, которая съела, стала на место съеденной фигуры

            board.board[self.basic_row][self.basic_col] = None  # убрали фигуру, которая съела с прежнего места
            board.all_figures[self.taken_figure.color].remove(self.taken_figure)  # съеденная фигура убрана из списка
            # фигур
        elif self.type_of_move == CONVERSION_MOVE:
            # важно помнить, что taken_figure может быть как быть, так и не быть
            queen = board.create_queen_for_pawn(self.row, self.col, self.figure.color)  # создаем ферзя, который
            # займет место пешки на row, col
            board.board[self.row][self.col] = queen  # поставили фигуру ФЕРЗЯ (!) на новое место
            board.all_figures[self.figure.color].remove(self.figure)  # убрали пешку из списка фигур
            board.all_figures[self.figure.color].append(queen)  # добавили ферзя в список фигур

            board.board[self.basic_row][self.basic_col] = None  # убрали фигуру пешки, которая съела с прежнего места
            if self.taken_figure is not None:  # если ход со взятием, то
                board.all_figures[self.taken_figure.color].remove(self.taken_figure)  # съеденная фигура убрана из
                # списка фигур
        elif self.type_of_move == PASSED_TAKE_MOVE:
            board.board[self.row][self.col] = self.figure  # поставили фигуру на место съетой фигуры
            self.figure.row = self.row  # фигура, которая съела, встала на определенное место
            self.figure.col = self.col  # фигура, которая съела, встала на определенное место

            board.board[self.basic_row][self.basic_col] = None  # убрали фигуру, которая съела с прежнего места
            board.board[self.basic_taken_figure_row][self.basic_taken_figure_col] = None  # убираем фигуру, которая
            # была съедена на проходе
            board.all_figures[self.taken_figure.color].remove(self.taken_figure)  # съеденная фигура убрана из списка
            # фигур

        elif self.type_of_move == CASTLING_MOVE:
            # ВАЖНО!!! в данном случае taken_figure это Ладья и она НЕ СЪЕДАЕТСЯ!!!
            board.board[self.row][self.col] = self.figure  # поставили фигуру КОРОЛЯ (!) на новое место
            board.board[self.basic_row][self.basic_col] = None  # убрали фигуру КОРОЛЯ с прежнего места
            self.figure.row = self.row  # король встал на необходимую клетку (row)
            self.figure.col = self.col  # король встал на необходимую клетку (col)
            # поскольку taken_figure (ЛАДЬЯ!!!) может ходить по разному, то нужно написать определенное условие
            if self.taken_figure.col == 0:  # если ладья была на 0-м столбце, то
                board.board[self.row][self.taken_figure.col + 3] = self.taken_figure  # поставили ладью на 3 столбец
                # (ВАЖНО!!! БЕРЕМ COL ЛАДЬИ (taken_figure), а не КОРОЛЯ!!!)
                self.taken_figure.col = self.taken_figure.col + 3  # ладья стала на 3 столбец (ВАЖНО!!! БЕРЕМ COL
                # ЛАДЬИ (taken_figure), а не КОРОЛЯ!!!)
                # не меняем row, так как она не меняется
            elif self.taken_figure.col == 7:
                board.board[self.row][self.basic_taken_figure_col - 2] = self.taken_figure  # поставили ладью на 5
                # столбец (ВАЖНО!!! БЕРЕМ COL ЛАДЬИ (taken_figure), а не КОРОЛЯ!!!)
                self.taken_figure.col = self.basic_taken_figure_col - 2  # ладья стала на 5 столбец (ВАЖНО!!! БЕРЕМ
                # COL ЛАДЬИ (taken_figure), а не КОРОЛЯ!!!)
            board.board[self.basic_taken_figure_row][self.basic_taken_figure_col] = None  # убрали ладью с прежнего
            # места
        converted_board = []
        for row in board.board:
            converted_board += row
        board.positions.append(converted_board)  # добавляем новую позицию в список позиций
        # TODO: не уберу, пока не буду уверен, что все работает идеально (а пока - реализовать для всех остальных типов)

    def undo_move(self, board):
        self.figure.amount_of_moves -= 1  # уменьшаем количество ходов фигуры
        board.all_moves.pop()  # удаляем последний ход из списка всех ходов
        if self.type_of_move == NORMAL_MOVE:
            board.board[self.basic_row][self.basic_col] = self.figure  # ставим фигуру на место, с которого она ходила
            board.board[self.row][self.col] = None  # убираем фигуру с места, на которое она ходила
            self.figure.row = self.basic_row  # фигура вернулась на место, с которого она ходила
            self.figure.col = self.basic_col  # фигура вернулась на место, с которого она ходила
        elif self.type_of_move == TAKE_MOVE:
            board.board[self.row][self.col] = self.taken_figure  # ставим съеденную фигуру на место, где она была
            board.board[self.basic_row][self.basic_col] = self.figure  # ставим фигуру на место, где она была
            self.figure.row = self.basic_row  # фигура вернулась на место, с которого она ходила
            self.figure.col = self.basic_col  # фигура вернулась на место, с которого она ходила
            board.all_figures[self.taken_figure.color].append(self.taken_figure)  # съеденная фигура вернулась в
            # список фигур
        elif self.type_of_move == CONVERSION_MOVE:
            board.all_figures[self.figure.color].remove(board.board[self.row][self.col])  # убрали ферзя из списка фигур
            board.all_figures[self.figure.color].append(self.figure)  # вернули пешку в список фигур
            board.board[self.row][self.col] = self.taken_figure  # ставим съеденную фигуру на место, где она была (
            # МОЖЕТ БЫТЬ  и None !!!!!)
            board.board[self.basic_row][self.basic_col] = self.figure  # ставим фигуру на место, с которого она ходила
            # TODO: это мне пока не надо, так как я не менял координаты figure
            # self.figure.row = self.basic_row  # фигура вернулась на место, с которого она ходила
            # self.figure.col = self.basic_col  # фигура вернулась на место, с которого она ходила
            if self.taken_figure is not None:  # если ход со взятием, то
                board.all_figures[self.taken_figure.color].append(self.taken_figure)
        elif self.type_of_move == PASSED_TAKE_MOVE:
            board.board[self.basic_taken_figure_row][self.basic_taken_figure_col] = self.taken_figure  # ставим
            # съеденную фигуру на место, где она была
            board.board[self.basic_row][self.basic_col] = self.figure  # ставим фигуру на место, с которого она ходила
            self.figure.row = self.basic_row  # фигура вернулась на место, с которого она ходила
            self.figure.col = self.basic_col  # фигура вернулась на место, с которого она ходила

            board.board[self.row][self.col] = None  # убираем фигуру с места, на котором она стояла
            board.all_figures[self.taken_figure.color].append(self.taken_figure)  # съеденная фигура вернулась в
            # список фигур
        elif self.type_of_move == CASTLING_MOVE:
            board.board[self.basic_row][self.basic_col] = self.figure  # ставим фигуру (КОРОЛЯ!) на место, с которого
            # она ходила
            board.board[self.row][self.col] = None  # убираем фигуру (КОРОЛЯ!) с места, на которое он ходил
            self.figure.row = self.basic_row  # фигура вернулась на место, с которого она ходила
            self.figure.col = self.basic_col  # фигура вернулась на место, с которого она ходила

            board.board[self.basic_taken_figure_row][self.basic_taken_figure_col] = self.taken_figure  # ставим
            # фигуру (ЛАДЬЮ!) на место, с которого она ходила
            board.board[self.basic_taken_figure_row][self.taken_figure.col] = None  # убираем фигуру (ЛАДЬЮ!) с
            # места, на которое она ходила
            self.taken_figure.row = self.basic_taken_figure_row  # фигура вернулась на место, с которого она ходила
            self.taken_figure.col = self.basic_taken_figure_col  # фигура вернулась на место, с которого она ходила
        board.positions.pop()
        # TODO: не уберу, пока не буду уверен, что все работает идеально (а пока - реализовать для всех остальных типов)
