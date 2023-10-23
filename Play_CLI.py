import game as othello
import copy as c
import os

import numpy as np
from keras.models import load_model

modelPath = "AllWorld/savingModel.h5"
if os.path.isfile(modelPath):
    model = load_model(modelPath)


def searchDown(nowBoard, color, mycolor, cnt):
    tmp = list()
    tmp1 = list()
    for i in range(2):
        tmp1.append([
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
            if nowBoard[i][j] == 1:
                tmp1[0][i][j] = 1
            elif nowBoard[i][j] == -1:
                tmp1[1][i][j] = 1
    aiResult = model.predict(np.array([tmp1]))
    canMove = othello.isEnableToMove(nowBoard, color)
    if len(canMove) == 0:
        Wi = 0
        Ni = 0
        downBoard = c.deepcopy(nowBoard)
        downWN, _ = searchDown(downBoard, -1 * color, mycolor, cnt + 1)
        for j in downWN:
            Wi += j[0]
            Ni += j[1]
        tmp.append([Wi, Ni])
        return tmp, []
    else:
        canMovA = list()
        for a in canMove:
            canMovA.append(aiResult[0][a[0] + a[1] * 8])
        canMovF = list()

        for i in range(len(canMovA)):
            if 0.71 > abs(1 - canMovA[i]):
                canMovF.append(canMove[i])

        if len(canMovF) == 0:
            rsD = 3
            for i in range(len(canMovA)):
                if rsD > abs(1 - canMovA[i]):
                    rsD = abs(1 - canMovA[i])
            for i in range(len(canMovA)):
                if rsD + 0.0000000001 > abs(1 - canMovA[i]):
                    canMovF.append(canMove[i])

        for i in canMovF:
            downBoard = c.deepcopy(nowBoard)
            othello.move(i, downBoard, color)
            if len(othello.isEnableToMove(downBoard, -1 * color)) == 0 and len(othello.isEnableToMove(downBoard, color)) == 0:
                my = 0
                en = 0
                for j in downBoard:
                    for k in j:
                        if k == mycolor:
                            my += 1
                        elif k == -1 * mycolor:
                            en += 1
                if my > en:
                    tmp.append([1, 1])
                elif my < en:
                    tmp.append([0, 1])
                else:
                    tmp.append([0.5, 1])
            else:
                Wi = 0
                Ni = 0
                downWN, _ = searchDown(downBoard, -1 * color, mycolor, cnt + 1)
                for j in downWN:
                    Wi += j[0]
                    Ni += j[1]
                tmp.append([Wi, Ni])
        return tmp, canMovF


if __name__ == "__main__":
    # 보드 생성

    disboard, cnt = othello.initializeGame()
    nowply = 1

    ply = othello.intScan("플레이 색을 고르세요 흑1 백-1 : ")

    while True:
        if nowply == ply:
            print("==========플레이어 턴==========")
            if len(othello.isEnableToMove(disboard, nowply)) == 0:
                print("스킵")
            else:
                othello.printBoard(disboard, othello.isEnableToMove(disboard, ply))

                while True:
                    plc = othello.parseOriginStrForTurn(input("기보를 입력하세요 ex)a2 : "))
                    can = False
                    for i in othello.isEnableToMove(disboard, ply):
                        if plc == i:
                            can = True
                            break
                    if can:
                        othello.move(plc, disboard, ply)
                        cnt += 1
                        break
        else:
            print("==========인공지능 턴==========")
            if cnt == 0:
                othello.printBoard(disboard, othello.isEnableToMove(disboard, nowply))
                cnt += 1
                print("인공지능 수 :", 'f 5')
                othello.move([5, 4], disboard, nowply)
            else:
                if len(othello.isEnableToMove(disboard, nowply)) == 0:
                    print("스킵")
                else:
                    disboardTmp = c.deepcopy(disboard)

                    othello.printBoard(disboard, othello.isEnableToMove(disboard, nowply))
                    if nowply == -1:
                        for a in range(8):
                            for b in range(8):
                                disboardTmp[a][b] = -1 * disboardTmp[a][b]
                    print("생각중...")
                    mcts, canMov = searchDown(disboardTmp, 1, 1, cnt)
                    rs = 0
                    rsWR = mcts[0][0] / mcts[0][1]

                    for i in range(1, len(canMov)):
                        if rsWR < mcts[i][0] / mcts[i][1]:
                            rs = i
                            rsWR = mcts[i][0] / mcts[i][1]
                    print(mcts[rs][0], mcts[rs][1])
                    print("인공지능 승률", mcts[rs][0]/mcts[rs][1]*100, "%")
                    cnt += 1
                    if canMov[rs][0] == 0:
                        print("인공지능 수 :", 'a', canMov[rs][1] + 1)
                    if canMov[rs][0] == 1:
                        print("인공지능 수 :", 'b', canMov[rs][1] + 1)
                    if canMov[rs][0] == 2:
                        print("인공지능 수 :", 'c', canMov[rs][1] + 1)
                    if canMov[rs][0] == 3:
                        print("인공지능 수 :", 'd', canMov[rs][1] + 1)
                    if canMov[rs][0] == 4:
                        print("인공지능 수 :", 'e', canMov[rs][1] + 1)
                    if canMov[rs][0] == 5:
                        print("인공지능 수 :", 'f', canMov[rs][1] + 1)
                    if canMov[rs][0] == 6:
                        print("인공지능 수 :", 'g', canMov[rs][1] + 1)
                    if canMov[rs][0] == 7:
                        print("인공지능 수 :", 'h', canMov[rs][1] + 1)

                    othello.move(canMov[rs], disboard, nowply)

        nowply = -1 * nowply

        end = False
        if len(othello.isEnableToMove(disboard, nowply)) == 0 and len(othello.isEnableToMove(disboard, -1 * nowply)) == 0:
            end = True
        if end:
            no1 = 0
            no2 = 0
            for z in range(8):
                for x in range(8):
                    if disboard[z][x] == 1:
                        no1 += 1
                    if disboard[z][x] == -1:
                        no2 += 1
            if no1 > no2:
                if ply == 1:
                    print(no1, "대", no2)
                    print("플레이어 승리")
                if ply == -1:
                    print(no2, "대", no1)
                    print("플레이어 패배")
            elif no1 < no2:
                if ply == 1:
                    print(no1, "대", no2)
                    print("플레이어 페배")
                if ply == -1:
                    print(no2, "대", no1)
                    print("플레이어 승리")
            break
