def log(c):
    f = open("logs.txt", "a")
    f.write(c)
    f.close()

def get(row):
    pass

def all():
    f = open("demofile2.txt", "r")
    s = f.read()
    f.close()
    return s