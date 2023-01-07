import sqlite3
from random import randint


def write_result_of_the_game(white_player_name, black_player_name, result, player_dict):  # запись результата игры в 
    # базу данных 
    # Описание передаваемых параметров: Имя игрока за белых, имя игрока за черных, результат игры (ВАЖНО! 1 - победа
    # белых, 0 - ничья, -1 - победа черных) Описание структуры базы данных: две таблицы (в первой - id партии и
    # результат, во второй - имена игроков). ВАЖНО! Инкрементный ключ, связывающий две таблицы - id партии (Идет по
    # порядку. Перед записью нового значения в бд необходимо вычеслить новый id).
    # Определяем result (str)
    if result == 1:
        result = 'Победил(а) ' + player_dict[1]  # Переводим result в str (game.player_dict[1] - имя игрока за
        # белых)
    elif result == 0:
        result = 'Ничья'
    else:  # result == -1
        result = 'Победил(а) ' + player_dict[0]  # Переводим result в str (game.player_dict[0] - имя игрока за
        # черных)
    con = sqlite3.connect('gameresults.sqlite3')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, result TEXT)")
    try:
        id_of_the_game = cur.execute('SELECT MAX(id) FROM results').fetchone()[0] + 1
    except TypeError:
        id_of_the_game = 1
    cur.execute('INSERT INTO results VALUES (?, ?)', (id_of_the_game, result))
    cur.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, white_player_name TEXT, '
                'black_player_name TEXT)')
    cur.execute('INSERT INTO players VALUES (?, ?, ?)', (id_of_the_game, white_player_name, black_player_name))
    con.commit()
    con.close()


def read_results_of_the_game():  # чтение результата игры из базы данных
    try:
        con = sqlite3.connect('gameresults.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT * FROM results')
        results = cur.fetchall()
        cur.execute('SELECT * FROM players')
        players = cur.fetchall()
        con.close()
        dict_to_return = {}
        for results in zip(results, players):
            dict_to_return[results[0][0]] = (results[1][1], results[1][2], results[0][1])
    except Exception:
        dict_to_return = {}
    return dict_to_return


if __name__ == '__main__':
    for i in range(200):
        write_result_of_the_game('Даниил', 'Илон', randint(-1, 1), {1: 'Даниил', 0: 'Илон'})
    print(read_results_of_the_game())
