import random
import os


class LabGen:
    def coordinate_changer(self, direction):
        dirmanager ={
            'N':(0, -1),
            'S':(0, 1),
            'E':(1, 0),
            'W':(-1, 0)
        }
        
        return dirmanager[direction]

    def generate(self, max_size, seed, id):
        self.Opposite = {
            'E':'W',
            'W':'E',
            'N':'S',
            'S':'N' 
        }

        self.Bitwise = {
            'N':1,
            'S':2,
            'E':4,
            'W':8,
        
        }
        self.max_x = max_size
        self.max_y = max_size

        Grid = []

        for i in range(self.max_y):
            Grid.append([0 for x in range(self.max_x)])

        random.seed(seed)

        self.worker_passage(0, 0, Grid)
        self.save_to_text(Grid, id)

    def worker_passage(self, x, y, Grid):
        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)
        #print(directions)

        for direction in directions:
            n_x, n_y = self.coordinate_changer(direction)
            n_x, n_y = x+n_x, y+n_y
            if n_x < self.max_x and n_x >= 0 and n_y < self.max_y and n_y >= 0 and Grid[n_y][n_x] == 0:
                var = Grid[y][x]
                var |= self.Bitwise[direction]
                Grid[y][x] = var
                Grid[n_y][n_x] = Grid[n_y][n_x] | self.Bitwise[self.Opposite[direction]] 
                self.worker_passage(n_x, n_y, Grid)

    def save_to_text(self, Grid, id):
        file = open(f"{id}.txt","w+")

        file.write("_" * (self.max_x * 2 - 1))

        for i in range(self.max_y):
            file.write('\n|')
            for j in range(self.max_x):
                file.write(" " if (Grid[i][j] & self.Bitwise['S'] != 0) else "_")
                if Grid[i][j] & self.Bitwise["E"] != 0:
                    file.write(" " if (((Grid[i][j] | Grid[i][j+1]) & self.Bitwise['S']) != 0) else "_")
                else:
                    file.write("|")

        file.close()


