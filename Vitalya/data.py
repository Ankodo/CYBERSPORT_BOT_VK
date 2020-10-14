#�������
#0 - � ����� ����
#1 - ������ ������
#2 - ������ ���
#G0 - игра меню
#G1 - игра выбор сложности
#G2 - В игре
#G3 - отметка
def getUserStatus(userId):
    try:
        file = open('UsersInfo/' + str(userId) + '.txt', 'r')
        out = str(file.readline()).replace('\n', '')
        file.close()
        return out
    except:
        return '-1'

def addUser(userId):
    file = open('UsersInfo/' + str(userId) + '.txt', 'w')
    file.write('0\n0\n0\n0')
    file.close

def getUserSTUD(userId):
    file = open('UsersInfo/' + str(userId) + '.txt', 'r')
    out = str(file.readlines()[1]).replace('\n', '')
    file.close()
    return out

def getUserFIO(userId):
    file = open('UsersInfo/' + str(userId) + '.txt', 'r')
    out = str(file.readlines()[2]).replace('\n', '')
    file.close()
    return out

def getUserSUBS(userId):
    file = open('UsersInfo/' + str(userId) + '.txt', 'r')
    out = str(file.readlines()[3]).replace('\n', '')
    file.close()
    return out

def setUserInfo(userId, status, STUD, FIO, SUBS):
    file = open('UsersInfo/' + str(userId) + '.txt', 'w')
    file.write(status+'\n')
    file.write(STUD+'\n')
    file.write(FIO+'\n')
    file.write(SUBS+'\n')
    file.close

def setUserSTUD(userId, STUD):
    setUserInfo(userId, '0', STUD, getUserFIO(userId), getUserSUBS(userId))

def setUserFIO(userId, FIO):
    setUserInfo(userId, '0', getUserSTUD(userId), FIO, getUserSUBS(userId))

def setUserStatus(userId, status):
    setUserInfo(userId, status, getUserSTUD(userId), getUserFIO(userId), getUserSUBS(userId))

def setUserSUBS(userId, SUBS):
    setUserInfo(userId, '0', getUserSTUD(userId), getUserFIO(userId), SUBS)