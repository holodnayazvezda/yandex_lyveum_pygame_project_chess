# импорт pygame
import pygame

# прочие импорта
import config
from background import Background
from button import Button
from Board import Board
from config import OPPONENT_COLOR

# инициализируем необходимые переменные
background = None  # создаем фон
board = None  # создаем переменную доски
elements = []  # создаем список элементов
font = None  # создаем шрифт
main_surface = None  # создаем главное окно
game_surface = None  # создаем окно игры
width, height = 800, 800  # размеры окна
game_mode = None  # режим игры
player_color = None  # цвет игрока
selected_figure = None  # выбранная фигура
avl_moves = []  # доступные ходы
mouse_move_selected_cell = None
coords_before_move = None
coords_after_move = None
sound_of_normal_move = None  # звук обычного хода
sound_of_take_move = None  # звук взятия фигуры
sound_of_and_or_start_of_the_game = None  # звук начала и конца игры
white_player_name = None
black_player_name = None
msg = None
player_dict = {}
draw = False
mate = False
# функция запуска всего


def reset_coords():
    global coords_before_move, coords_after_move
    coords_before_move = None
    coords_after_move = None


def change_game_mode(mode):  # функция смены режима игры которая вызывается кнопкой
    global game_mode, sound_of_and_or_start_of_the_game, elements
    game_mode = mode
    sound_of_and_or_start_of_the_game.play()
    elements = [
        Button(main_surface, 56, 750, 208, 44, 'Сдаться', declare_a_mate, None, False, 'Arial', 20),
        Button(main_surface, 296, 750, 208, 44, 'Объявить ничью', declare_a_draw, None, False,
               'Arial', 20),
        Button(main_surface, 536, 750, 208, 44, 'Отменить ход', back, None, False, 'Arial', 20)]  # создаем кнопки
    # для игры


def change_player_color(color):  # функция смены цвета игрока которая вызывается кнопкой
    global player_color
    player_color = color


def declare_a_draw():
    global draw, msg, game_mode, sound_of_and_or_start_of_the_game
    if not draw and not mate and not board.check_mat(player_color) and not board.check_pat(player_color):
        draw = True
        msg = 'Ничья! Достигнута ничья!'
        sound_of_and_or_start_of_the_game.play()
        game_mode = 4


def declare_a_mate():
    global mate, msg, player_dict, player_color, game_mode, sound_of_and_or_start_of_the_game
    if not mate and not draw and not board.check_mat(player_color) and not board.check_pat(player_color):
        mate = True
        msg = 'Игрок ' + player_dict[player_color] + ' сдался! Игрок ' + player_dict[OPPONENT_COLOR[player_color]] + \
              ' победил!'
        sound_of_and_or_start_of_the_game.play()
        game_mode = 4


def back():
    global board, player_color, coords_before_move, coords_after_move, selected_figure, avl_moves
    if not mate and not draw and not board.check_mat(player_color) and not board.check_pat(player_color):
        if board.all_moves:
            board.all_moves[-1].undo_move(board)  # отменим последний ход
            # далее меняем необходимые переменные
            player_color = OPPONENT_COLOR[player_color]
            if board.all_moves:
                coords_before_move = (board.all_moves[-1].basic_row, board.all_moves[-1].basic_col)
                coords_after_move = (board.all_moves[-1].row, board.all_moves[-1].col)
            else:
                coords_before_move = None

                coords_after_move = None
            selected_figure = None
            avl_moves = []


