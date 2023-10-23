import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
import game as othello
import copy as c
import os
import random
import time

import numpy as np
from keras.models import load_model

path = os.getcwd()

PieceWidth = 70
PieceMargin = 2

searchDeep = 30
minsearch = 2
SearchRange = 0.7
SemiRange = 0
semimode = True

modelPath = "AllWorld/savingModel.h5"
valueModelPath = "AllWorld/savingModelValue.h5"
if os.path.isfile(modelPath):
    model = load_model(modelPath)

if os.path.isfile(modelPath):
    modelValue = load_model(valueModelPath)

isGameing = False
disboard, cnt = othello.initializeGame()
nowply = 0
ply = 1
playerCanMove = False


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = '오셀로 인공지능'
        self.left = PieceMargin
        self.top = PieceMargin
        self.width = PieceWidth * 8 + PieceMargin * 9 + 300
        self.height = PieceWidth * 8 + PieceMargin * 9
        self.setMouseTracking(True)
        self.buttonGroup = list()
        self.startBtn = QPushButton("보드 초기화", self)
        self.start1Btn = QPushButton("흑으로 시작", self)
        self.start2Btn = QPushButton("백으로 시작", self)
        self.nowGame1 = QLabel(" 흑 점수:\n 0", self)
        self.nowGame2 = QLabel(" 백 점수:\n 0", self)
        self.aiWinRate = QLabel(" 인공지능 예상 승률: %", self)
        self.nowTurn = QLabel(" 지금 턴", self)
        self.winner = QLabel(" 결과 칸", self)
        self.msgbox = QMessageBox(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background:rgb(0,0,0);color:white")

        for i in range(8):
            beforeButtonGroup = list()
            for j in range(8):
                buttonTmp = QLabel("", self)
                buttonTmp.setGeometry(self.top + i * (PieceWidth + PieceMargin),
                                      self.left + j * (PieceWidth + PieceMargin), PieceWidth, PieceWidth)
                buttonTmp.setStyleSheet("background:rgb(92,200,113)")
                beforeButtonGroup.append(buttonTmp)
            self.buttonGroup.append(beforeButtonGroup)

        self.startBtn.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin, 300 - PieceMargin, PieceWidth)
        self.startBtn.setStyleSheet("background:rgb(192,192,192);color:rgb(0,0,0);font-size:20px")
        self.startBtn.clicked.connect(self.startClick)

        self.start1Btn.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin * 2 + PieceWidth, 150 - PieceMargin,
                                   PieceWidth)
        self.start1Btn.setStyleSheet("background:rgb(192,192,192);color:rgb(0,0,0);font-size:20px")
        self.start1Btn.clicked.connect(self.start1Click)

        self.start2Btn.setGeometry(PieceWidth * 8 + PieceMargin * 9 + 150, PieceMargin * 2 + PieceWidth,
                                   150 - PieceMargin,
                                   PieceWidth)
        self.start2Btn.setStyleSheet("background:rgb(192,192,192);color:rgb(0,0,0);font-size:20px")
        self.start2Btn.clicked.connect(self.start2Click)

        self.nowGame1.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin * 4 + PieceWidth * 3, 150 - PieceMargin,
                                  PieceWidth)
        self.nowGame1.setStyleSheet("background:rgb(64,64,64);color:rgb(255,255,255);font-size:20px")

        self.nowGame2.setGeometry(PieceWidth * 8 + PieceMargin * 9 + 150, PieceMargin * 4 + PieceWidth * 3,
                                  150 - PieceMargin, PieceWidth)
        self.nowGame2.setStyleSheet("background:rgb(255,255,255);color:rgb(0,0,0);font-size:20px")

        self.aiWinRate.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin * 5 + PieceWidth * 4,
                                   300 - PieceMargin,
                                   PieceWidth)
        self.aiWinRate.setStyleSheet("background:rgb(255,255,255);color:rgb(0,0,0);font-size:20px")

        self.nowTurn.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin * 7 + PieceWidth * 6, 300 - PieceMargin,
                                 PieceWidth)
        self.nowTurn.setStyleSheet("background:rgb(255,255,255);color:rgb(0,0,0);font-size:20px")

        self.winner.setGeometry(PieceWidth * 8 + PieceMargin * 9, PieceMargin * 8 + PieceWidth * 7, 300 - PieceMargin,
                                PieceWidth)
        self.winner.setStyleSheet("background:rgb(255,255,255);color:rgb(0,0,0);font-size:20px")
        self.show()

    def mousePressEvent(self, e):
        global nowply, ply, isGameing, playerCanMove
        if isGameing and nowply == ply and playerCanMove:
            if 10 < e.x() < 8 * PieceWidth + 7 * PieceMargin:
                if e.buttons() & Qt.LeftButton:
                    i = e.x() // (PieceMargin + PieceWidth)
                    j = e.y() // (PieceMargin + PieceWidth)
                    self.playerMove([i, j])

    @pyqtSlot()
    def startClick(self):
        global disboard, cnt, nowply, isGameing
        disboard, cnt = othello.initializeGame()
        nowply = 1
        self.resetBoard(disboard, nowply)
        isGameing = False
        self.winner.setText(" 결과 칸")

    @pyqtSlot()
    def start1Click(self):
        global ply, isGameing
        ply = 1
        isGameing = True
        self.nowTurn.setText(" 녹색칸중 하나를 고르세요.")
        self.resetBoard(disboard, nowply)
        self.playerMovePre()

    @pyqtSlot()
    def start2Click(self):
        global ply, isGameing
        ply = -1
        isGameing = True
        self.nowTurn.setText(" 인공지능 턴, 생각중...")
        self.resetBoard(disboard, nowply)

        self.aiMove()

    def resetBoard(self, board, now, last=None):
        if now == ply:
            self.nowTurn.setText(" 녹색칸중 하나를 고르세요.")
        else:
            self.nowTurn.setText(" 인공지능 생각중...")
        board = c.deepcopy(board)
        can = othello.isEnableToMove(board, now)
        for i in can:
            board[i[1]][i[0]] = 3

        blacknum = 0
        whitlenum = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    pixmap = QPixmap('./images/black.png')
                    self.buttonGroup[j][i].setPixmap(pixmap.scaled(PieceWidth, PieceWidth, Qt.KeepAspectRatio))
                    blacknum += 1
                elif board[i][j] == -1:
                    pixmap = QPixmap('./images/white.png')
                    pixmap.scaled(PieceWidth, PieceWidth)
                    self.buttonGroup[j][i].setPixmap(pixmap.scaled(PieceWidth, PieceWidth, Qt.KeepAspectRatio))
                    whitlenum += 1
                else:
                    pixmap = QPixmap('./images/white.png')
                    pixmap.scaled(PieceWidth, PieceWidth)
                    self.buttonGroup[j][i].setPixmap(pixmap.scaled(0, 0, Qt.KeepAspectRatio))

                if board[i][j] == 3:
                    self.buttonGroup[j][i].setStyleSheet("background:rgb(125,250,76)")
                else:
                    self.buttonGroup[j][i].setStyleSheet("background:rgb(92,200,113)")
                if last != None and j == last[0] and i == last[1]:
                    self.buttonGroup[j][i].setStyleSheet("background:rgb(247,205,118)")
        if ply == 1:
            self.nowGame1.setText(" 흑, 내 점수:\n " + str(blacknum))
            self.nowGame2.setText(" 백, AI 점수:\n " + str(whitlenum))
        elif ply == -1:
            self.nowGame1.setText(" 흑, AI 점수:\n " + str(blacknum))
            self.nowGame2.setText(" 백, 내 점수:\n " + str(whitlenum))

    def searchValueDown(self, nowBoard, color, mycolor, cnt, repeat):
        # 승률 반환 시킬 배열
        tmp = list()
        # 정책망에 넣기 위해 변환한 데이터 저장
        tmp1 = list()
        # 정책망용 데이터 빈곳 생성
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
        # 정책망용 데이터 대입
        for i in range(8):
            for j in range(8):
                if nowBoard[i][j] == 1:
                    tmp1[0][i][j] = 1
                elif nowBoard[i][j] == -1:
                    tmp1[1][i][j] = 1
        # 정책망 대입으로 값 도출
        aiResult = model.predict(np.array([tmp1]))
        # 움직일 수 있는 곳 저장
        canMove = othello.isEnableToMove(nowBoard, color)

        # 움직일 수 있는 곳이 없다, 상대편으로 넘긴다.
        if len(canMove) == 0:

            Wi = 0
            Ni = 0
            downBoard = c.deepcopy(nowBoard)
            downWN, _ = self.searchValueDown(downBoard, -1 * color, mycolor, cnt + 1, repeat)
            for j in downWN:
                Wi += j[0]
                Ni += j[1]
            tmp.append([Wi, Ni])
            return tmp, []
        # 움직일 수 있는 곳이 한곳보다 많다
        else:
            # 움직일 수 있는 곳들에 두었던 확률을 저장할 변수
            canMovA = list()

            # 움직일 수 있는 곳들에 두었던 확률 저장
            for a in canMove:
                canMovA.append(aiResult[0][a[0] + a[1] * 8])

            # 선별한 움직임을 저장할 변수
            canMovF = list()

            # 범위 안의 것을 저장
            for i in range(len(canMovA)):
                if SearchRange \
                        > abs(1 - canMovA[i]):
                    canMovF.append(canMove[i])

            # 만약 최소 갯수 이하라면 최소 갯수는 채우게 만듬
            if len(canMovF) == 0:
                canMovF = list()
                if len(canMovF) == 0:
                    if semimode:
                        rsD = 3
                        for i in range(len(canMovA)):
                            if rsD > abs(1 - canMovA[i]):
                                rsD = abs(1 - canMovA[i])
                        for i in range(len(canMovA)):
                            if rsD + SemiRange >= abs(1 - canMovA[i]):
                                canMovF.append(canMove[i])
                    else:
                        for z in range(len(canMovA)):
                            canMovF.append(canMove[z])

            # 둘려는 수가 한개인데 원턴킬당하면 빡치니까 전체 다 조사함
            if len(canMovF) == 1:
                downBoard = c.deepcopy(nowBoard)
                othello.move(canMovF[0], downBoard, color)

                # 원턴킬이 나면 무조건 0,1 반환시키게 검사
                onekill = False
                nextCanMove = othello.isEnableToMove(downBoard, -1 * color)
                for y in nextCanMove:
                    dnextBoard = c.deepcopy(downBoard)
                    othello.move(y, dnextBoard, -1 * color)
                    if len(othello.isEnableToMove(dnextBoard, -1 * color)) == 0 and len(
                            othello.isEnableToMove(dnextBoard, color)) == 0:
                        my = 0
                        en = 0
                        for j in downBoard:
                            for k in j:
                                if k == mycolor:
                                    my += 1
                                elif k == -1 * mycolor:
                                    en += 1
                        if my == 0:
                            onekill = True
                        break

                # 원턴킬 이면 이렇게 함
                if onekill:
                    canMovF = list()
                    for z in range(len(canMovA)):
                        canMovF.append(canMove[z])

            # 선별한 수들을 둠
            for i in canMovF:
                # 둔 다음을 저장할 변수
                downBoard = c.deepcopy(nowBoard)
                # 말을 움직임
                othello.move(i, downBoard, color)

                if repeat == 1:
                    aiInput = c.deepcopy(tmp1)
                    aitmp = [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0], ]
                    aitmp[i[1]][i[0]] = 1
                    aiInput.append(aitmp)
                    aiResultValue = modelValue.predict(np.array([aiInput]))
                    tmp.append([aiResultValue[0][0], 1])
                elif len(othello.isEnableToMove(downBoard, -1 * color)) == 0 and len(othello.isEnableToMove(downBoard, color)) == 0:
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
                    # 원턴킬이 나면 무조건 0,1 반환시키게 검사
                    onekill = False
                    nextCanMove = othello.isEnableToMove(downBoard, -1 * color)
                    for y in nextCanMove:
                        dnextBoard = c.deepcopy(downBoard)
                        othello.move(y, dnextBoard, -1 * color)
                        if len(othello.isEnableToMove(dnextBoard, -1 * color)) == 0 and len(
                                othello.isEnableToMove(dnextBoard, color)) == 0:
                            my = 0
                            en = 0
                            for j in downBoard:
                                for k in j:
                                    if k == mycolor:
                                        my += 1
                                    elif k == -1 * mycolor:
                                        en += 1
                            if my == 0:
                                onekill = True
                            break


                    # 원턴킬 이면 이렇게 함
                    if onekill:
                        tmp.append([0, 1])
                    else:
                        Wi = 0
                        Ni = 0
                        downWN, _ = self.searchValueDown(downBoard, -1 * color, mycolor, cnt + 1, repeat - 1)
                        for j in downWN:
                            Wi += j[0]
                            Ni += j[1]
                        tmp.append([Wi, Ni])
            return tmp, canMovF

    def aiMove(self):
        global cnt, disboard, nowply, ply, isGameing
        if len(othello.isEnableToMove(disboard, 1)) == 0 and len(othello.isEnableToMove(disboard, -1)) == 0:
            blacknum = 0
            whitlenum = 0
            for i in range(8):
                for j in range(8):
                    if disboard[i][j] == 1:
                        blacknum += 1
                    elif disboard[i][j] == -1:
                        whitlenum += 1
            self.nowTurn.setText(" 경기 완료")
            if ply == 1:
                if blacknum > whitlenum:
                    self.winner.setText(" 흑, 플레이어가 이겼습니다.")
                elif blacknum < whitlenum:
                    self.winner.setText(" 백, AI가 이겼습니다.")
                else:
                    self.winner.setText(" 무승부 입니다.")
            elif ply == -1:
                if blacknum > whitlenum:
                    self.winner.setText(" 흑, AI가 이겼습니다.")
                elif blacknum < whitlenum:
                    self.winner.setText(" 백, 플레이어가 이겼습니다.")
                else:
                    self.winner.setText(" 무승부 입니다.")

            isGameing = False
        else:
            if cnt == 0:
                cnt += 1

                othello.move([5, 4], disboard, nowply)
                nowply = -1 * nowply
                self.resetBoard(disboard, nowply, [5, 4])

                self.playerMovePre()
            # elif cnt == 1:
            #     cnt += 1
            #
            #     if disboard[4][5] == -1 * nowply or disboard[5][4] == -1 * nowply:
            #         othello.move([5, 5], disboard, nowply)
            #         nowply = -1 * nowply
            #         self.resetBoard(disboard, nowply, [5, 5])
            #     elif disboard[2][3] == -1 * nowply or disboard[3][2] == -1 * nowply:
            #         othello.move([2, 2], disboard, nowply)
            #         nowply = -1 * nowply
            #         self.resetBoard(disboard, nowply, [2, 2])
            #
            #     self.playerMovePre()
            else:
                if len(othello.isEnableToMove(disboard, nowply)) == 0:
                    self.showMessageBox()
                    nowply = -1 * nowply
                    self.resetBoard(disboard, nowply)

                    self.playerMovePre()

                else:

                    disboardTmp = c.deepcopy(disboard)

                    if nowply == -1:
                        for a in range(8):
                            for b in range(8):
                                disboardTmp[a][b] = -1 * disboardTmp[a][b]
                    mcts, canMov = self.searchValueDown(disboardTmp, 1, 1, cnt, searchDeep)
                    rsWR = mcts[0][0] / mcts[0][1]
                    for i in range(1, len(canMov)):
                        if rsWR < mcts[i][0] / mcts[i][1]:
                            rsWR = mcts[i][0] / mcts[i][1]
                    sameM = list()
                    sameNum = list()
                    for i in range(len(canMov)):
                        if rsWR == mcts[i][0] / mcts[i][1]:
                            sameM.append(mcts[i])
                            sameNum.append(i)
                    sameRandom = random.randrange(0, len(sameM))

                    self.aiWinRate.setText(
                        " 인공지능 예상 승률: " + str("{0:.2f}".format(mcts[sameNum[sameRandom]][0] / mcts[sameNum[sameRandom]][1] * 100)) + "%")
                    cnt += 1

                    othello.move(canMov[sameNum[sameRandom]], disboard, nowply)
                    nowply = -1 * nowply
                    self.resetBoard(disboard, nowply, canMov[sameNum[sameRandom]])

                    self.playerMovePre()

    def playerMovePre(self):
        global nowply, isGameing, playerCanMove, disboard
        if len(othello.isEnableToMove(disboard, 1)) == 0 and len(othello.isEnableToMove(disboard, -1)) == 0:
            blacknum = 0
            whitlenum = 0
            for i in range(8):
                for j in range(8):
                    if disboard[i][j] == 1:
                        blacknum += 1
                    elif disboard[i][j] == -1:
                        whitlenum += 1
            self.nowTurn.setText(" 경기 완료")
            if ply == 1:
                if blacknum > whitlenum:
                    self.winner.setText(" 흑, 플레이어가 이겼습니다.")
                elif blacknum < whitlenum:
                    self.winner.setText(" 백, AI가 이겼습니다.")
                else:
                    self.winner.setText(" 무승부 입니다.")
            elif ply == -1:
                if blacknum > whitlenum:
                    self.winner.setText(" 흑, AI가 이겼습니다.")
                elif blacknum < whitlenum:
                    self.winner.setText(" 백, 플레이어가 이겼습니다.")
                else:
                    self.winner.setText(" 무승부 입니다.")
            isGameing = False
        else:
            if len(othello.isEnableToMove(disboard, ply)) == 0:
                self.showMessageBox()
                nowply = -1 * nowply

                self.aiMove()
            else:
                playerCanMove = True

    def playerMove(self, plc):
        global cnt, nowply
        can = False
        for i in othello.isEnableToMove(disboard, ply):
            if plc == i:
                can = True
                break
        if can:
            othello.move(plc, disboard, ply)
            cnt += 1
            nowply = -1 * nowply
            self.nowTurn.setText(" 인공지능 턴, 생각중...")
            self.resetBoard(disboard, nowply, plc)

            self.aiMove()

    def showMessageBox(self):
        global disboard, nowply

        self.msgbox.question(self, '정보', '둘 수 있는 곳이 없어 넘어갑니다.',
                        QMessageBox.Yes)
        self.resetBoard(disboard, nowply)


if __name__ == '__main__':
    libpaths = QApplication.libraryPaths()
    libpaths.append(
        "/Users/nonamep/Documents/2018_Project/2018_파이썬프로젝트/ai/AlphaO/venv/lib/python3.6/site-packages/PyQt5/Qt/plugins")
    QApplication.setLibraryPaths(libpaths)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
