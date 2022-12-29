# импорт pygame
import pygame

# прочие импорта
import config
from background import Background
from button import Button
from Board import Board
from config import OPPONENT_COLOR


class Game:
    def __init__(self, color, white_name, black_name):
        # инициализируем необходимые переменные
        self.background = Background('images/fon.jpg', [0, 0])  # создаем фон
        self.player_color = None  # цвет игрока
        self.board = None  # создаем переменную доски
        self.elements = []  # создаем список элементов
        self.font = None  # создаем шрифт
        self.width, self.height = 800, 800  # размеры окна
        self.main_surface = None  # создаем главное окно
        self.game_surface = None  # создаем окно игры
        self.game_mode = None  # режим игры
        self.selected_figure = None  # выбранная фигура
        self.avl_moves = []  # доступные ходы
        self.mouse_move_selected_cell = None
        self.coords_before_move = None
        self.coords_after_move = None
        self.sound_of_normal_move = None  # звук обычного хода
        self.sound_of_take_move = None  # звук взятия фигуры
        self.sound_of_end_or_start_of_the_game = None  # звук начала и конца
        # игры
        self.white_player_name = None  # имя белого игрока
        self.black_player_name = None  # имя черного игрока
        self.msg = None
        self.player_dict = {}
        self.draw = False
        self.mate = False
        self.main(color, white_name, black_name)

    def reset_coords(self):
        self.coords_before_move = None
        self.coords_after_move = None

    def change_game_mode(self, mode):
        self.game_mode = mode
        self.sound_of_end_or_start_of_the_game.play()
        self.elements = [
            Button(self.main_surface, 56, 750, 208, 44, 'Сдаться', self.declare_a_mate, None, False, 'Arial', 20),
            Button(self.main_surface, 296, 750, 208, 44, 'Объявить ничью', self.declare_a_draw, None, False,
                   'Arial', 20),
            Button(self.main_surface, 536, 750, 208, 44, 'Отменить ход', self.back, None, False, 'Arial',
                   20)]  # создаем кнопки
        # для игры

    def change_player_color(self, color):  # функция смены цвета игрока которая вызывается кнопкой
        self.player_color = color

    def declare_a_draw(self):
        if not self.draw and not self.mate and not self.board.check_mat(self.player_color) and not \
                self.board.check_pat(self.player_color):
            self.draw = True
            self.msg = 'Ничья! Достигнута ничья!'
            self.sound_of_end_or_start_of_the_game.play()
            self.game_mode = 4

    def declare_a_mate(self):
        if not self.mate and not self.draw and not self.board.check_mat(self.player_color) and not \
                self.board.check_pat(self.player_color):
            self.mate = True
            self.msg = 'Игрок ' + self.player_dict[self.player_color] + ' сдался! Игрок ' + \
                       self.player_dict[OPPONENT_COLOR[self.player_color]] + ' победил!'
            self.sound_of_end_or_start_of_the_game.play()
            self.game_mode = 4

    def back(self):
        if not self.mate and not self.draw and not self.board.check_mat(self.player_color) and not \
                self.board.check_pat(self.player_color):
            if self.board.all_moves:
                self.board.all_moves[-1].undo_move(self.board)  # отменим последний ход
                # далее меняем необходимые переменные
                self.player_color = OPPONENT_COLOR[self.player_color]
                if self.board.all_moves:
                    self.coords_before_move = (self.board.all_moves[-1].basic_row, self.board.all_moves[-1].basic_col)
                    self.coords_after_move = (self.board.all_moves[-1].row, self.board.all_moves[-1].col)
                else:
                    self.coords_before_move = None

                    self.coords_after_move = None
                self.selected_figure = None
                self.avl_moves = []

    def main(self, player_side, white_name, black_name):
        self.game_mode = 0
        # инициализируем pygame
        pygame.init()
        pygame.display.set_caption('Chess')
        # устанавливаем фон
        self.main_surface = pygame.display.set_mode((self.width, self.height))
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        # создаем звук обычного хода
        self.sound_of_normal_move = pygame.mixer.Sound('sounds/normal_move.mp3')
        # создаем звук взятия фигуры
        self.sound_of_take_move = pygame.mixer.Sound('sounds/take_move.mp3')
        # создаем звук начала или конца игры
        self.sound_of_end_or_start_of_the_game = pygame.mixer.Sound('sounds/start_or_end.mp3')
        self.elements = [
            Button(self.main_surface, 250, 290, 300, 100, "Начать игру", self.change_game_mode, 1, False)]  # режим 1 -
        # игра (без зажатой кнопки просто отрисовывае поле, если кнопка нажата, то ищем фигуру, которую выбрал игрок)
        # создаем цвет
        self.player_color = player_side
        # создаем доску
        self.board = Board(self.player_color)
        # создаем шрифт
        self.font = pygame.font.SysFont('Arial', 20)
        # инициализируем игроков
        self.white_player_name = white_name
        self.black_player_name = black_name
        # инициализируем словарь игроков
        self.player_dict = {1: self.white_player_name, 0: self.black_player_name}
        # инициализируем остальные координаты
        self.msg = None
        self.reset_coords()
        self.draw = False
        self.mate = False
        # игровой цикл
        while True:
            # обрабатываем события
            for event in pygame.event.get():
                # обрабатываем события
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # если нажата не левая кнопка мыши, то ничего не делаем при нажатой кнопке в режиме 1 разрешен только выбор фигуры
                        if self.game_mode == 1:
                            if self.selected_figure:
                                figure = self.get_selected_figure(event)
                                # print(figure)
                                if figure and figure == self.selected_figure:
                                    self.selected_figure = None
                                    self.avl_moves = []
                                    continue
                                self.selected_figure = figure
                            else:
                                self.selected_figure = self.get_selected_figure(event)
                            if self.selected_figure is not None:
                                self.avl_moves = self.selected_figure.get_all_moves(self.board)
                            else:
                                self.avl_moves = []
                            if self.avl_moves:
                                self.game_mode = 2
                                continue
                        if self.game_mode == 2:
                            # print('ready_to_find')
                            result = self.get_mouse_selected_cell(event)
                            if result is not None:
                                selected_row, selected_col = result
                                if self.board.board[selected_row][selected_col] is not None:
                                    if self.board.board[selected_row][selected_col].color == self.player_color:
                                        if self.board.board[selected_row][
                                            selected_col] == self.selected_figure:  # если выбрана та же
                                            # фигура (пользователь еще раз нажал по ней)
                                            self.game_mode = 1
                                            self.avl_moves = []
                                            self.selected_figure = None
                                            continue
                                        self.selected_figure = self.board.board[selected_row][selected_col]
                                        self.avl_moves = self.selected_figure.get_all_moves(self.board)
                                        # reset_coords()
                                        continue
                                for move in self.avl_moves:
                                    if move.row == selected_row and move.col == selected_col:
                                        if move.type_of_move in [config.TAKE_MOVE, config.PASSED_TAKE_MOVE]:
                                            self.sound_of_take_move.play()
                                        elif move.type_of_move == config.CONVERSION_MOVE and move.taken_figure is not None:
                                            self.sound_of_take_move.play()
                                        else:
                                            self.sound_of_normal_move.play()
                                        move.apply_move(self.board)
                                        print(self.board.check_triple_repetition_of_a_position())
                                        # записываем координаты хода
                                        self.coords_before_move = (move.basic_row, move.basic_col)
                                        self.coords_after_move = (move.row, move.col)
                                        self.selected_figure = None
                                        self.avl_moves = []
                                        self.game_mode = 1
                                        self.change_player_color(config.OPPONENT_COLOR[self.player_color])
                                        if self.board.check_mat(self.player_color):
                                            self.msg = 'Шах и мат! Победил(а) игрок ' + self.player_dict[
                                                config.OPPONENT_COLOR[self.player_color]] + '!'
                                            self.game_mode = 4
                                            pygame.time.wait(
                                                250)  # добавляем задержку, чтобы звук совершения хода успел
                                            # проиграться
                                            self.sound_of_end_or_start_of_the_game.play()
                                        elif self.board.check_pat(self.player_color):
                                            self.msg = 'Пат! Достигнута ничья!'
                                            self.game_mode = 4
                                            pygame.time.wait(
                                                250)  # добавляем задержку, чтобы звук совершения хода успел
                                            # проиграться
                                            self.sound_of_end_or_start_of_the_game.play()
                                        elif self.board.check_triple_repetition_of_a_position():
                                            self.msg = 'Ничья! Троекратное повторение позиции!'
                                            self.game_mode = 4
                                            pygame.time.wait(250)
                                            self.sound_of_end_or_start_of_the_game.play()
                                        elif self.board.check_fifty_moves_rule():
                                            self.msg = 'Ничья! Правило пятидесяти ходов!'
                                            self.game_mode = 4
                                            pygame.time.wait(250)
                                            self.sound_of_end_or_start_of_the_game.play()
                    if event.button == 3:
                        if self.game_mode == 4:
                            self.main(1, 'Денистон', 'Красавчик')
                    if event.button == 4:
                        config.recount_coefficent_and_length_of_divider(2)
                    if event.button == 5:
                        config.recount_coefficent_and_length_of_divider(-2)
                    # TODO: ОСНОВНАЯ ЗАДАЧА - ПРОПИСАТЬ ВСЕ ОСТАЛЬНЫЕ РЕЖИМЫ РАБОТЫ ИГРЫ
                if event.type == pygame.MOUSEMOTION:
                    if self.game_mode == 2:
                        self.mouse_move_selected_cell = self.get_mouse_selected_cell(event)
                        if self.mouse_move_selected_cell is not None:
                            if self.player_color == config.WHITE:
                                self.mouse_move_selected_cell[0] = 7 - self.mouse_move_selected_cell[0]
                            else:
                                self.mouse_move_selected_cell[1] = 7 - self.mouse_move_selected_cell[1]
                        # print(mouse_move_selected_cell)
                # обрабатываем режимы игры
                if self.game_mode == 0:
                    self.redraw_main_screen()
            # обновляем фон
            self.background.update()
            if self.game_mode != 0:
                self.redraw_game_screen()
            # обновляем окно
            pygame.display.flip()

    # функция отрисовки начального экрана
    def redraw_main_screen(self):
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        for element in self.elements:
            element.process()  # обрабатываем элементы
        pygame.display.flip()  # обновляем окно

    # функция отрисовки игрового экрана
    def redraw_game_screen(self):
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        for element in self.elements:
            element.process()  # обрабатываем элементы
        self.draw_cell()
        self.draw_figures()
        self.draw_msg()
        pygame.display.flip()  # обновляем окно

    def draw_cell(self):  # функция отрисовки клеток
        # создаем холст с математически-вычисленными размерами клеток и разделителей
        self.game_surface = pygame.Surface(
            (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2,
             config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2))
        self.game_surface.blit(self.background.image, self.background.rect)
        self.game_surface.fill((35, 35, 35))
        pygame.draw.rect(self.game_surface, (0, 0, 0), (
            0, 0, config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2,
            config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2),
                         config.length_of_divider_between_cells)
        # отрисовываю границу с запсом в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
        pygame.draw.rect(self.game_surface, (210, 202, 140), (
            config.length_of_divider_between_cells,
            config.length_of_divider_between_cells,
            self.game_surface.get_width() - config.length_of_divider_between_cells * 2,
            self.game_surface.get_height() - config.length_of_divider_between_cells * 2
        ), config.coefficient)
        # отрисовываем вторую границу, которая теперь состоит из четырех прямоугольников, два - сверху вниз, два - млева направо, вне поля с запасов в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
        # это спарва налево
        pygame.draw.rect(self.game_surface, (0, 0, 0), (
            config.length_of_divider_between_cells,
            config.coefficient + config.length_of_divider_between_cells,
            self.game_surface.get_width() - config.length_of_divider_between_cells * 2,
            config.length_of_divider_between_cells
        ))
        pygame.draw.rect(self.game_surface, (0, 0, 0), (
            config.length_of_divider_between_cells,
            self.game_surface.get_height() - config.coefficient - config.length_of_divider_between_cells * 2,
            self.game_surface.get_width() - config.length_of_divider_between_cells * 2,
            config.length_of_divider_between_cells
        ))
        # это сверху вниз
        pygame.draw.rect(self.game_surface, (0, 0, 0), (
            config.coefficient + config.length_of_divider_between_cells,
            config.length_of_divider_between_cells,
            config.length_of_divider_between_cells,
            self.game_surface.get_height() - config.length_of_divider_between_cells * 2
        ))
        pygame.draw.rect(self.game_surface, (0, 0, 0), (
            self.game_surface.get_width() - config.coefficient - config.length_of_divider_between_cells * 2,
            config.length_of_divider_between_cells,
            config.length_of_divider_between_cells,
            self.game_surface.get_height() - config.length_of_divider_between_cells * 2
        ))
        # отрисовываем доску по рядам (row - номер ряда, col - номер клетки в ряду row), не забываем про разделитель
        for amount_of_row in range(8):
            # отрисовываем границу каждого ряда не рисуем, если нулевая позиция
            if amount_of_row != 0:
                # сверху в низ
                pygame.draw.rect(self.game_surface, (0, 0, 0), (
                    config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells,
                    self.game_surface.get_height() - config.length_of_divider_between_cells * 2
                ))
                # справа налево
                pygame.draw.rect(self.game_surface, (0, 0, 0), (
                    config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                    self.game_surface.get_width() - config.length_of_divider_between_cells * 2,
                    config.length_of_divider_between_cells
                ))
            for amount_of_col in range(8):
                if self.player_color == config.WHITE:
                    help_row, help_col = 7 - amount_of_row, amount_of_col
                else:
                    help_row, help_col = amount_of_row, 7 - amount_of_col
                if (amount_of_row + amount_of_col) % 2 == 0:
                    color = (238, 232, 170)
                else:
                    color = (160, 82, 45)
                if self.selected_figure is not None and help_row == self.selected_figure.row and help_col == self.selected_figure.col:
                    color = (135, 148, 212)
                if self.board.check_check(self.player_color) and self.board.get_king(
                        self.player_color).row == help_row and self.board.get_king(
                        self.player_color).col == help_col:
                    color = (255, 0, 0)
                # отрисовываем непосредственно клетки
                pygame.draw.rect(self.game_surface, color, (
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                    config.size_of_cell,
                    config.size_of_cell
                ))
                if (self.coords_before_move and self.coords_after_move) and (
                        (help_row == self.coords_before_move[0] and help_col == self.coords_before_move[1]) or (
                        help_row == self.coords_after_move[0] and help_col == self.coords_after_move[1])):
                    pygame.draw.rect(self.game_surface, (95, 41, 153), (
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells,
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                        config.size_of_cell,
                        config.size_of_cell
                    ), 5)
                if self.avl_moves:
                    for move in self.avl_moves:
                        if help_row == move.row and help_col == move.col:
                            indent = round(config.size_of_cell * 0.3)
                            color_of_selection = (82, 209, 25)
                            if self.board.board[help_row][help_col] is not None and self.board.board[help_row][
                                help_col].color != self.player_color and \
                                    self.board.under_attack(help_row, help_col, OPPONENT_COLOR[self.player_color]):
                                indent = round(config.size_of_cell * 0.13)
                                color_of_selection = (255, 50, 50)
                            if self.mouse_move_selected_cell and amount_of_row == self.mouse_move_selected_cell[
                                0] and amount_of_col == self.mouse_move_selected_cell[1]:
                                indent = 0
                                pygame.draw.rect(self.game_surface, color_of_selection, (
                                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + indent,
                                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + indent,
                                    config.size_of_cell - indent * 2,
                                    config.size_of_cell - indent * 2
                                ))
                            else:
                                pygame.draw.ellipse(self.game_surface, color_of_selection, (
                                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + indent,
                                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + indent,
                                    config.size_of_cell - indent * 2,
                                    config.size_of_cell - indent * 2
                                ))
                # отрисовываем буквы так, чтобы они появились в области с шириной coefficient пикселей
                if amount_of_row == 0:
                    text = self.font.render(
                        chr(amount_of_col + 65) if self.player_color == config.WHITE else chr(7 - amount_of_col + 65), True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient // 2 - text.get_height() // 2
                    ))
                if amount_of_row == 7:
                    text = self.font.render(
                        chr(amount_of_col + 65) if self.player_color == config.WHITE else chr(7 - amount_of_col + 65), True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                        self.game_surface.get_height() - config.length_of_divider_between_cells - config.coefficient // 2 - text.get_height() // 2
                    ))
                # отрисовываем цифры так, чтобы они появились в области с высотой coefficient пикселей
                if amount_of_col == 0:
                    text = self.font.render(str(8 - amount_of_row) if self.player_color == 1 else str(amount_of_row + 1), True,
                                       (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient // 2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                    ))
                if amount_of_col == 7:
                    text = self.font.render(str(8 - amount_of_row) if self.player_color == 1 else str(amount_of_row + 1), True,
                                       (0, 0, 0))
                    self.game_surface.blit(text, (
                        self.game_surface.get_width() - config.length_of_divider_between_cells - config.coefficient // 2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                    ))
        self.main_surface.blit(self.game_surface, (
            # отрисовываем холст на экране в первый раз c координатами, вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
            (self.width - (
                    config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
            (self.height - (
                    config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
        ))
        # board.print_board()

    # функция, которая отрисовывает фигуры на доске

    def draw_figures(self):
        board_to_work_with = self.board.board.copy()
        # переворасиваем в зависимости от цвета игрока
        if self.player_color == config.BLACK:
            board_to_work_with = list(map(lambda row: row[::-1], board_to_work_with))
        else:
            board_to_work_with = board_to_work_with[::-1]
        for amount_of_row in range(8):
            for amount_of_col in range(8):
                # если в клетке есть фигура
                if board_to_work_with[amount_of_row][amount_of_col]:
                    # отрисовываем фигуру
                    try:
                        self.game_surface.blit(board_to_work_with[amount_of_row][amount_of_col].image, (
                            config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                            board_to_work_with[amount_of_row][amount_of_col].image.get_width() // 2,
                            config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                            board_to_work_with[amount_of_row][amount_of_col].image.get_height() // 2
                        ))
                    except Exception:
                        pass
        self.main_surface.blit(self.game_surface, (  # отрисовываем холст на экране в первый раз c координатами,
            # вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
            (self.width - (
                    config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
            (self.height - (
                    config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
        ))

    def get_selected_figure(self, mouse_event):
        event_x = mouse_event.pos[0] - (self.width - (
                config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
        event_y = mouse_event.pos[1] - (self.height - (
                config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
        # в этой функции мы должны вернуть фигуру, которая была выбрана если кликнули по месту, где ее нет,
        # то вернуть None
        board_to_work_with = self.board.board.copy()
        # переворасиваем в зависимости от цвета игрока
        if self.player_color == config.BLACK:
            board_to_work_with = list(map(lambda row: row[::-1], board_to_work_with))
        else:
            board_to_work_with = board_to_work_with[::-1]
        x = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
        for amount_of_row in range(8):
            y = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
            for amount_of_col in range(8):
                if board_to_work_with[amount_of_row][amount_of_col] is not None:
                    if board_to_work_with[amount_of_row][amount_of_col].color == self.player_color:
                        try:
                            if pygame.Rect(y, x, config.size_of_cell, config.size_of_cell).collidepoint(
                                    (event_x, event_y)):
                                return board_to_work_with[amount_of_row][amount_of_col]
                        except Exception:
                            pass
                y += config.size_of_cell + config.length_of_divider_between_cells
            x += config.size_of_cell + config.length_of_divider_between_cells

    # это функция для поиска координат нажатия мыши относительно поля и массива board.board
    def get_mouse_selected_cell(self, mouse_event):
        event_x = mouse_event.pos[0] - (
                self.width - (
                config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
        event_y = mouse_event.pos[1] - (
                self.height - (
                config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
        x = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells  # ряды
        for amount_of_row in range(8):
            y = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells  # столбцы
            for amount_of_col in range(8):
                try:
                    if pygame.Rect(y, x, config.size_of_cell, config.size_of_cell).collidepoint((event_x, event_y)):
                        if self.player_color == config.BLACK:
                            return [amount_of_row, 7 - amount_of_col]
                        return [7 - amount_of_row, amount_of_col]
                except Exception:
                    pass
                y += config.size_of_cell + config.length_of_divider_between_cells
            x += config.size_of_cell + config.length_of_divider_between_cells

    def draw_msg(self):
        if self.msg:
            size_of_font = round(
                (config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells +
                 config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2) / len(
                    self.msg) * 1.5)
            font = pygame.font.SysFont('Arial', size_of_font, True)
            text = font.render(self.msg, True, (255, 0, 0))
            self.main_surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height()
                                          // 2))
            pygame.display.update()


if __name__ == '__main__':
    game = Game(1, 'Даниил', 'Виктор')
