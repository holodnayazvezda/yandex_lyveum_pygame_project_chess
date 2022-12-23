# импорт pygame
import pygame

import Pawn
# прочие импорта
from config import *
from background import Background
from button import Button
from Board import Board

# инициализируем необходимые переменные
background = None  # создаем фон
board = None  # создаем переменную доски
elements = []  # создаем список элементов
font = None  # создаем шрифт
main_surface = None  # создаем главное окно
game_surface = None  # создаем окно игры
width, height = 800, 800  # размеры окна
game_mode = None  # режим игры
player_color = None
# функция запуска всего


def change_game_mode(mode):  # функция смены режима игры которая вызывается кнопкой
    global game_mode
    game_mode = mode


def main(player_side):   # 1 если пользователь играет белыми, 0 если черными
    global background, board, elements, font, main_surface, width, height, game_mode, player_color
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
    # создаем доску
    board = Board(player_side)
    # создаем цвет
    player_color = player_side
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
                if game_mode != 0:
                    selected_figure = get_selected_figure(event, player_side)
                    if selected_figure is not None:
                        avl_moves = selected_figure.get_all_moves(board)
                        if avl_moves:
                            for move in avl_moves:
                                print(move)
                        else:
                            print("No moves available")
                    else:
                        print("None")
                # ОСНОВНАЯ ЗАДАЧА - ПРОПИСАТЬ ВСЕ ОСТАЛЬНЫЕ РЕЖИМЫ РАБОТЫ ИГРЫ
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
    global elements, board, main_surface, width, height
    main_surface.blit(background.image, background.rect)  # отрисовываем фон
    draw_cell()
    draw_figures()
    pygame.display.flip()  # обновляем окно


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
            # отрисовываем непосредственно клетки
            pygame.draw.rect(game_surface, (238, 232, 170) if (amount_of_row + amount_of_col) % 2 == 0 else (160, 82, 45), (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                    size_of_cell,
                    size_of_cell
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


def draw_figures():
    for amount_of_row in range(8):
        for amount_of_col in range(8):
            if board.board[amount_of_row][amount_of_col] is not None:  # отрисовываем фигуры
                game_surface.blit(board.board[amount_of_row][amount_of_col].image, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - board.board[amount_of_row][amount_of_col].image.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - board.board[amount_of_row][amount_of_col].image.get_height() // 2
                ))
    main_surface.blit(game_surface, (  # отрисовываем холст на экране в первый раз c координатами, вычисленными по
        # принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
        (height - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
    ))


def get_selected_figure(mouse_event, player_side):
    # в этой функции мы должны вернуть фигуру, которая была выбрана если кликнули по месту, где ее нет, то вернуть None
    for amount_of_row in range(8):
        for amount_of_col in range(8):
            if board.board[amount_of_row][amount_of_col] is not None:
                if board.board[amount_of_row][amount_of_col].color == player_side:
                    if board.board[amount_of_row][amount_of_col].image.get_rect(
                            topleft=(
                                length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_col + 1) * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2,
                                length_of_divider_between_cells + coefficient + length_of_divider_between_cells + (amount_of_row + 1) * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2
                            )
                    ).collidepoint(mouse_event.pos):
                        return board.board[amount_of_row][amount_of_col]


if __name__ == '__main__':
    main(0)  # пока 1 - игра за белых, 0 - игра за черных
