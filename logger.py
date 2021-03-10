def log(c):
    f = open("botlogs.txt", "a")
    f.write(c)
    f.close()

def get(row):
    pass

def all():
    f = open("botlogs.txt", "a")
    f.close()
    f = open("botlogs.txt", "r")
    s = f.read()
    f.close()
    return s