class Game:
    def __init__(self, bot, db):
        '''Игра'''
        self.db = db
        self.bot = bot
        self.generator = LabGen()

    def newGame(self, id, seed):
        '''Новая игра'''
        self.db.delete("GameMaze", f"user_id='{id}'")
        self.db.insert("GameMaze", "user_id, p_coords, m_coords", f"'{id}', '1;1', '5;9'")
        self.generator.generate(5, seed, id)
        self.db.connection.commit()
        self.showMazePart(id, [0, 0])
        self.bot.writeMsg(id, """
Добро пожаловать в лабиринт. Тут очень темно и ничего не видно. Поэтому 
придется передвигаться вслепую. Также тут где-то рядом бегает монстр, который за
один ход делает два шага. Естественно, с ним лучше не пересекаться. Удачи!
        """)

    def gameOver(self, id):
        self.db.delete("GameMaze", f"user_id='{id}'")
        self.db.connection.commit()
        os.remove(f"{id}.txt")
        self.bot.sendKeyboard(id, "main_game_start", "Монстр настигнул Вас. Вы проиграли.", True)

    def monster_action(self, id, second_move=False):
        """Ход монстра и проверка коллизии с игроком"""
        def check_player_nearby(id, m_res):
            """Проверяем, не находится ли игрок рядом"""
            self.db.select("GameMaze", "p_coords", f"WHERE user_id='{id}'")
            p_res = self.db.cursor.fetchone()[0].split(';')
            p_res = list(map(int, p_res))

            if p_res[0] == m_res[0] and p_res[1] == m_res[1]:
                return True

        maze = self.getMaze(id)
        self.db.select("GameMaze", "m_coords", f"WHERE user_id='{id}'")
        res = self.db.cursor.fetchone()[0].split(';')
        res = list(map(int, res))
        gameover = False

        free_space = []

        if check_player_nearby(id, res):
            gameover = True

        if not gameover:
            if res[1] > 0:
                if maze[res[0]][res[1]-1] != '|':
                    free_space.append('left')
                    if check_player_nearby(id, [res[0], res[1]-1]):
                        gameover = True
            if res[1] < len(maze[0])-1:
                if maze[res[0]][res[1]+1] != '|':
                    free_space.append('rigth')
                    if check_player_nearby(id, [res[0], res[1]+1]):
                        gameover = True
            if res[0] > 0:
                if maze[res[0]-1][res[1]] != '_':
                    free_space.append('up')
                    if check_player_nearby(id, [res[0]-1, res[1]]):
                        gameover = True
            if res[0] < len(maze)-1:
                if maze[res[0]][res[1]] != '_':
                    free_space.append('down')
                    if check_player_nearby(id, [res[0]+1, res[1]]):
                        gameover = True

            random.shuffle(free_space)
            direction = free_space[0]

            if direction == 'left':
                res[1]-=1
            if direction == 'right':
                res[1]+=1
            if direction == 'up':
                res[0]-=1
            if direction == 'down':
                res[0]+=1

        if not gameover:
            self.applyCoords(id, 'm_coords', res)
            if not second_move:
                self.monster_action(id, True)
        else:
            self.gameOver(id)

    def stay(self, id, _):
        """Игрок остается на месте"""
        def end_turn(id, res):
            self.applyCoords(id, 'p_coords', res)
            self.monster_action(id)

        maze = self.getMaze(id)
        self.db.select("GameMaze", "p_coords", f"WHERE user_id='{id}'")
        res = self.db.cursor.fetchone()[0].split(';')
        res = list(map(int, res))

        self.db.select("GameMaze", "m_coords", f"WHERE user_id='{id}'")
        m_res = self.db.cursor.fetchone()[0].split(';')
        m_res = list(map(int, m_res))

        monster_position = None
        
        self.bot.writeMsg(id, """
Вы остаетесь на месте, чтобы получше разглядеть путь.
        """)

        if res[1]-1 > 0:
            if m_res[0] == res[0] and (m_res[1] == res[1]-2 or m_res[1] == res[1]-1):
                monster_position = 'слева'
        if res[1] < len(maze[0])-2:
            if m_res[0] == res[0] and (m_res[1] == res[1]+2 or m_res[1] == res[1]+1):
                monster_position = 'справа'
        if res[0]-1 > 0:
            if m_res[1] == res[1] and (m_res[0] == res[0]-2 or m_res[0] == res[0]-1):
                monster_position = 'сверху'
        if res[0] < len(maze)-2:
            if m_res[1] == res[1] and (m_res[0] == res[0]+2 or m_res[0] == res[0]+1):
                monster_position = 'снизу'

        if monster_position != None:
            self.bot.writeMsg(id, f"""
Вы слышите монстра! Похоже, он где-то {monster_position}
        """)

        self.showMazePart(id, res)
        end_turn(id, res)

    def move(self, id, direction):
        """Ход игрока"""
        def end_turn(id, res):
            self.applyCoords(id, 'p_coords', res)
            self.monster_action(id)

        maze = self.getMaze(id)
        self.db.select("GameMaze", "p_coords", f"WHERE user_id='{id}'")
        res = self.db.cursor.fetchone()[0].split(';')
        res = list(map(int, res))

        if direction == 'left':
            if res[1] > 0:
                if maze[res[0]][res[1]-1] != '|':
                    self.bot.writeMsg(id, """
Вы пошли налево
        """)
                    res[1]-=1
                else:
                    self.bot.writeMsg(id, """
Вы пошли налево и уперлись в стену.
        """)
        elif direction == 'right':
            if res[1] < len(maze[0])-1:
                if maze[res[0]][res[1]+1] != '|':
                    self.bot.writeMsg(id, """
Вы пошли направо
        """)
                    res[1] += 1
                else:
                    self.bot.writeMsg(id, """
Вы пошли направо и уперлись в стену.
        """)
        elif direction == 'up':
            if res[0] > 0:
                if maze[res[0]-1][res[1]] != '_' and maze[res[0]-1][res[1]] != '|':
                    self.bot.writeMsg(id, """
Вы пошли наверх
        """)
                    res[0] -= 1
                else:
                    self.bot.writeMsg(id, """
Вы пошли вверх и уперлись в стену.
        """)
        elif direction == 'down':
            if res[0] < len(maze)-1:
                if maze[res[0]][res[1]] != '_' and maze[res[0]][res[1]] != '|':
                    self.bot.writeMsg(id, """
Вы пошли вниз
        """)
                    res[0] += 1
                else:
                    self.bot.writeMsg(id, """
Вы пошли вниз и уперлись в стену.
        """)
        end_turn(id, res)

    def showMazePart(self, id, p_coords, m_coords=None):
        maze = self.getMaze(id)
        text = []

        for i in range(6):
            text.append([])
            for j in range(6):
                text[i].append(" ")
            text[i].append("\n") 

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_y = p_coords[0]+i
                new_x = p_coords[1]+j
                if new_y == p_coords[0] and new_x == p_coords[1]:
                    if maze[new_y][new_x] == "_":
                        text[i+1][j+1] = "p"
                        text[i+2][j+1] = "#"
                    else:
                        text[i+1][j+1] = "p"
                elif  new_y >= 0 and new_y < len(maze) and new_x >= 0 and new_x < len(maze[0]):
                    if maze[new_y][new_x] == "_":
                        text[i+1][j+1] = "-"
                        text[i+2][j+1] = "#"
                    elif maze[new_y][new_x] == "|":
                        text[i+1][j+1] = "#"
                        text[i+2][j+1] = "#"
                    elif maze[new_y][new_x] == " ":
                        text[i+1][j+1] = "-"
                        text[i+2][j+1] = "-"
                else:
                    text[i+1][j+1] = "#"
        
        result = ""
        for item in text:
            result += "".join(item)
        self.bot.writeMsg(id, result)

    def applyCoords(self, id, who, coords):
        """Залить новые координаты в БД"""
        self.db.update("GameMaze", who, f"'{coords[0]};{coords[1]}'", f"WHERE user_id = '{id}'")
        self.db.connection.commit()

    def getMaze(self, id):
        """Загрузить лабиринт из файла"""
        maze = []
        with open(f'{id}.txt') as f:
            maze = f.readlines()
            maze = [x.strip() for x in maze] 

        return maze

    def gameManager(self, id, command, add_ard=None):
        """Управление игрой. Вызывается через клавиатуру"""
        commands = {
            'stay': self.stay,
            'move': self.move,
            'newgame': self.newGame
        }

        commands[command](id, add_ard)