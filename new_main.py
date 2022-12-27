# импорт pygame
import pygame

import Pawn
# прочие импорта
from config import *
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
# функция запуска всего


def change_game_mode(mode):  # функция смены режима игры которая вызывается кнопкой
    global game_mode
    game_mode = mode


def change_player_color(color):  # функция смены цвета игрока которая вызывается кнопкой
    global player_color
    player_color = color


def main(player_side):   # 1 если пользователь играет белыми, 0 если черными
    global background, board, elements, font, main_surface, game_surface, width, height, game_mode, player_color, selected_figure, avl_moves
    # инициализируем pygame
    game_mode = 0  # режим игры 0 - начальный экран с кнопками
    pygame.init()
    pygame.display.set_caption('Chess')
    # создаем фон
    background = Background('images/fon.jpg', [0, 0])
    main_surface = pygame.display.set_mode((width, height))
    main_surface.blit(background.image, background.rect)  # отрисовываем фон
    elements = [Button(main_surface, 250, 290, 300, 100, "Начать игру", change_game_mode, 1, False)]  # режим 1 -
    # игра (без зажатой кнопки просто отрисовывае поле, если кнопка нажата, то ищем фигуру, которую выбрал игрок)
    # создаем цвет
    player_color = player_side
    # создаем доску
    board = Board(player_color)
    # создаем шрифт
    font = pygame.font.SysFont('Arial', 20)
    while True:
        # обрабатываем события
        for event in pygame.event.get():
            # обрабатываем события
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:  # если нажата не левая кнопка мыши, то ничего не делаем
                    continue
                # при нажатой кнопке в режиме 1 разрешен только выбор фигуры
                if game_mode == 1:
                    selected_figure = get_selected_figure(event, player_color)
                    if selected_figure is not None:
                        avl_moves = selected_figure.get_all_moves(board)
                    else:
                        avl_moves = []
                    for move in avl_moves:
                        print(move)
                    if avl_moves:
                        game_mode = 2
                        continue
                if game_mode == 2:
                    print('ready_to_find')
                    result = get_mouse_selected_cell(event)
                    if result is not None:
                        selected_row, selected_col = result
                        if board.board[selected_row][selected_col] is not None:
                            if board.board[selected_row][selected_col].color == player_color:
                                selected_figure = board.board[selected_row][selected_col]
                                avl_moves = selected_figure.get_all_moves(board)
                                game_mode = 1
                                continue
                        for move in avl_moves:
                            if move.row == selected_row and move.col == selected_col:
                                move.apply_move(board)
                                selected_figure = None
                                avl_moves = []
                                game_mode = 1
                                change_player_color(OPPONENT_COLOR[player_color])
                                break
                # TODO: ОСНОВНАЯ ЗАДАЧА - ПРОПИСАТЬ ВСЕ ОСТАЛЬНЫЕ РЕЖИМЫ РАБОТЫ ИГРЫ
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
    draw_cell()
    draw_figures(board, player_color)
    pygame.display.flip()  # обновляем окно


