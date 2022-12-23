import pygame
from background import Background
from button import Button
from Board import Board
from config import *

SIZE = width, height = 800, 800
pygame.init()
screen = pygame.display.set_mode(SIZE)
# шахматный фон
background = Background('images/fon.jpg', [0, 0])
elements_to_process = []
font = pygame.font.SysFont('Arial', 20)
board = Board()
# создаем холст с математически-вычисленными размерами клеток и разделителей
game_surface = pygame.Surface((size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2,
                               size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2))
# все возможные ходы для выбранной фигуры
avl_moves = []
# это функция главного меню, создает новый холст с изображением background


def start_game():
    global elements_to_process, board, game_surface

    board.print_board()
    game_surface.blit(background.image, background.rect)
    game_surface.fill((35, 35, 35))
    # отрисовываю первую границу вне поля границу с запсом в coefficient пикселей и шириной в length_of_divider_between_cells пикселей
    pygame.draw.rect(game_surface, (0, 0, 0), (0, 0, *game_surface.get_size()), length_of_divider_between_cells)
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
            if board.board[amount_of_row][amount_of_col].color == 0:
                pygame.draw.rect(game_surface, board.board[amount_of_row][amount_of_col].get_color(), (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                    size_of_cell,
                    size_of_cell
                ))
            else:
                pygame.draw.rect(game_surface, board.board[amount_of_row][amount_of_col].get_color(), (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells,
                    size_of_cell,
                    size_of_cell
                ))
            # отрисовываем буквы так, чтобы они появились в области с шириной coefficient пикселей
            if amount_of_row == 0:
                text = font.render(board.board[amount_of_row][amount_of_col].col, True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient // 2 - text.get_height() // 2
                ))
            if amount_of_row == 7:
                text = font.render(board.board[amount_of_row][amount_of_col].col, True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - text.get_width() // 2,
                    game_surface.get_height() - length_of_divider_between_cells - coefficient // 2 - text.get_height() // 2
                ))
            # отрисовываем цифры так, чтобы они появились в области с высотой coefficient пикселей
            if amount_of_col == 0:
                text = font.render(str(board.board[amount_of_row][amount_of_col].row), True, (0, 0, 0))
                game_surface.blit(text, (
                    length_of_divider_between_cells + coefficient // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - text.get_height() // 2
                ))
            if amount_of_col == 7:
                text = font.render(str(board.board[amount_of_row][amount_of_col].row), True, (0, 0, 0))
                game_surface.blit(text, (
                    game_surface.get_width() - length_of_divider_between_cells - coefficient // 2 - text.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - text.get_height() // 2
                ))
            if board.board[amount_of_row][amount_of_col].figure is not None:  # отрисовываем фигуры
                game_surface.blit(board.board[amount_of_row][amount_of_col].figure.image, (
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_col * size_of_cell + amount_of_col * length_of_divider_between_cells + size_of_cell // 2 - board.board[amount_of_row][amount_of_col].figure.image.get_width() // 2,
                    length_of_divider_between_cells + coefficient + length_of_divider_between_cells + amount_of_row * size_of_cell + amount_of_row * length_of_divider_between_cells + size_of_cell // 2 - board.board[amount_of_row][amount_of_col].figure.image.get_height() // 2
                ))

    elements_to_process = [(game_surface, (  # добавляем в список элементов для обработки c координатами, вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
        (height - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
    ), False)]
    screen.blit(game_surface, (  # отрисовываем холст на экране в первый раз c координатами, вычисленными по принципцу (длина\ширина холста - длина\ширина экрана) / 2
        (width - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
        (height - (size_of_cell * 8 + length_of_divider_between_cells * 11 + coefficient * 2)) / 2,
    ))


def main_menu():
    global elements_to_process

    main_surface = pygame.Surface(screen.get_size())
    main_surface.blit(background.image, background.rect)
    button = Button(main_surface, 250, 290, 300, 100, "Начать игру", start_game, False)
    elements_to_process = [(main_surface, (0, 0), True, button)]
    screen.blit(main_surface, (0, 0))


if __name__ == "__main__":
    running = True
    # запуск вызываем функцию начала
    main_menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for surface_and_button in elements_to_process:
            screen.blit(surface_and_button[0], surface_and_button[1])
            if surface_and_button[2]:  # если есть, что процессить, то процессив (flag = surface_and_button[2])
                surface_and_button[3].process()
        pygame.display.flip()
    pygame.quit()

