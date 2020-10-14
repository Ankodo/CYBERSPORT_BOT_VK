import random, os

def newGame(userId, hard):#hard - 3х значное число
        file = open('Game/' + str(userId) + 'p.txt', 'w')
        #file.write(str(hard).rjust(3,'0')+'0'+str(hard/2).rjust(3,'0')+'000' + '   ' * hard)
        file.write(str(hard-1).rjust(3,'0')+'0'+'999'+'000' + '         ' * hard)
        file.close()
        file = open('Game/' + str(userId) + '.txt', 'w')
        h = 0
        a1 = random.randint(2, hard // 4) * 2 - 1
        b = hard // 2
        a2 = hard - a1
        while h < hard:
            file.write(str((h + a1)%hard).rjust(3,'0')+ str((h + b)%hard).rjust(3,'0') + str((h + a2)%hard).rjust(3,'0'))
            h += 1
        file.close()



def getLine(userId, line):
        file = open('Game/' + str(userId) + '.txt', 'r')
        file.seek(line*9)
        out = [file.read(3), file.read(3), file.read(3)]
        file.close()
        return out

def addPrint(userId, print):
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        a = file.read(10)
        if (a[4:7] != a[7:10]):
            a = a[:7] + str(int(a[7:10]) + 1).rjust(3,'0')
            b = file.read()
            c = int(a[:3]) * 9 + int(a[3]) * 3
            b= b[:c] + print + b[c+3:]
            file.close()
            file = open('Game/' + str(userId) + 'p.txt', 'w')
            file.write(a+b)
            file.close()
            return True
        else:
            file.close()
            return False


def check(userId):
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        a = file.read(10)
        b = file.read()
        c = int(a[:3]) * 9
        d = int(a[3])
        out = [ b[c:c+3], b[c+3:c+6], b[c+6:c+9] ]
        out = [out[d], out[(d+1)%3], out[(d+2)%3]]
        file.close()
        return out

def move(userId, loc):#0 - назад, 1 налево, 2 - право
        file = open('Game/' + str(userId) + 'p.txt', 'r')
        oldL = file.read(4)
        b = file.read()
        r = (int(oldL[3]) + loc) % 3
        oldL = oldL[:3]
        newL = getLine(userId, int(oldL))[r]
        if newL == '000':
            file.close()
            os.remove('Game/' + str(userId) + 'p.txt')
            os.remove('Game/' + str(userId) + '.txt')
            return True
        r = getLine(userId, int(newL)).index(oldL)
        file.close()
        file = open('Game/' + str(userId) + 'p.txt', 'w')
        file.write(newL+str(r)+b)
        file.close()
        return False