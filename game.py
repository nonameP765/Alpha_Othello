# 오셀로 인게임 구현
import copy


def winnerIs(input_str):
    _board_, _count = gameInit()

    _now_player = 1
    _gibos = []
    for i in range(len(input_str)):
        if i % 2 == 0:
            _gibos.append(giboParse(input_str[i: i + 2]))

    while True:
        can_do = False
        for j in canMove(_board_, _now_player):
            if j == _gibos[_count]:
                can_do = True
        if can_do:
            move(_gibos[_count], _board_, _now_player)
            _count += 1

        _now_player = -1 * _now_player

        if _count >= len(_gibos):
            break

    num1c = 0
    num2c = 0

    for i in _board_:
        for j in i:
            if j == 1:
                num1c += 1
            if j == -1:
                num2c += 1
    if num1c > num2c:
        return 1
    elif num2c > num1c:
        return -1
    elif num2c == num1c:
        return 0


def currentBoard(winner, boardTmp, _count):
    tmp = list()
    boardTmp = copy.deepcopy(boardTmp)

    a_ = list()
    for b in range(8):
        b_ = list()
        for c in range(8):
            b_.append(0)
        a_.append(b_)
    tmp.append(a_)

    if winner == -1:
        for i in range(len(boardTmp)):
            for j in range(len(boardTmp[i])):
                boardTmp[i][j] = -1 * boardTmp[i][j]

    for i in range(len(boardTmp)):
        for j in range(len(boardTmp[i])):
            tmp[0][i][j] = boardTmp[i][j]

    return tmp


def createData(input_str):
    rtnTmp = list()
    rtn2Tmp = list()
    _board_, _count = gameInit()
    _board_ = copy.deepcopy(_board_)
    _count = copy.deepcopy(_count)

    _now_player = 1
    _gibos = list()
    for i in range(len(input_str)):
        if i % 2 == 0:
            _gibos.append(giboParse(input_str[i: i + 2]))
    while True:
        can_do = False
        for j in canMove(_board_, _now_player):
            if j == _gibos[_count]:
                can_do = True
        if can_do:
            boardTmp = copy.deepcopy(_board_)

            move(_gibos[_count], _board_, _now_player)
            _count += 1
            brtnTmp = currentBoard(_now_player, boardTmp, _count)
            brtnTmp.append(_now_player)
            rtnTmp.append(brtnTmp)
            rtn2Tmp.append(_gibos[_count - 1])

        _now_player = -1 * _now_player
        if _count >= len(_gibos):
            break
    return rtnTmp, rtn2Tmp


def createValueData(input_str):
    rtnTmp = list()
    rtn2Tmp = list()
    _board_, _count = gameInit()
    _board_ = copy.deepcopy(_board_)
    _count = copy.deepcopy(_count)
    winner = winnerIs(input_str)
    _now_player = 1
    _gibos = list()
    for i in range(len(input_str)):
        if i % 2 == 0:
            _gibos.append(giboParse(input_str[i: i + 2]))
    while True:
        can_do = False
        for j in canMove(_board_, _now_player):
            if j == _gibos[_count]:
                can_do = True
        if can_do:
            boardTmp = copy.deepcopy(_board_)

            move(_gibos[_count], _board_, _now_player)
            _count += 1
            brtnTmp = list()
            brtnTmp.append(currentBoard(_now_player, boardTmp, _count))
            brtnTmp.append(_gibos[_count - 1])
            rtnTmp.append(brtnTmp)
            if winner == _now_player:
                rtn2Tmp.append([1, 0])
            elif winner == -1 * _now_player:
                rtn2Tmp.append([0, 1])
            elif winner == 0:
                rtn2Tmp.append([1, 1])

        _now_player = -1 * _now_player
        if _count >= len(_gibos):
            break
    return rtnTmp, rtn2Tmp


def gameInit():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0], ], 0


def giboParse(str_):
    if str_[0] == 'a':
        return [0, int(str_[1]) - 1]
    if str_[0] == 'b':
        return [1, int(str_[1]) - 1]
    if str_[0] == 'c':
        return [2, int(str_[1]) - 1]
    if str_[0] == 'd':
        return [3, int(str_[1]) - 1]
    if str_[0] == 'e':
        return [4, int(str_[1]) - 1]
    if str_[0] == 'f':
        return [5, int(str_[1]) - 1]
    if str_[0] == 'g':
        return [6, int(str_[1]) - 1]
    if str_[0] == 'h':
        return [7, int(str_[1]) - 1]