# функция, которая отрисовывает доску
def draw_cell():  # функция отрисовки клеток
    global main_surface, width, height, game_surface, background, player_color
    # создаем холст с математически-вычисленными размерами клеток и разделителей
    game_surface = pygame.Surface((size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2,
                                   size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2))
    game_surface.blit(background.image, background.rect)
    game_surface.fill((35, 35, 35))
    # отрисовываю границу с запсом в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
    pygame.draw.rect(game_surface, (210, 202, 140), (
        length_of_divider_between_cells,
        length_of_divider_between_cells,
        game_surface.get_width() - length_of_divider_between_cells * 2,
        game_surface.get_height() - length_of_divider_between_cells * 2
    ), coefficient)
    # отрисовываем вторую границу, которая теперь состоит из четырех прямоугольников, два - сверху вниз, два - млева направо, вне поля с запасов в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
    # это спарва налево
    pygame.draw.rect(game_surface, (0, 0, 0), (
        length_of_divider_between_cells,
        coefficient + length_of_divider_between_cells,
        game_surface.get_width() - length_of_divider_between_cells * 2,
        length_of_divider_between_cells
    ))
    pygame.draw.rect(game_surface, (0, 0, 0), (
        length_of_divider_between_cells,
        game_surface.get_height() - coefficient - length_of_divider_between_cells * 2,
        game_surface.get_width() - length_of_divider_between_cells * 2,
        length_of_divider_between_cells
    ))
    # это сверху вниз
    pygame.draw.rect(game_surface, (0, 0, 0), (
        coefficient + length_of_divider_between_cells,
        length_of_divider_between_cells,
        length_of_divider_between_cells,
        game_surface.get_height() - length_of_divider_between_cells * 2
    ))
    pygame.draw.rect(game_surface, (0, 0, 0), (
        game_surface.get_width() - coefficient - length_of_divider_between_cells * 2,
        length_of_divider_between_cells,
        length_of_divider_between_cells,
        game_surface.get_height() - length_of_divider_between_cells * 2
    ))
    # отрисовываем доску по рядам (row - номер ряда, col - номер клетки в ряду row), не забываем про разделитель
    for amount_of_row in range(8):
        # отрисовываем границу каждого ряда не рисуем, если нулевая позиция
        if amount_of_row != 0:
            # сверху в низ
            pygame.draw.rect(game_surface, (0, 0, 0), (
                length_of_divider_between_cells + coefficient + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                length_of_divider_between_cells,
                length_of_divider_between_cells,
                game_surface.get_height() - length_of_divider_between_cells * 2
            ))
            # справа налево
            pygame.draw.rect(game_surface, (0, 0, 0), (
                length_of_divider_between_cells,
                length_of_divider_between_cells + coefficient + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                game_surface.get_width() - length_of_divider_between_cells * 2,
                length_of_divider_between_cells
            ))
        for amount_of_col in range(8):
            if player_color == WHITE:
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
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                    size_of_cell,
                    size_of_cell
                ))
            if avl_moves:
                for move in avl_moves:
                    if help_row == move.row and help_col == move.col:
                        indent = 20
                        color_of_selection = (82, 209, 25)
                        if board.board[help_row][help_col] is not None and board.board[help_row][help_col].color != player_color and board.under_attack(help_row, help_col, OPPONENT_COLOR[player_color]):
                            indent = 8
                            color_of_selection = (200, 0, 0)
                        pygame.draw.ellipse(game_surface, color_of_selection, (
                            length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + indent,
                            length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + indent,
                            size_of_cell - indent * 2,
                            size_of_cell - indent * 2
                        ))
            # отрисовываем буквы так, чтобы они появились в области с шириной coefficient пикселей
            if amount_of_row == 0:
                text = font.render(chr(amount_of_col + 65) if player_color == WHITE else chr(7 - amount_of_col + 65), True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient // 2 - text.get_height() // 2
                ))
            if amount_of_row == 7:
                text = font.render(chr(amount_of_col + 65) if player_color == WHITE else chr(7 - amount_of_col + 65), True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - text.get_width() // 2,
                    game_surface.get_height() - length_of_divider_between_cells - coefficient // 2 - text.get_height() // 2
                ))
            # отрисовываем цифры так, чтобы они появились в области с высотой coefficient пикселей
            if amount_of_col == 0:
                text = font.render(str(8 - amount_of_row) if player_color == 1 else str(amount_of_row + 1), True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - text.get_height() // 2
                ))
            if amount_of_col == 7:
                text = font.render(str(8 - amount_of_row) if player_color == 1 else str(amount_of_row + 1), True, (0, 0, 0))
                game_surface.blit(text, (
                    game_surface.get_width() - length_of_divider_between_cells - coefficient // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - text.get_height() // 2
                ))
    main_surface.blit(game_surface, (
    # отрисовываем холст на экране в первый раз c координатами, вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
        (height - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
    ))
    #board.print_board()


# функция, которая отрисовывает фигуры на доске
def draw_figures(board, player_color):
    board_to_work_with = board.board.copy()
    # переворасиваем в зависимости от цвета игрока
    if player_color == BLACK:
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
                        length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 -
                        board_to_work_with[amount_of_row][amount_of_col].image.get_width() // 2,
                        length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 -
                        board_to_work_with[amount_of_row][amount_of_col].image.get_height() // 2
                    ))
                except Exception:
                    pass
    main_surface.blit(game_surface, (  # отрисовываем холст на экране в первый раз c координатами, вычисленными по
        # принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
        (height - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
    ))


def get_selected_figure(mouse_event, player_color):
    # в этой функции мы должны вернуть фигуру, которая была выбрана если кликнули по месту, где ее нет, то вернуть None
    board_to_work_with = board.board.copy()
    # переворасиваем в зависимости от цвета игрока
    if player_color == BLACK:
        board_to_work_with = list(map(lambda row: row[::-1], board_to_work_with))
    else:
        board_to_work_with = board_to_work_with[::-1]
    for amount_of_row in range(8):
        for amount_of_col in range(8):
            if board_to_work_with[amount_of_row][amount_of_col] is not None:
                if board_to_work_with[amount_of_row][amount_of_col].color == player_color:
                    try:
                        if board_to_work_with[amount_of_row][amount_of_col].image.get_rect(
                                topleft=(
                                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_col + 1) * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2,
                                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_row + 1) * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2
                                )
                        ).collidepoint(mouse_event.pos):
                            return board_to_work_with[amount_of_row][amount_of_col]
                    except Exception:
                        pass


# это функция для поиска координат нажатия мыши относительно поля и массива board.board
def get_mouse_selected_cell(mouse_event):
    for amount_of_row in range(8):
        for amount_of_col in range(8):
            try:
                if pygame.Rect(
                            length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_col + 1) * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2,
                            length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_row + 1) * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2,
                            size_of_cell,
                            size_of_cell
                ).collidepoint(mouse_event.pos):
                    if player_color == BLACK:
                        return amount_of_row, 7 - amount_of_col
                    return 7 - amount_of_row, amount_of_col
            except Exception:
                pass




if __name__ == '__main__':
    main(1)  # пока 1 - игра за белых, 0 - игра за черных
