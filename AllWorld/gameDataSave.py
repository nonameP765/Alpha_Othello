import game as othello
import json
import copy


def create_dump():
    tmp = list()

    tmp.append([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0], ])
    return copy.deepcopy(tmp)


def y_categorical(p0):
    tmp = list()
    for i in range(8):
        btmp = list()
        for j in range(8):
            if p0 == [j, i]:
                btmp.append(1)
            else:
                btmp.append(0)
        tmp.append(btmp)

    rtmp = list()
    for i in range(8):
        for j in range(8):
            rtmp.append(tmp[i][j])

    return rtmp


def ap(x_save, y_save, x_input, y_input):
    tmp = list()
    for i in range(2):
        tmp.append([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0], ])
    for i in range(8):
        for j in range(8):
            if x_input[0][i][j] == 1:
                tmp[0][i][j] = 1
            elif x_input[0][i][j] == -1:
                tmp[1][i][j] = 1
    try:
        z = x_save.index(tmp)
        found1 = 0
        for i in range(1, len(y_input)):
            if y_input[i] == 1:
                found1 = i
                break
        y_save[z][found1] += 1

    except Exception as e:
        x_save.append(tmp)
        y_save.append(y_input)


def apValue(x_save, y_save, x_input, y_input, winner):
    tmp = list()
    for i in range(3):
        tmp.append([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0], ])
    for i in range(8):
        for j in range(8):
            if x_input[0][i][j] == 1:
                tmp[0][i][j] = 1
            elif x_input[0][i][j] == -1:
                tmp[1][i][j] = 1
    tmp[2][y_input[1]][y_input[0]] = 1

    try:
        z = x_save.index(tmp)
        if winner == x_input[1]:
            y_save[z][0] += 1
            y_save[z][1] += 0
        elif winner == -1 * x_input[1]:
            y_save[z][0] += 0
            y_save[z][1] += 1
        else:
            y_save[z][0] += 1
            y_save[z][1] += 1


    except Exception as e:
        x_save.append(tmp)
        if winner == x_input[1]:
            y_save.append([1, 0])
        elif winner == -1 * x_input[1]:
            y_save.append([0, 1])
        else:
            y_save.append([1, 1])


def mainplay(p0):
    with open(p0 + '.json') as f:
        data = json.load(f)
    data = list(data)
    print(data)
    x_save = list()
    y_save = list()

    for i in data:
        print(i)
        x, y = othello.createData(i)
        for j in range(len(x)):
            x1 = create_dump()
            for a in range(8):
                for b in range(8):
                    x1[0][a][b] = x[j][0][b][7 - a]
            y1 = [y[j][1], 7 - y[j][0]]

            x2 = create_dump()
            for a in range(8):
                for b in range(8):
                    x2[0][a][b] = x[j][0][7 - a][7 - b]
            y2 = [7 - y[j][0], 7 - y[j][1]]

            x3 = create_dump()
            for a in range(8):
                for b in range(8):
                    x3[0][a][b] = x[j][0][7 - b][a]
            y3 = [7 - y[j][1], y[j][0]]

            x4 = create_dump()
            for a in range(8):
                for b in range(8):
                    x4[0][a][b] = x[j][0][7 - a][b]
            y4 = [y[j][0], 7 - y[j][1]]

            x5 = create_dump()
            for a in range(8):
                for b in range(8):
                    x5[0][a][b] = x[j][0][b][a]
            y5 = [y[j][1], y[j][0]]

            x6 = create_dump()
            for a in range(8):
                for b in range(8):
                    x6[0][a][b] = x[j][0][a][7 - b]
            y6 = [7 - y[j][0], y[j][1]]
            x7 = create_dump()
            for a in range(8):
                for b in range(8):
                    x7[0][a][b] = x[j][0][a][7 - b]
            y7 = [7 - y[j][0], y[j][1]]

            ap(x_save, y_save, x[j], y_categorical(y[j]))
            ap(x_save, y_save, x1, y_categorical(y1))
            ap(x_save, y_save, x2, y_categorical(y2))
            ap(x_save, y_save, x3, y_categorical(y3))
            ap(x_save, y_save, x4, y_categorical(y4))
            ap(x_save, y_save, x5, y_categorical(y5))
            ap(x_save, y_save, x6, y_categorical(y6))
            ap(x_save, y_save, x7, y_categorical(y7))

    for i in range(0, len(y_save)):
        maxy = max(y_save[i])
        for j in range(0, len(y_save[i])):
            y_save[i][j] = y_save[i][j] / maxy

    print(len(x_save))
    print(len(x_save[0]))
    print(len(x_save[0][0]))
    print(len(x_save[0][0][0]))
    print(len(y_save))
    print(y_save[0])
    for i in x_save[0]:
        tmp = ""
        for j in i:
            tmp += str(j)
        print(tmp)
    print()
    print(y_save[0][46])
    for i in range(8):
        t = ""
        for j in range(8):
            t += str(y_save[0][i * 8 + j]) + " "
        print(t)

    othello.printBoard(x_save[8][0], othello.canMove(x_save[8][0], 1))

    for z in range(10, 20):
        print("x", z)
        for i in x_save[z]:
            for c in i:
                tmp = ""
                for j in c:
                    tmp += str(j) + " "
                print(tmp)
        print("y", z)
        for i in range(8):
            t = ""
            for j in range(8):
                t += str(y_save[z][i * 8 + j]) + " "
            print(t)

    import numpy as np

    print(np.shape(x_save))
    with open(p0 + '_x.json', 'w') as outfile:
        json.dump(x_save, outfile)
    with open(p0 + '_y.json', 'w') as outfile:
        json.dump(y_save, outfile)