def searchColor(color, board):
    tmp = []
    for i in range(8):
        for j in range(8):
            if board[j][i] == color:
                tmp.append([i, j])
    return tmp


def canMove(board, color):
    tmp = []
    myPiece = searchColor(color, board)
    check = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    for i in myPiece:
        for j in check:
            if 8 > i[1] + j[1] >= 0 and 8 > i[0] + j[0] >= 0:
                if board[i[1] + j[1]][i[0] + j[0]] == -1 * color:
                    for k in range(2, 9):
                        if 8 > i[1] + j[1] * k >= 0 and 8 > i[0] + j[0] * k >= 0:
                            if board[i[1] + j[1] * k][i[0] + j[0] * k] == -1 * color:
                                continue
                            elif board[i[1] + j[1] * k][i[0] + j[0] * k] == 0:
                                try:
                                    tmp.index([i[0] + j[0] * k, i[1] + j[1] * k])
                                except:
                                    tmp.append([i[0] + j[0] * k, i[1] + j[1] * k])
                                break
                            else:
                                break
                        else:
                            break
    return tmp


def move(position, board, color):
    cnt = 0
    myPiece = position
    board[myPiece[1]][myPiece[0]] = color
    check = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    tmp2 = []
    for j in check:
        if myPiece[1] + j[1] >= 0 and myPiece[0] + j[0] >= 0 and myPiece[1] + j[1] < 8 and myPiece[0] + j[0] < 8:
            if board[myPiece[1] + j[1]][myPiece[0] + j[0]] == -1 * color:
                for k in range(2, 9):
                    if myPiece[1] + j[1] * k >= 0 and myPiece[0] + j[0] * k >= 0 and myPiece[1] + j[1] * k < 8 and \
                            myPiece[0] + j[0] * k < 8:
                        if board[myPiece[1] + j[1] * k][myPiece[0] + j[0] * k] == -1 * color:
                            continue
                        elif board[myPiece[1] + j[1] * k][myPiece[0] + j[0] * k] == color:
                            cnt += 1
                            tmp2.append([j, k])
                            break
                        else:
                            break
                    else:
                        break
    for i in tmp2:
        for j in range(i[1]):
            board[myPiece[1] + i[0][1] * j][myPiece[0] + i[0][0] * j] = color

    return cnt


def printBoard(board, can=None):
    if can is None:
        can = list()
    tmp = copy.deepcopy(board)
    for i in can:
        tmp[i[1]][i[0]] = 3
    print("  ", ' a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ')
    print(" ", '┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓')
    for j in range(len(tmp)):
        tmp1 = "┃"
        for i in tmp[j]:
            if i == 0:
                tmp1 += "   ┃"
            if i == 1:
                tmp1 += " ○ ┃"
            if i == -1:
                tmp1 += " ● ┃"
            if i == 3:
                tmp1 += " X ┃"
        print(str(j + 1), tmp1)
        if j == len(tmp) - 1:
            print(" ", "┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛")
        else:
            print(" ", "┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫")


def intScan(p0):
    try:
        a = int(input(p0))
        return a
    except:
        print("잘못입력하셨습니다.")
        return intScan(p0)


if __name__ == "__main__":
    board_, count = gameInit()

    now_player = 1
    str_in = input("입력")
    gibos = []
    for i in range(len(str_in)):
        if i % 2 == 0:
            gibos.append(giboParse(str_in[i: i + 2]))

    print(gibos)
    print(len(gibos))
    while True:
        printBoard(board_, canMove(board_, now_player))
        canDo = False
        for j in canMove(board_, now_player):
            if j == gibos[count]:
                canDo = True
        if canDo:
            move(gibos[count], board_, now_player)
            count += 1
            print(count, "턴, 플레이어 :", now_player, "착수")
        else:
            print("플레이어 :", now_player, "턴 넘김")
        now_player = -1 * now_player
        if count >= len(gibos):
            break

    printBoard(board_, canMove(board_, now_player))
