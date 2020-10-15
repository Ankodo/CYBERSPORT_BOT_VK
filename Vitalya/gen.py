import random

for lvl in range(1, 10):
    weys = lvl * 10 + 10
    for i in range(1, 10):
        f = random.randint(3, 8)
        size = [1]
        f = 0
        for l in range(1, weys):
             size.append(random.randint(2, 4))
             f += size[l]
        if f % 2 == 0:
            f = 1
            while(size[f] >= 4):
                f += 1
            size[f] += 1
        data = [[1],[0]]
        for l in range(2, weys):
            data.append([])
        for l in range(1, weys):
            if (len(data[l]) < size[l]):
                a = random.randint(1, weys - 1)
                while(len(data[a]) >= size[a] or a == l):
                    a = random.randint(1, weys - 1)
                data[a].append(l)
                data[l].append(a)
        for m in range(1, 4):
            for l in range(1 , weys):
                if (len(data[l]) < size[l] - 1):
                    a = weys // 2
                    while(len(data[a]) >= size[a] or a == l):
                        a += 1
                        a %= weys
                    data[a].append(l)
                    data[l].append(a)
        for m in range(1, 4):
            for l in range(1 , weys):
                if (len(data[l]) < size[l]):
                    a = 1
                    while(len(data[a]) >= size[a] or a == l):
                        a += 1
                        a %= weys
                    data[a].append(l)
                    data[l].append(a)
        fp = open('Game/Maps/' + str(lvl) + '.0' + str(i) + 'p.txt', 'w')
        f = open('Game/Maps/' + str(lvl) + '.0' + str(i) + '.txt', 'w')
        for wey in data:
            for a in wey:
                f.write(str(a).rjust(3,'0'))
                fp.write('   ')
            f.write('\n')
            fp.write('\n')