def mainValue(p0):
    with open(p0 + '.json') as f:
        data = json.load(f)
    data = list(data)
    print(data)
    x_save = list()
    y_save = list()

    for i in data:
        print(i)
        winner = othello.winnerIs(i)
        x, y = othello.createData(i)
        for j in range(len(x)):
            x1 = create_dump()
            for a in range(8):
                for b in range(8):
                    x1[0][a][b] = x[j][0][b][7 - a]
            x1.append(x[j][1])
            y1 = [y[j][1], 7 - y[j][0]]

            x2 = create_dump()
            for a in range(8):
                for b in range(8):
                    x2[0][a][b] = x[j][0][7 - a][7 - b]
            x2.append(x[j][1])
            y2 = [7 - y[j][0], 7 - y[j][1]]

            x3 = create_dump()
            for a in range(8):
                for b in range(8):
                    x3[0][a][b] = x[j][0][7 - b][a]
            x3.append(x[j][1])
            y3 = [7 - y[j][1], y[j][0]]

            x4 = create_dump()
            for a in range(8):
                for b in range(8):
                    x4[0][a][b] = x[j][0][7 - a][b]
            x4.append(x[j][1])
            y4 = [y[j][0], 7 - y[j][1]]

            x5 = create_dump()
            for a in range(8):
                for b in range(8):
                    x5[0][a][b] = x[j][0][b][a]
            x5.append(x[j][1])
            y5 = [y[j][1], y[j][0]]

            x6 = create_dump()
            for a in range(8):
                for b in range(8):
                    x6[0][a][b] = x[j][0][a][7 - b]
            x6.append(x[j][1])
            y6 = [7 - y[j][0], y[j][1]]

            x7 = create_dump()
            for a in range(8):
                for b in range(8):
                    x7[0][a][b] = x[j][0][a][7 - b]
            x7.append(x[j][1])
            y7 = [7 - y[j][0], y[j][1]]

            apValue(x_save, y_save, x[j], y[j], winner)
            apValue(x_save, y_save, x1, y1, winner)
            apValue(x_save, y_save, x2, y2, winner)
            apValue(x_save, y_save, x3, y3, winner)
            apValue(x_save, y_save, x4, y4, winner)
            apValue(x_save, y_save, x5, y5, winner)
            apValue(x_save, y_save, x6, y6, winner)
            apValue(x_save, y_save, x7, y7, winner)

    for i in range(0, len(y_save)):

        y_save[i] = [y_save[i][0] / (y_save[i][0] + y_save[i][1]), y_save[i][1] / (y_save[i][0] + y_save[i][1])]
    print(len(x_save))
    print(len(x_save[0]))
    print(len(x_save[0][0]))
    print(len(x_save[0][0][0]))
    print(len(y_save))
    print(y_save[0])
    for i in x_save[0]:
        tmp = ""
        for j in i:
            tmp += str(j)
        print(tmp)
    print()

    othello.printBoard(x_save[8][0], othello.canMove(x_save[8][0], 1))

    for z in range(0, 20):
        print("x", z)
        for i in x_save[z]:
            for c in i:
                tmp = ""
                for j in c:
                    tmp += str(j) + " "
                print(tmp)
        print("y", z)
        print(y_save[z])

    import numpy as np

    print(np.shape(x_save))
    with open(p0 + '_ValueX.json', 'w') as outfile:
        json.dump(x_save, outfile)
    with open(p0 + '_ValueY.json', 'w') as outfile:
        json.dump(y_save, outfile)


if __name__ == '__main__':
    mainplay('gameData')