def main(player_side, white_name=None, black_name=None):   # 1 если пользователь играет белыми, 0 если
    # черными
    global background, board, elements, font, main_surface, game_surface, width, height, game_mode, player_color, selected_figure, avl_moves, mouse_move_selected_cell, coords_before_move, coords_after_move, sound_of_move, white_player_name, black_player_name, msg, player_dict, sound_of_and_or_start_of_the_game, draw, mate
    # инициализируем pygame
    game_mode = 0  # режим игры 0 - начальный экран с кнопками
    pygame.init()
    pygame.display.set_caption('Chess')
    # создаем фон
    background = Background('images/fon.jpg', [0, 0])
    main_surface = pygame.display.set_mode((width, height))
    main_surface.blit(background.image, background.rect)  # отрисовываем фон
    # создаем звук обычного хода
    sound_of_move = pygame.mixer.Sound('sounds/normal_move.mp3')
    # создаем звук взятия фигуры
    sound_of_take_move = pygame.mixer.Sound('sounds/take_move.mp3')
    # создаем звук начала или конца игры
    sound_of_and_or_start_of_the_game = pygame.mixer.Sound('sounds/start_or_end.mp3')
    elements = [Button(main_surface, 250, 290, 300, 100, "Начать игру", change_game_mode, 1, False)]  # режим 1 -
    # игра (без зажатой кнопки просто отрисовывае поле, если кнопка нажата, то ищем фигуру, которую выбрал игрок)
    # создаем цвет
    player_color = player_side
    # создаем доску
    board = Board(player_color)
    # создаем шрифт
    font = pygame.font.SysFont('Arial', 20)
    # инициалируем игроков
    if white_name is not None:
        white_player_name = white_name
    if black_name is not None:
        black_player_name = black_name
    # инициализируем словарь игроков
    player_dict = {1: white_player_name, 0: black_player_name}
    # инициализируем остальные координаты
    msg = None
    reset_coords()
    draw = False
    mate = False
    while True:
        # обрабатываем события
        for event in pygame.event.get():
            # обрабатываем события
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # если нажата не левая кнопка мыши, то ничего не делаем
                    # при нажатой кнопке в режиме 1 разрешен только выбор фигуры
                    if game_mode == 1:
                        if selected_figure:
                            figure = get_selected_figure(event, player_color)
                            # print(figure)
                            if figure and figure == selected_figure:
                                selected_figure = None
                                avl_moves = []
                                continue
                            selected_figure = figure
                        else:
                            selected_figure = get_selected_figure(event, player_color)
                        if selected_figure is not None:
                            avl_moves = selected_figure.get_all_moves(board)
                        else:
                            avl_moves = []
                        # for move in avl_moves:
                            # print(move)
                        if avl_moves:
                            # reset_coords()  # сбрасываем координаты, возможно, что это необходимо делать, когда мы просто
                            # определили, что фигура не None
                            game_mode = 2
                            continue
                        # print(game_mode)
                    if game_mode == 2:
                        # print('ready_to_find')
                        result = get_mouse_selected_cell(event)
                        if result is not None:
                            selected_row, selected_col = result
                            if board.board[selected_row][selected_col] is not None:
                                if board.board[selected_row][selected_col].color == player_color:
                                    if board.board[selected_row][selected_col] == selected_figure:  # если выбрана та же
                                        # фигура (пользователь еще раз нажал по ней)
                                        game_mode = 1
                                        avl_moves = []
                                        selected_figure = None
                                        continue
                                    selected_figure = board.board[selected_row][selected_col]
                                    avl_moves = selected_figure.get_all_moves(board)
                                    # reset_coords()
                                    continue
                            for move in avl_moves:
                                if move.row == selected_row and move.col == selected_col:
                                    if move.type_of_move in [config.TAKE_MOVE, config.PASSED_TAKE_MOVE]:
                                        sound_of_take_move.play()
                                    elif move.type_of_move == config.CONVERSION_MOVE and move.taken_figure is not None:
                                        sound_of_take_move.play()
                                    else:
                                        sound_of_move.play()
                                    move.apply_move(board)
                                    print(board.check_triple_repetition_of_a_position())
                                    # записываем координаты хода
                                    coords_before_move = (move.basic_row, move.basic_col)
                                    coords_after_move = (move.row, move.col)
                                    selected_figure = None
                                    avl_moves = []
                                    game_mode = 1
                                    change_player_color(config.OPPONENT_COLOR[player_color])
                                    if board.check_mat(player_color):
                                        msg = 'Шах и мат! Победил(а) игрок ' + player_dict[config.OPPONENT_COLOR[player_color]] + '!'
                                        game_mode = 4
                                        pygame.time.wait(250)  # добавляем задержку, чтобы звук совершения хода успел
                                        # проиграться
                                        sound_of_and_or_start_of_the_game.play()
                                    elif board.check_pat(player_color):
                                        msg = 'Пат! Достигнута ничья!'
                                        game_mode = 4
                                        pygame.time.wait(250)  # добавляем задержку, чтобы звук совершения хода успел
                                        # проиграться
                                        sound_of_and_or_start_of_the_game.play()
                                    elif board.check_triple_repetition_of_a_position():
                                        msg = 'Ничья! Троекратное повторение позиции!'
                                        game_mode = 4
                                        pygame.time.wait(250)
                                        sound_of_and_or_start_of_the_game.play()
                                    elif board.check_fifty_moves_rule():
                                        msg = 'Ничья! Правило пятидесяти ходов!'
                                        game_mode = 4
                                        pygame.time.wait(250)
                                        sound_of_and_or_start_of_the_game.play()
                if event.button == 3:
                    if game_mode == 4:
                        main(1, 'Денистон', 'Красавчик')
                if event.button == 4:
                    config.recount_coefficent_and_length_of_divider(2)
                if event.button == 5:
                    config.recount_coefficent_and_length_of_divider(-2)
                # TODO: ОСНОВНАЯ ЗАДАЧА - ПРОПИСАТЬ ВСЕ ОСТАЛЬНЫЕ РЕЖИМЫ РАБОТЫ ИГРЫ
            if event.type == pygame.MOUSEMOTION:
                if game_mode == 2:
                    mouse_move_selected_cell = get_mouse_selected_cell(event)
                    if mouse_move_selected_cell is not None:
                        if player_color == config.WHITE:
                            mouse_move_selected_cell[0] = 7 - mouse_move_selected_cell[0]
                        else:
                            mouse_move_selected_cell[1] = 7 - mouse_move_selected_cell[1]
                    # print(mouse_move_selected_cell)
            # обрабатываем режимы игры
            if game_mode == 0:
                redraw_main_screen()
        # обновляем фон
        background.update()
        if game_mode != 0:
            redraw_game_screen()
        # обновляем окно
        pygame.display.flip()


