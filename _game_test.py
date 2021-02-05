from game import Game
from db import DataBase

db = DataBase("students.db")

game = Game(db)
id = '2281337'
game.gameManager(id, 'newgame', 'HELLO BITCH')

while True:
    inp = input('Введите ход > ')
    x = None
    if inp == 'move':
        x = input('Введите сторону > ')
    game.gameManager('2281337', inp, x)

    db.select("GameMaze", "p_coords", f"WHERE user_id='{id}'")
    res = db.cursor.fetchone()[0].split(';')
    p_coords = list(map(int, res))
    db.select("GameMaze", "m_coords", f"WHERE user_id='{id}'")
    res = db.cursor.fetchone()[0].split(';')
    m_coords = list(map(int, res))
    print(p_coords, m_coords)