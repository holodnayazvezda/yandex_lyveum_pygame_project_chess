WHITE = 1
BLACK = 0
size_of_cell = 55
coefficient = None  # 30% от ширины клетки
length_of_divider_between_cells = None  # 10% от ширины клетки


def recount_coefficent_and_length_of_divider(cell_sice_coef):
    global coefficient, length_of_divider_between_cells, size_of_cell
    size_of_cell = size_of_cell + cell_sice_coef
    if size_of_cell < 40:
        size_of_cell = 40
    if size_of_cell > 83:
        size_of_cell = 83
    coefficient = round(size_of_cell * 0.3)
    length_of_divider_between_cells = round(size_of_cell * 0.1)


# типывозможгых ходов
NORMAL_MOVE = 'normal'
TAKE_MOVE = 'take'
CONVERSION_MOVE = 'conversion'
PASSED_TAKE_MOVE = 'passed_take'
CASTLING_MOVE = 'castling'
OPPONENT_COLOR = {WHITE: BLACK, BLACK: WHITE}
ENGLISH_ALPHABED = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
RUSSIAN_ALPHABED = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
NUMBERS = '0123456789'


recount_coefficent_and_length_of_divider(0)
