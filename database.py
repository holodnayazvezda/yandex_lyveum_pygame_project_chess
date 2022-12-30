import sqlite3


def write_result_of_the_game(white_player_name, black_player_name, result):  # запись результата игры в базу данных
    # описание передаваемых параметров: Имя игрока за белых, имя игрока за черных, результат игры (ВАЖНО! 1 - победа
    # белых, 0 - ничья, -1 - победа черных) Описание структуры базы данных: две таблицы (в первой - id партии и
    # результат, во второй - имена игроков). ВАЖНО! Инкрементный ключ, связывающий две таблицы - id партии (Идет по
    # порядку. Перед записью нового значения в бд необходимо вычеслить новый id).
    con = sqlite3.connect('gameresults.sqlite3')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, result INTEGER)")
    try:
        id = cur.execute('SELECT MAX(id) FROM results').fetchone()[0] + 1
    except TypeError:
        id = 1
    cur.execute('INSERT INTO results VALUES (?, ?)', (id, result))
    cur.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, white_player_name TEXT, '
                'black_player_name TEXT)')
    cur.execute('INSERT INTO players VALUES (?, ?, ?)', (id, white_player_name, black_player_name))
    con.commit()
    con.close()


if __name__ == '__main__':
    for i in range(100):
        write_result_of_the_game('Ivan', 'Petr', 1)
        #write_result_of_the_game('Huy', 'Blacka', 1)
