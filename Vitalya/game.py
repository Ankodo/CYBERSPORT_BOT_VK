import random, os

def newGame(userId, hard):#hard - 3х значное число
        Id = str(random.randint(1, 9))
        file = open('Game/Maps/' + str(hard) + '.0' + Id + 'p.txt', 'r')
        spase = file.readlines()
        file.close()

        file = open('Game/' + str(userId) + 'p.txt', 'w')
        file.write(str(hard) + '0' + Id + str(random.randint(1, 9)).rjust(3,'0')+'0'+'999'+'000' + '\n')
        file.writelines(spase)
        file.close()

def haveSave(userId):
    try:
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        file.close()
        return True
    except:
        return False

def getWey(userId):
    file = open('Game/' + str(userId) + 'p.txt', 'r')
    gameInfo = file.read(3)
    oldL = file.read(3)
    file.close()

    file = open('Game/Maps/' + gameInfo[0]+ '.' + gameInfo[1:] + '.txt', 'r')
    map = file.readlines()
    file.close()

    c = int(oldL)
    r = 0
    b = map[c][r:r+3]
    while(b[0] != '\n'):
        r += 3
        b = map[c][r:r+3]
    r //= 3
    return r

def addPrint(userId, print):
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        mapId = file.read(3)
        gameInfo = file.read(11)
        if (gameInfo[4:7] != gameInfo[7:10]):
            gameInfo = gameInfo[:7] + str(int(gameInfo[7:10]) + 1).rjust(3,'0') + '\n'
            prints = file.readlines()
            weyId = int(gameInfo[:3])
            localSimbolsId = int(gameInfo[3]) * 3
            prints[weyId] = prints[weyId][:localSimbolsId] + print + prints[weyId][localSimbolsId+3:]
            file.close()
            file = open('Game/' + str(userId) + 'p.txt', 'w')
            file.write(mapId+gameInfo)
            file.writelines(prints)
            file.close()
            return True
        else:
            file.close()
            return False

def check(userId):
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        gameInfo = file.read(14)
        prints = file.readlines()
        file.close()
        c = int(gameInfo[3:6])
        d = int(gameInfo[6])
        out = []
        a =  0
        b = prints[c][a:a+3]
        while(b[0] != '\n'):
            out.append(b)
            a += 3
            b = prints[c][a:a+3]
        a //= 3
        out1 = []
        for i in range(0, a):
            out1.append(out[(d+i)%a])
        return out1

def move(userId, loc):#0 - назад, 1 налево, 2 - право, 3 - Вперед
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        gameInfo = file.read(3)
        oldL = file.read(4)
        dopInfo = file.read(7)
        prints = file.readlines()
        file.close()

        r = getWey(userId)
        if r == 2:
            if loc == 3:
                loc = 2
        elif r == 4:
            if loc == 2:
                loc = 3
            elif loc == 3:
                loc = 2


        file = open('Game/Maps/' + gameInfo[0]+ '.' + gameInfo[1:] + '.txt', 'r')
        map = file.readlines()
        file.close()

        r = (int(oldL[3]) + loc) % r * 3

        oldL = oldL[:3]

        c = int(oldL)
        newL = map[c][r:r+3]

        if newL == '000':
            os.remove('Game/' + str(userId) + 'p.txt')
            return True

        c = int(newL)
        r =  0
        b = map[c][r:r+3]
        while(b != oldL):
            r += 3
            b = map[c][r:r+3]
        r //= 3

        file = open('Game/' + str(userId) + 'p.txt', 'w')
        file.write(gameInfo + newL + str(r) + dopInfo)
        file.writelines(prints)
        file.close()
        return False