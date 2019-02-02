# 오셀로 인공지능 (feat.Keras)

## 개요

인공지능 모듈 케라스로 구현한 오셀로 인공지능 입니다. 몬테카를로 트리 검색 (MCTS)를 사용하였습니다.<br>
2018 진로 직업 박람회 선린인터넷고등학교 AI로 출품되었던 작품입니다.

## 주로 사용된 모듈 (requirements.txt)

Keras==2.2.0<br>
PyQt5==5.11.2<br>

## 프로젝트 구조 설명


>AllWorld<br>
┣━━━ gameData.json : 전처리 이전 기보 데이터 <br>
┣━━━ gameDataSave.py : 데이터 전처리용<br>
┣━━━ trainAw.py : 정책망 학습, 모델 생성<br>
┗━━━ trainAwValue.py : 가치망 학습, 모델 생성<br>
game.py : 파이썬으로 오셀로를 구현<br>
Play_CLI.py : 콘솔로 학습된 모델을 테스트하는 용도<br>
Play_GUI_Deep_Less.py : 트리를 더 깊게 파는 대신 생각하는 가짓수를 줄인 버전<br>
Play_GUI_Deep_Less.py : 트리를 더 얕게 파는 대신 생각하는 가짓수를 늘린 버전<br>


## 사용 방법

####  기보를 AllWorld/gameData.json에 모은다.
기보가 틀렸을 경우(게임을 진행할수 없는 이상한 기보)는 오류가 반겨준다.
> AllWorld/gameData.json
<pre>
[
  "f5d6c4d3c3f4c5b3e2c6b4e3b5a6f3g4g3b6a5g5e7d7d2a3c2a4h4d1h5f1c7f8e6c8b7f6g7a8f2g6e1h3c1b1d8b8h6f7e8h8b2h7g8g1a7a1h2h1g2a2",
  "f5d6c3d3c4f4f6f3g4g5e3e2d2h3e6g3g6f7h5h4h2c5b6h7c7e7d7c1f1d1e1c6b1d8c8e8f8a6b5g2h1f2a5g1a7b4h6g7a4a1h8a3a2b3c2b2a8b7b8g8",
  "f5d6c3d3c4f4f6f3e6e7d7g6d8c5c6c7c8b6b5e3b4a5a4a3d2b3a6a7h6f8f7b7g3e1g5h3e2g4f2d1c1b1f1g1c2e8h5g2g8h7h8g7a2a1h2h1b8a8h4b2",
  ...
]
</pre>
#### AllWorld/gameDateSave.py 를 실행한다.
많은 시간을 기다리면 프로세스가 정상적으로 완료되며 아래 파일들이 생성됨
>AllWorld<br>
┣━━━ gameData_ValueX.json : 가치망 input<br>
┣━━━ gameData_ValueY.json : 가치망 output<br>
┣━━━ gameData_x.json : 정책망 input<br>
┗━━━ gameData_y.json : 가치망 output<br>

#### AllWorld/trainAw.py와 AllWorld/trainAwValue.py 를 실행한다.
while True로 되어있으니 저장되는것 보고 끊거나 for문으로 조절하세요. 둘다 실행해서 아래 파일들이 생성되야합니다.
>AllWorld<br>
┣━━━ model.yml<br>
┣━━━ modelValue.yml<br>
┣━━━ savingModel.h5<br>
┣━━━ savingModelValue.h5<br>
┣━━━ weight.hd5<br>
┗━━━ weightValue.hd5<br>

#### Play_*.py 들로 테스팅합니다!

## 모델 상세

정책망 (2, 8, 8) -> (8 * 8)

48채널 인풋 -> 96채널 CNN 8층 -> Dropout 0.25 -> Relu(16^2) -> Dropout 0.5  -> Softmax(8*8)

가치망 (3, 8, 8) -> (2)

32채널 인풋 -> 96채널 CNN 5층 -> Dropout 0.25 -> Relu(16^2) -> Dropout 0.5  -> Softmax(2)

## 구동 확인 환경
MacOS 10.12~10.14.2<br>
Window 10(with CUDA and tensorflow-gpu)