# импорт pygame
import pygame

# прочие импорта
import config
from background import Background
from button import Button
from Board import Board
from config import OPPONENT_COLOR
from inputbox import InputBox
from database import write_result_of_the_game, read_results_of_the_game


class Game:
    def __init__(self, color):
        # инициализируем необходимые переменные
        self.background = Background('images/fon.jpg', [0, 0])  # создаем фон
        self.player_color = None  # цвет игрока
        self.board = None  # создаем переменную доски
        self.elements = []  # создаем список элементов
        self.font = None  # создаем шрифт
        self.width, self.height = 800, 800  # размеры окна
        self.main_surface = None  # создаем главное окно
        self.players_name_surface = None  # создаем окно для ввода имени игроков
        self.game_surface = None  # создаем окно игры
        self.before_mode = None  # создаем переменную для хранения предыдущего режима
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
        self.input_boxes = []
        self.result_of_the_game = None
        self.global_results_of_the_game = {}
        self.main(color)

    def reset_coords(self):
        self.coords_before_move = None
        self.coords_after_move = None

    def change_game_mode(self, mode, another_func=False):  # функция смены режима игры
        self.before_mode = self.game_mode
        self.game_mode = mode
        if self.game_mode == 2 or self.game_mode == 3:
            if not self.msg:
                self.mode2()
            else:
                self.game_mode = self.before_mode
        elif self.game_mode == 1:
            self.mode1()
        elif self.game_mode == 0:
            self.main(1)
        elif self.game_mode == 5:
            if not self.draw and not self.mate and not self.board.check_mat(self.player_color) and not \
                    self.board.check_pat(self.player_color):
                self.mode5(another_func)
            elif self.draw or self.mate or self.board.check_mat(self.player_color) or \
                    self.board.check_pat(self.player_color):
                self.main(1)
            else:
                self.game_mode = self.before_mode

    def mode1(self):
        # создаем список с полями ввода для удобства обработки
        self.input_boxes = [InputBox(380, 244, 140, 32), InputBox(380, 344, 140, 32)]
        # создаем кнопку для начала игры и помещаем ее в список элементов для обработки
        self.elements = [
            Button(self.main_surface, 100, 550, 200, 100, "<- Назад", self.change_game_mode, 0, False),
            Button(self.main_surface, 500, 550, 200, 100, "Далее ->", self.change_game_mode, 2, False)
        ]

    def mode2(self):
        # создаем кнопки
        self.elements = [
            Button(self.main_surface, 90, 675, 200, 50, 'Сдаться', self.declare_a_mate, None, False, 'Arial', 25),
            Button(self.main_surface, 310, 675, 200, 50, 'Объявить ничью', self.declare_a_draw, None, False,
                   'Arial', 25),
            Button(self.main_surface, 530, 675, 200, 50, 'Отменить ход', self.back, None, False, 'Arial',
                   25),
            Button(self.main_surface, 90, 740, 640, 50, "<- Назад", self.change_game_mode, 5, False, 'Arial', 30)]
        self.white_player_name = self.input_boxes[0].text  # получаем имя белого игрока
        self.black_player_name = self.input_boxes[1].text  # получаем имя черного игрока
        self.player_dict = {1: self.white_player_name, 0: self.black_player_name}  # обновляем словарь с именами игроков
        self.sound_of_end_or_start_of_the_game.play()

    def mode5(self, another_func):
        self.elements = [
            Button(self.main_surface, 110, 550, 200, 100, "Да", self.exit_and_lose, 2, False),
            Button(self.main_surface, 490, 550, 200, 100, "Нет", self.change_game_mode, self.before_mode, False)
        ]
        if another_func:
            self.elements[0] = Button(self.main_surface, 110, 550, 200, 100, "Да", self.exit_and_lose, 1, False)

    def exit_and_lose(self, what_to_do=1):  # 1 - выход, 2 - главное меню
        if self.player_color == 1:
            self.result_of_the_game = -1
        else:
            self.result_of_the_game = 1
        write_result_of_the_game(self.white_player_name, self.black_player_name,
                                 self.result_of_the_game, self.player_dict)
        if what_to_do == 1:
            exit()
        else:
            self.change_game_mode(0)

    def change_player_color(self, color):  # функция смены цвета игрока которая вызывается кнопкой
        self.player_color = color

    def declare_a_draw(self):
        if not self.draw and not self.mate and not self.board.check_mat(self.player_color) and not \
                self.board.check_pat(self.player_color):
            self.draw = True
            self.msg = 'Ничья! Достигнута ничья!'
            self.sound_of_end_or_start_of_the_game.play()
            self.game_mode = 6
            self.result_of_the_game = 0
            write_result_of_the_game(self.white_player_name, self.black_player_name,
                                     self.result_of_the_game, self.player_dict)

    def declare_a_mate(self):
        if not self.mate and not self.draw and not self.board.check_mat(self.player_color) and not \
                self.board.check_pat(self.player_color):
            self.mate = True
            self.msg = 'Игрок ' + self.player_dict[self.player_color] + ' сдался! Игрок ' + \
                       self.player_dict[OPPONENT_COLOR[self.player_color]] + ' победил!'
            self.sound_of_end_or_start_of_the_game.play()
            self.game_mode = 6
            if self.player_color == 1:
                self.result_of_the_game = -1
            else:
                self.result_of_the_game = 1
            write_result_of_the_game(self.white_player_name, self.black_player_name,
                                     self.result_of_the_game, self.player_dict)

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

    def main(self, player_side):
        self.global_results_of_the_game = read_results_of_the_game()
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
        self.board = Board()
        # создаем шрифт
        self.font = pygame.font.SysFont('Arial', 20)
        # TODO: инициализация имен игроков будет доделана позже
        # инициализируем словарь игроков
        self.player_dict = {1: self.white_player_name, 0: self.black_player_name}
        # инициализируем остальные координаты
        self.msg = None
        self.reset_coords()
        self.draw = False
        self.mate = False
        self.result_of_the_game = None
        self.selected_figure = None
        self.avl_moves = []
        # игровой цикл
        while True:
            # обрабатываем события
            for event in pygame.event.get():
                # обрабатываем события
                if event.type == pygame.QUIT:
                    if self.game_mode == 2 or self.game_mode == 3 or self.game_mode == 5:
                        self.change_game_mode(5, True)
                    else:
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # если нажата не левая кнопка мыши, то ничего не делаем при нажатой кнопке
                        # в режиме 1 разрешен только выбор фигуры
                        if self.game_mode == 2:
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
                                self.game_mode = 3
                                continue
                        if self.game_mode == 3:
                            # print('ready_to_find')
                            result = self.get_mouse_selected_cell(event)
                            if result is not None:
                                selected_row, selected_col = result
                                if self.board.board[selected_row][selected_col] is not None:
                                    if self.board.board[selected_row][selected_col].color == self.player_color:
                                        if self.board.board[selected_row][
                                            selected_col] == self.selected_figure:  # если выбрана та же
                                            # фигура (пользователь еще раз нажал по ней)
                                            self.game_mode = 2
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
                                        elif move.type_of_move == config.CONVERSION_MOVE and \
                                                move.taken_figure is not None:
                                            self.sound_of_take_move.play()
                                        else:
                                            self.sound_of_normal_move.play()
                                        move.apply_move(self.board)
                                        # print(self.board.check_triple_repetition_of_a_position())
                                        # записываем координаты хода
                                        self.coords_before_move = (move.basic_row, move.basic_col)
                                        self.coords_after_move = (move.row, move.col)
                                        self.selected_figure = None
                                        self.avl_moves = []
                                        self.game_mode = 2
                                        self.change_player_color(config.OPPONENT_COLOR[self.player_color])
                                        if self.board.check_mat(self.player_color):
                                            self.msg = 'Шах и мат! Победил(а) игрок ' + self.player_dict[
                                                config.OPPONENT_COLOR[self.player_color]] + '!'
                                            self.game_mode = 6
                                            pygame.time.wait(
                                                250)  # добавляем задержку, чтобы звук совершения хода успел
                                            # проиграться
                                            if self.player_color == 0:
                                                self.result_of_the_game = 1
                                            else:
                                                self.result_of_the_game = -1
                                            self.sound_of_end_or_start_of_the_game.play()
                                        elif self.board.check_pat(self.player_color):
                                            self.msg = 'Пат! Достигнута ничья!'
                                            self.game_mode = 6
                                            pygame.time.wait(
                                                250)  # добавляем задержку, чтобы звук совершения хода успел
                                            # проиграться
                                            self.sound_of_end_or_start_of_the_game.play()
                                            self.result_of_the_game = 0
                                        elif self.board.check_triple_repetition_of_a_position():
                                            self.msg = 'Ничья! Троекратное повторение позиции!'
                                            self.game_mode = 6
                                            pygame.time.wait(250)
                                            self.sound_of_end_or_start_of_the_game.play()
                                            self.result_of_the_game = 0
                                        elif self.board.check_fifty_moves_rule():
                                            self.msg = 'Ничья! Правило пятидесяти ходов!'
                                            self.game_mode = 6
                                            pygame.time.wait(250)
                                            self.sound_of_end_or_start_of_the_game.play()
                                            self.result_of_the_game = 0
                                        if self.result_of_the_game is not None:
                                            write_result_of_the_game(self.white_player_name, self.black_player_name,
                                                                     self.result_of_the_game, self.player_dict)
                    if event.button == 3:
                        if self.game_mode == 6:
                            self.main(1)
                    if event.button == 4 and self.game_mode in [2, 3, 6]:
                        config.recount_coefficent_and_length_of_divider(2)
                    if event.button == 5 and self.game_mode in [2, 3, 6]:
                        config.recount_coefficent_and_length_of_divider(-2)
                    # TODO: ОСНОВНАЯ ЗАДАЧА - ПРОПИСАТЬ ВСЕ ОСТАЛЬНЫЕ РЕЖИМЫ РАБОТЫ ИГРЫ
                if event.type == pygame.MOUSEMOTION:
                    if self.game_mode == 3:
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
                if self.game_mode == 1:
                    self.redraw_players_name_screen(event)
                if self.game_mode == 5:
                    self.redraw_question_screen()
            # обновляем фон
            self.background.update()
            if self.game_mode not in [0, 1, 5]:
                self.redraw_game_screen()
            # обновляем окно
            pygame.display.flip()

    # функция отрисовки экрана с вопросом о продолжении игры
    def redraw_question_screen(self):
        # отрисовываем фон
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        # отрисовываю прямоугольник (подложку) для текста (для того, чтобы прямоугольник был полупрозрачным я
        # использую surface)
        surface = pygame.Surface((600, 600))
        surface.fill((35, 25, 95))
        surface.set_alpha(200)
        self.main_surface.blit(surface, (100, 100))
        font = pygame.font.Font(None, 51)
        text = font.render('Вы уверены, что хотите выйти?', True, (255, 0, 0))
        font = pygame.font.Font(None, 25)
        text1 = font.render('Ваш соперник будет объявлен победителем, если вы покинете игру!', True, (255, 255, 255))
        self.main_surface.blit(text, (130, 120))
        self.main_surface.blit(text1, (112, 170))
        for element in self.elements:
            element.process()

    # функция отрисовки начального экрана
    def redraw_main_screen(self):
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        # Код ниже отвечает за отрисовку информации из базы данных (она получена заранее в методе main и записана в
        # переменную global_results_of_the_game) в левой части экрана отрисовываеться информация о последних 3ех
        # играх в формате player_name1 vs player_name2. В правой - результат игры (Победил(а) player_name1 или
        # Ничья)
        if self.global_results_of_the_game:
            # отриовываем прямоугольник под информацию о последних играх (для того, чтобы он был полупрозрачный я
            # использую surface)
            surface = pygame.Surface((760, 250))
            surface.fill((35, 25, 95))
            surface.set_alpha(200)
            self.main_surface.blit(surface, (20, 20))
            # заголовок к информации о проследних играх
            font = pygame.font.Font(None, 25)
            text = font.render('Последние игры:', True, (255, 0, 0))
            self.main_surface.blit(text, (30, 30))
            # заголовок к результатам игр
            font = pygame.font.Font(None, 25)
            text = font.render('Результаты поледних игр:', True, (255, 0, 0))
            self.main_surface.blit(text, (470, 30))
            # отрисовываем информацию о последних играх
            font = pygame.font.Font(None, 18)
            counter_of_printed_games_info = 1
            for i in range(len(self.global_results_of_the_game), 0, -1):
                player_name_text = font.render(self.global_results_of_the_game[i][0] + ' vs ' +
                                               self.global_results_of_the_game[i][1], True, (255, 255, 255))
                result_of_the_game_text = font.render(self.global_results_of_the_game[i][2], True, (255, 255, 255))
                self.main_surface.blit(player_name_text, (35, 30 + counter_of_printed_games_info * 22))
                self.main_surface.blit(result_of_the_game_text, (485, 30 + counter_of_printed_games_info * 22))
                if counter_of_printed_games_info >= 10:
                    break
                counter_of_printed_games_info += 1

        for element in self.elements:
            element.process()  # обрабатываем элементы
        pygame.display.flip()  # обновляем окно

    def draw_players_name_screen(self):
        # рисуем цветной прямоугольник под текст и поля ввода (для того, чтобы он был полупрозрачный я использую
        # surface)
        surface = pygame.Surface((600, 400))
        surface.fill((35, 25, 95))
        surface.set_alpha(200)
        self.main_surface.blit(surface, (100, 100))
        # рисуем текст
        font = pygame.font.Font(None, 50)
        text = font.render('Введите имена игроков', True, (255, 255, 255))
        text_x = 100 + 600 // 2 - text.get_width() // 2
        text_y = 100 + 50
        self.main_surface.blit(text, (text_x, text_y))
        # рисуем текст
        font = pygame.font.Font(None, 30)
        text = font.render('Имя игрока за белых', True, (255, 255, 255))
        self.main_surface.blit(text, (162, 250))
        # рисуем текст
        font = pygame.font.Font(None, 30)
        text = font.render('Имя игрока за черных', True, (255, 255, 255))
        self.main_surface.blit(text, (150, 350))
        if self.msg:
            font = pygame.font.Font(None, 30)
            text = font.render(self.msg, True, (255, 0, 0))
            self.main_surface.blit(text, (175, 515))

    # функция отрисовки игрового экрана
    def redraw_game_screen(self):
        self.main_surface.blit(self.background.image, self.background.rect)  # отрисовываем фон
        for element in self.elements:
            if element.buttonText in ['Сдаться', 'Объявить ничью', 'Отменить ход']:
                if config.size_of_cell < 57:
                    element.process()  # обрабатываем элементы
            if element.buttonText in ['<- Назад']:
                if config.size_of_cell < 71:
                    element.process()
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
        # отрисовываем вторую границу, которая теперь состоит из четырех прямоугольников, два - сверху вниз,
        # два - млева направо, вне поля с запасов в coefficient пикселей и шириной в length_of_divider_between_cells
        # пикселей это спарва налево
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
                    config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell
                    + amount_of_row * config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells,
                    self.game_surface.get_height() - config.length_of_divider_between_cells * 2
                ))
                # справа налево
                pygame.draw.rect(self.game_surface, (0, 0, 0), (
                    config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell +
                    amount_of_row * config.length_of_divider_between_cells,
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
                if self.selected_figure is not None and help_row == self.selected_figure.row and help_col == \
                        self.selected_figure.col:
                    color = (135, 148, 212)
                if self.board.check_check(self.player_color) and self.board.get_king(
                        self.player_color).row == help_row and self.board.get_king(
                    self.player_color).col == help_col:
                    color = (255, 0, 0)
                # отрисовываем непосредственно клетки
                pygame.draw.rect(self.game_surface, color, (
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
                    + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
                    + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                    config.size_of_cell,
                    config.size_of_cell
                ))
                if (self.coords_before_move and self.coords_after_move) and (
                        (help_row == self.coords_before_move[0] and help_col == self.coords_before_move[1]) or (
                        help_row == self.coords_after_move[0] and help_col == self.coords_after_move[1])):
                    pygame.draw.rect(self.game_surface, (95, 41, 153), (
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col *
                        config.length_of_divider_between_cells,
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row *
                        config.length_of_divider_between_cells,
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
                                    config.length_of_divider_between_cells + config.coefficient +
                                    config.length_of_divider_between_cells + amount_of_col * config.size_of_cell +
                                    amount_of_col * config.length_of_divider_between_cells + indent,
                                    config.length_of_divider_between_cells + config.coefficient +
                                    config.length_of_divider_between_cells + amount_of_row * config.size_of_cell +
                                    amount_of_row * config.length_of_divider_between_cells + indent,
                                    config.size_of_cell - indent * 2,
                                    config.size_of_cell - indent * 2
                                ))
                            else:
                                pygame.draw.ellipse(self.game_surface, color_of_selection, (
                                    config.length_of_divider_between_cells + config.coefficient +
                                    config.length_of_divider_between_cells + amount_of_col * config.size_of_cell +
                                    amount_of_col * config.length_of_divider_between_cells + indent,
                                    config.length_of_divider_between_cells + config.coefficient +
                                    config.length_of_divider_between_cells + amount_of_row * config.size_of_cell +
                                    amount_of_row * config.length_of_divider_between_cells + indent,
                                    config.size_of_cell - indent * 2,
                                    config.size_of_cell - indent * 2
                                ))
                # отрисовываем буквы так, чтобы они появились в области с шириной coefficient пикселей
                if amount_of_row == 0:
                    text = self.font.render(
                        chr(amount_of_col + 65) if self.player_color == config.WHITE else chr(7 - amount_of_col + 65),
                        True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col *
                        config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient // 2 - text.get_height() // 2
                    ))
                if amount_of_row == 7:
                    text = self.font.render(
                        chr(amount_of_col + 65) if self.player_color == config.WHITE else chr(7 - amount_of_col + 65),
                        True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col *
                        config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                        self.game_surface.get_height() - config.length_of_divider_between_cells - config.coefficient //
                        2 - text.get_height() // 2
                    ))
                # отрисовываем цифры так, чтобы они появились в области с высотой coefficient пикселей
                if amount_of_col == 0:
                    text = self.font.render(
                        str(8 - amount_of_row) if self.player_color == 1 else str(amount_of_row + 1), True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        config.length_of_divider_between_cells + config.coefficient // 2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row *
                        config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                    ))
                if amount_of_col == 7:
                    text = self.font.render(
                        str(8 - amount_of_row) if self.player_color == 1 else str(amount_of_row + 1), True,
                        (0, 0, 0))
                    self.game_surface.blit(text, (
                        self.game_surface.get_width() - config.length_of_divider_between_cells - config.coefficient //
                        2 - text.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient +
                        config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row *
                        config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                    ))
        self.main_surface.blit(self.game_surface, (
            # отрисовываем холст на экране в первый раз c координатами, вычисленными по принципцу (длина\ширина
            # холста - длина\ширина экрана) / 2
            (self.width - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 +
                           config.coefficient * 2)) / 2,
            (self.height - (
                    config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 +
                    config.coefficient * 2)) / 2
        ))

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
                            config.length_of_divider_between_cells + config.coefficient +
                            config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col
                            * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                            board_to_work_with[amount_of_row][amount_of_col].image.get_width() // 2,
                            config.length_of_divider_between_cells + config.coefficient +
                            config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row
                            * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                            board_to_work_with[amount_of_row][amount_of_col].image.get_height() // 2
                        ))
                    except Exception:
                        pass
        self.main_surface.blit(self.game_surface, (  # отрисовываем холст на экране в первый раз c координатами,
            # вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
            (self.width - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient *
                           2)) / 2,
            (self.height - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient
                            * 2)) / 2,
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
                self.width - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient
                              * 2)) / 2
        event_y = mouse_event.pos[1] - (
                self.height - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 +
                               config.coefficient * 2)) / 2
        x = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells  # ряды
        for amount_of_row in range(8):
            # столбцы
            y = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
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

    # функция отрисовки экрана ввода имени игроков
    def redraw_players_name_screen(self, event):
        self.main_surface.blit(self.background.image, self.background.rect)
        for element in self.elements:
            element.process()  # обрабатываем элементы
        self.draw_players_name_screen()
        for input_box in self.input_boxes:
            input_box.handle_event(event)
            if len(input_box.text.replace(' ', '')) == 0:
                self.msg = 'Поле "имя игрока" не может быть пустым!'
            else:
                self.msg = None
        for input_box in self.input_boxes:
            input_box.update()
        for input_box in self.input_boxes:
            input_box.draw(self.main_surface)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game(1)