# функция отрисовки начального экрана
def redraw_main_screen():
    global elements
    main_surface.blit(background.image, background.rect)  # отрисовываем фон
    for element in elements:
        element.process()  # обрабатываем элементы
    pygame.display.flip()  # обновляем окно


# функция отрисовки игрового экрана
def redraw_game_screen():
    global elements, board, main_surface, width, height, player_color
    main_surface.blit(background.image, background.rect)  # отрисовываем фон
    for element in elements:
        element.process()  # обрабатываем элементы
    draw_cell()
    draw_figures(board, player_color)
    draw_msg()
    pygame.display.flip()  # обновляем окно


# функция, которая отрисовывает доску
def draw_cell():  # функция отрисовки клеток
    global main_surface, width, height, game_surface, background, player_color
    # создаем холст с математически-вычисленными размерами клеток и разделителей
    game_surface = pygame.Surface((config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2,
                                   config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2))
    game_surface.blit(background.image, background.rect)
    game_surface.fill((35, 35, 35))
    pygame.draw.rect(game_surface, (0, 0, 0), (0, 0, config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2,
                                               config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2),
                     config.length_of_divider_between_cells)
    # отрисовываю границу с запсом в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
    pygame.draw.rect(game_surface, (210, 202, 140), (
        config.length_of_divider_between_cells,
        config.length_of_divider_between_cells,
        game_surface.get_width() - config.length_of_divider_between_cells * 2,
        game_surface.get_height() - config.length_of_divider_between_cells * 2
    ), config.coefficient)
    # отрисовываем вторую границу, которая теперь состоит из четырех прямоугольников, два - сверху вниз, два - млева направо, вне поля с запасов в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
    # это спарва налево
    pygame.draw.rect(game_surface, (0, 0, 0), (
        config.length_of_divider_between_cells,
        config.coefficient + config.length_of_divider_between_cells,
        game_surface.get_width() - config.length_of_divider_between_cells * 2,
        config.length_of_divider_between_cells
    ))
    pygame.draw.rect(game_surface, (0, 0, 0), (
        config.length_of_divider_between_cells,
        game_surface.get_height() - config.coefficient - config.length_of_divider_between_cells * 2,
        game_surface.get_width() - config.length_of_divider_between_cells * 2,
        config.length_of_divider_between_cells
    ))
    # это сверху вниз
    pygame.draw.rect(game_surface, (0, 0, 0), (
        config.coefficient + config.length_of_divider_between_cells,
        config.length_of_divider_between_cells,
        config.length_of_divider_between_cells,
        game_surface.get_height() - config.length_of_divider_between_cells * 2
    ))
    pygame.draw.rect(game_surface, (0, 0, 0), (
        game_surface.get_width() - config.coefficient - config.length_of_divider_between_cells * 2,
        config.length_of_divider_between_cells,
        config.length_of_divider_between_cells,
        game_surface.get_height() - config.length_of_divider_between_cells * 2
    ))
    # отрисовываем доску по рядам (row - номер ряда, col - номер клетки в ряду row), не забываем про разделитель
    for amount_of_row in range(8):
        # отрисовываем границу каждого ряда не рисуем, если нулевая позиция
        if amount_of_row != 0:
            # сверху в низ
            pygame.draw.rect(game_surface, (0, 0, 0), (
                config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                config.length_of_divider_between_cells,
                config.length_of_divider_between_cells,
                game_surface.get_height() - config.length_of_divider_between_cells * 2
            ))
            # справа налево
            pygame.draw.rect(game_surface, (0, 0, 0), (
                config.length_of_divider_between_cells,
                config.length_of_divider_between_cells + config.coefficient + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                game_surface.get_width() - config.length_of_divider_between_cells * 2,
                config.length_of_divider_between_cells
            ))
        for amount_of_col in range(8):
            if player_color == config.WHITE:
                help_row, help_col = 7 - amount_of_row, amount_of_col
            else:
                help_row, help_col = amount_of_row, 7 - amount_of_col
            if (amount_of_row + amount_of_col) % 2 == 0:
                color = (238, 232, 170)
            else:
                color = (160, 82, 45)
            if selected_figure is not None and help_row == selected_figure.row and help_col == selected_figure.col:
                color = (135, 148, 212)
            if board.check_check(player_color) and board.get_king(player_color).row == help_row and board.get_king(player_color).col == help_col:
                color = (255, 0, 0)
            # отрисовываем непосредственно клетки
            pygame.draw.rect(game_surface, color, (
                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells,
                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                config.size_of_cell,
                config.size_of_cell
            ))
            if (coords_before_move and coords_after_move) and ((help_row == coords_before_move[0] and help_col == coords_before_move[1]) or (help_row == coords_after_move[0] and help_col == coords_after_move[1])):
                pygame.draw.rect(game_surface, (95, 41, 153), (
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells,
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells,
                    config.size_of_cell,
                    config.size_of_cell
                ), 5)
            if avl_moves:
                for move in avl_moves:
                    if help_row == move.row and help_col == move.col:
                        indent = round(config.size_of_cell * 0.3)
                        color_of_selection = (82, 209, 25)
                        if board.board[help_row][help_col] is not None and board.board[help_row][help_col].color != player_color and board.under_attack(help_row, help_col, OPPONENT_COLOR[player_color]):
                            indent = round(config.size_of_cell * 0.13)
                            color_of_selection = (255, 50, 50)
                        if mouse_move_selected_cell and amount_of_row == mouse_move_selected_cell[0] and amount_of_col == mouse_move_selected_cell[1]:
                            indent = 0
                            pygame.draw.rect(game_surface, color_of_selection, (
                                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + indent,
                                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + indent,
                                config.size_of_cell - indent * 2,
                                config.size_of_cell - indent * 2
                            ))
                        else:
                            pygame.draw.ellipse(game_surface, color_of_selection, (
                                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + indent,
                                config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + indent,
                                config.size_of_cell - indent * 2,
                                config.size_of_cell - indent * 2
                            ))
            # отрисовываем буквы так, чтобы они появились в области с шириной coefficient пикселей
            if amount_of_row == 0:
                text = font.render(chr(amount_of_col + 65) if player_color == config.WHITE else chr(7 - amount_of_col + 65), True, (0, 0, 0))
                game_surface.blit(text, (
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                    config.length_of_divider_between_cells + config.coefficient // 2 - text.get_height() // 2
                ))
            if amount_of_row == 7:
                text = font.render(chr(amount_of_col + 65) if player_color == config.WHITE else chr(7 - amount_of_col + 65), True, (0, 0, 0))
                game_surface.blit(text, (
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_width() // 2,
                    game_surface.get_height() - config.length_of_divider_between_cells - config.coefficient // 2 - text.get_height() // 2
                ))
            # отрисовываем цифры так, чтобы они появились в области с высотой coefficient пикселей
            if amount_of_col == 0:
                text = font.render(str(8 - amount_of_row) if player_color == 1 else str(amount_of_row + 1), True, (0, 0, 0))
                game_surface.blit(text, (
                    config.length_of_divider_between_cells + config.coefficient // 2 - text.get_width() // 2,
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                ))
            if amount_of_col == 7:
                text = font.render(str(8 - amount_of_row) if player_color == 1 else str(amount_of_row + 1), True, (0, 0, 0))
                game_surface.blit(text, (
                    game_surface.get_width() - config.length_of_divider_between_cells - config.coefficient // 2 - text.get_width() // 2,
                    config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 - text.get_height() // 2
                ))
    main_surface.blit(game_surface, (
    # отрисовываем холст на экране в первый раз c координатами, вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
        (height - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
    ))
    #board.print_board()


# функция, которая отрисовывает фигуры на доске
def draw_figures(board, player_color):
    board_to_work_with = board.board.copy()
    # переворасиваем в зависимости от цвета игрока
    if player_color == config.BLACK:
        board_to_work_with = list(map(lambda row: row[::-1], board_to_work_with))
    else:
        board_to_work_with = board_to_work_with[::-1]
    for amount_of_row in range(8):
        for amount_of_col in range(8):
            # если в клетке есть фигура
            if board_to_work_with[amount_of_row][amount_of_col]:
                # отрисовываем фигуру
                try:
                    game_surface.blit(board_to_work_with[amount_of_row][amount_of_col].image, (
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_col * config.size_of_cell + amount_of_col * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                        board_to_work_with[amount_of_row][amount_of_col].image.get_width() // 2,
                        config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells + amount_of_row * config.size_of_cell + amount_of_row * config.length_of_divider_between_cells + config.size_of_cell // 2 -
                        board_to_work_with[amount_of_row][amount_of_col].image.get_height() // 2
                    ))
                except Exception:
                    pass
    main_surface.blit(game_surface, (  # отрисовываем холст на экране в первый раз c координатами, вычисленными по
        # принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
        (height - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2,
    ))


def get_selected_figure(mouse_event, player_color):
    event_x = mouse_event.pos[0] - (width - (
            config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
    event_y = mouse_event.pos[1] - (height - (
            config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
    # в этой функции мы должны вернуть фигуру, которая была выбрана если кликнули по месту, где ее нет, то вернуть None
    board_to_work_with = board.board.copy()
    # переворасиваем в зависимости от цвета игрока
    if player_color == config.BLACK:
        board_to_work_with = list(map(lambda row: row[::-1], board_to_work_with))
    else:
        board_to_work_with = board_to_work_with[::-1]
    x = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
    for amount_of_row in range(8):
        y = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells
        for amount_of_col in range(8):
            if board_to_work_with[amount_of_row][amount_of_col] is not None:
                if board_to_work_with[amount_of_row][amount_of_col].color == player_color:
                    try:
                        if pygame.Rect(y, x, config.size_of_cell, config.size_of_cell).collidepoint((event_x, event_y)):
                            return board_to_work_with[amount_of_row][amount_of_col]
                    except Exception:
                        pass
            y += config.size_of_cell + config.length_of_divider_between_cells
        x += config.size_of_cell + config.length_of_divider_between_cells


# это функция для поиска координат нажатия мыши относительно поля и массива board.board
def get_mouse_selected_cell(mouse_event):
    event_x = mouse_event.pos[0] - (
                width - (
                config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
    event_y = mouse_event.pos[1] - (
                height - (config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2)) / 2
    x = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells  # ряды
    for amount_of_row in range(8):
        y = config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells  # столбцы
        for amount_of_col in range(8):
            try:
                if pygame.Rect(y, x, config.size_of_cell, config.size_of_cell).collidepoint((event_x, event_y)):
                    if player_color == config.BLACK:
                        return [amount_of_row, 7 - amount_of_col]
                    return [7 - amount_of_row, amount_of_col]
            except Exception:
                pass
            y += config.size_of_cell + config.length_of_divider_between_cells
        x += config.size_of_cell + config.length_of_divider_between_cells


def draw_msg():
    global msg
    if msg:
        size_of_font = round((config.length_of_divider_between_cells + config.coefficient + config.length_of_divider_between_cells +
                              config.size_of_cell * 8 + config.length_of_divider_between_cells * 11 + config.coefficient * 2) / len(msg) * 1.5)
        font = pygame.font.SysFont('Arial', size_of_font, True)
        text = font.render(msg, True, (255, 0, 0))
        main_surface.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.update()


if __name__ == '__main__':
    main(1, 'Даниил', 'Виктор')  # пока 1 - игра за белых, 0 - игра за черных
