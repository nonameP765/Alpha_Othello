# 아이돌 생일 DB

## 개요

> https://idoldb.iptime.org, https://birth.xn--db-vf0ju60a7id96d.kr 에 서빙중인 아이돌마스터 캐릭터들의 생일을 보는 데이터베이스입니다.

## API 사용법

#### 모든 아이돌
>https://idoldb.iptime.org/api/idols/<br>
>https://birth.xn--db-vf0ju60a7id96d.kr/api/idols/

method: GET<br>
parameter: None

response:
<pre>
{
    "count": 104, // 총 아이돌 수
    "next": "http://idoldb.ngdb.kr/api/idols/?page=2", //다음페이지
    "previous": null, //이전페이지
    "results": [
        {
            "id": 1,
            "JapaneseName": "はぎわら ゆきほ",
            "KanjiName": "萩原 雪歩",
            "KoreanName": "하기와라 유키호",
            "age": 17,
            "height": 155,
            "weight": 42,
            "birth": "2018-12-24",
            "bloodType": "A",
            "BWH": "81-56-81",
            "hobby": "시 쓰기, 다과, 블로그",
            "bornPlace": "도쿄",
            "color": "#D3DDE9",
            "voice": "아사쿠라 아즈미",
            "mainPicture": "/media/Yukiho.png", //실제로 사용하시려면 media 대신 static을 쓰시고 url에 넣으세요
            "signPicture": "/media/YukihoSign.png", //ex) idoldb.ngdb.kr/static/Yukiho.png
            "production": 1
        }, .....
    ] //아이돌들
}
</pre>

#### 아이돌 검색
>https://idoldb.iptime.org/api/idols/<br>
>https://birth.xn--db-vf0ju60a7id96d.kr/api/idols/

method: GET<br>
parameter:<br><br>
id검색을 진행하면 id 파라메터만 적용됩니다.<br><br>
id="" //id 검색(반환값 무조건 1개)<br><br>
response:
<pre>
{
    "count": 3, // 검색된 아이돌 수
    "next": "http://idoldb.ngdb.kr/api/idols/?page=2", //다음페이지
    "previous": null, //이전페이지
    "results": [ ] // 검색된 아이돌들 
}
</pre>
<br>
<hr><br>
id검색을 진행하지 않으면 아래 파라메터는 중복이 가능합니다!
<br><br>
korean_name="" //한글 검색<br>
japanese_name="" //일본어 검색<br>
kanji_name="" //한자 검색<br>
produntions="" //소속(ex. 따음표없이 '1,2,3' 넣으면 나옴)<br>
1: 본가마스<br>
2: 961프로덕션<br>
3: 샤니마스<br>
4: 밀리마스<br>
5: 신데마스(추가중)<br><br>
response:
<pre>
{
    "count": 3, // 검색된 아이돌 수
    "next": "http://idoldb.ngdb.kr/api/idols/?page=2", //다음페이지
    "previous": null, //이전페이지
    "results": [ ] // 검색된 아이돌들 
}
</pre>


## 본 프로젝트 사용법

1. git clone "https://github.com/nonameP765/idolDB_Django.git"<br><br>
2. cd 클론된폴더<br><br>
3. mkdir .config_secret<br><br>
4. 아래와 같이 프로젝트 루트에 파일 생성<br><br>
 .config_secret<br>
┣━━━ settings_common.json<br>
┣━━━ settings_debug.json<br>
┗━━━ settings_deploy.json<br><br><pre>
settings_common.json<br><br><code>{
  "django": {
    "secret_key": 시크릿 키,
    "email_password": 이메일 비밀번호,
    "email":이메일 주소,
    "database": 데이터베이스 설정
  }
}
</code><br>
settings_debug.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      테스트용 호스트
    ]
  }
}
</code><br>
settings_deploy.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      서빙용 호스트
    ]
  }
}</code></pre>

5. 마이그레이션 등등 설정...<br><br>
6. 디버깅용 옵션 --settings=ngdb.settings.debug <br>
실서비스용 옵션 --settings=ngdb.settings.deploy
<br><br>

###버전
<h5>1.0.0</h5>
https로 서비스 시작<br>
계정 관리를 모두 기본 auth로 변경<br>
인덱싱 관리를 세션에서 GET으로 변경<br>
기타 쿼리 최적화
<h5>Alpha v12.3.1_drf</h5>
rest Api 가동<br>
view를 모두 제네릭뷰로 리메이크
<h5>Alpha v11.28.1</h5>
디자인 구현<br>
로그인 관련 예외들 적용
<h5>Alpha v11.26.1</h5>
디자인 없는 방명록 구현<br>
담당 아이돌 기능 추가
<h5>Alpha v11.25.1</h5>
방명록, 아이돌 댓글을 위한 계정 생성<br>
주소 idoldb.ngdb.kr로 변경
<h5>Alpha v10.29.2</h5>
신데마스 캐릭터 지속적인 추가
<h5>Alpha v10.29.1</h5>
이름검색 지원, 코토리 파비콘 생성
<h5>Alpha v10.10.1</h5>
신데마스 큐트 일부 추가, 레이아웃 일부 변경
<h5>Alpha v10.05.2</h5>
배포용 프로젝트 설정 완료, DEBUG = False
<h5>Beta v10.05.1</h5>
아이돌 전체 목록에 인덱싱 추가(최적화 차원)
<h5>Beta v09.27.1</h5>
초기 서빙용 버전
<br><br>

우분투 18.04를 기준으로 만들어졌습니다!