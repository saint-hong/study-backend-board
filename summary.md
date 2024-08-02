# 전체 프로세스 요약 및 정리
- Flask를 사용하여 게시판 웹 서비스 개발

## 1. 소스코드 실행을 위한 batch 파일 
- `배치 파일 : .cmd 확장자인 파일`
   - 여러 명령어를 한번에 실행해주는 파일과 같다.
- batch 파일의 위치 path를 환경변수에 추가하기
   - 윈도우 기준
   - 환경변수에 batch 파일의 path를 추가해 놓으면 특정 명령어를 어디에서든 실행할 수 있다.
   - 윈도우버튼 + R ===> sysdm.cpl ===> 시스템 속성 ===> 고급 ===> 환경변수 ===> 사용자 변수 목록 ===> Path 누르고 편집 ===> 환경 변수 편집 창 ===> 새로만들기 ===> 해당 batch 파일의 path 입력 후 확인 ===> 환경변수 창에서 확인
- `path 환경변수 확인`
   - set path 명령어 입력 : 추가한 path가 보임
- 윈도우의 batch file 이 리눅스에서는 shell script 와 같다. 
   - 이에 대해서는 linux_summary에 정리 했음

## 2. Flask

### 1) flask run
- 플라스크는 FALSK_APP 환경변수가 지정되어 있지 않은 경우 app.py를 자동으로 기본 application으로 인식한다.
   - flask run 도 application을 실행하는 명령어이다.
- application 파일명이 app.py가 아닌 경우 이 파일명을 FALSK_APP 환경변수로 셋팅하면 됨
   - set FALSK_APP=<my_service>
   - flask run 하면 이 my_service.py 파일을 어플리케이션으로 인식하고 실행한다.
   - FLASK_APP=my_service.py flask run 이렇게 실행해도 됨
- 디버깅 설정 : 디버그 모드
   - 오류가 발생하면 디버깅 결과 메시지를 웹브라우저에 출력해준다.
   - 서버 실행 중(어플리케이션 실행 중)에 코드, 프로그램이 바뀌면 재설정하여 반영해준다.
- set FLASK_DEBUG=true
   - flask run
   - 어플리케이션 실행에서 FLASK_DEBUG=1 로 함께 명령해도 됨
- set FLASK_APP과 set FALSK_DEBUG를 쉘 스크립트로 자동 실행되도록 해도 된다.

### 2) WSGI 서버와 개발 서버
- falsk run 은 어플리케이션을 개발 서버에서 실행한다는 의미
   - flask run 하면 WSGI 관련 warnnig이 나오는 이유
- WSGI 서버에서 실행하는 방법은 따로 있음
   - 추후에 다루게 됨

### 3) 애플리케이션 팩토리
- application factory : app=Flask(__name__)을 전역으로 사용하는 경우 순환 참조(circular import) 오류가 발생할 수 있는데 이 것을 해결해 주는 flask의 내부함수
   - def create_app() 함수

### 4) 애너테이션과 라우팅 함수
- @app.route('/') : 애너테이션
- def ping() : 라우팅 함수
   - @app.route('/') 애너테이션이 URL을 라우팅 함수와 매핑해준다.

### 4) 블루프린트 클래스 (사용하면 편할 듯)
- `라우팅 함수를 체계적으로 관리할 수 있는 flask의 클래스`
   - from flask import Blueprint
- create_app() 함수안에 여러가지 라우팅 함수들을 만들지 않고, 라우팅 함수들만 다른 파일에서 블루프린트 클래스를 사용해 연결 할 수 있다.
- 즉 minitter에서 __init__.py 에 create_app() 함수를 만들고 여기에 라우팅 함수들을 넣었는데, 라우팅 함수들을 main_views.py 파일에서 관리하고, __init__.py 의 create_app()에서는 이 블루프린트 클래스를 가져와서 라우팅 함수들을 사용한다.

#### 블루프린트 기본 코드
- Blueprint("main", __name__, url_prefix='/')
   - "main" : Blueprint의 별칭
   - __name__ : 모듈명 (main_views)
   - url_prefix='/' : URL의 기본 접두어, 이것을 /main이라고 설정하면, 모든 URL의 시작점이 /main이 된다.
      - /main/ping

"""
[main_views.py]

from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/ping', methods=['GET'])
def ping() :
   return 'pong'

~~~ 블루프린트 엔드포인트를 init 파일에서 불러오기 설정 ~~~
   
[__init__.py]

from flask import Flask


def create_app() : 
   app = Flask(__name__)
   
   from .views import main_views
   app.register_blueprint(main_views.bp)
   
   return app   
"""

## 3. ORM 사용하여 SQLite에 데이터 생성하기 (object relational mapping)
- 파이썬에서 쿼리를 사용하지 않고 파이썬 문법으로 데이터 베이스를 실행시킬 수 있도록 해준다.
   - 저장, 생성, 조회 등...
   - class Question() 와 class Answer() 를 사용하여 데이터 베이스에 명령과 결과에 대한 반환을 받는 구조로 이루어져 있다.
   - minitter에서는 sqlalchemy 패키지를 설치하고 쿼리를 사용하여 이에 대한 결과값을 바로 반환 받음
- `ORM을 사용하여 명령을 내리면 SQL 쿼리로 변환하여 데이터 베이스를 실행함`
- `ORM 장점`	
   - 데이터 베이스의 종류에 상관업싱 일관된 코드를 유지
   - 프로그램 유지 보수가 편하다
   - 내부에서 SQL 쿼리를 자동으로 생성하므로 개발자가 달라도 통일 된 쿼리를 작성할 수 있음
- 플라스크 ORM 라이브러리
   - SQLAlchemy : 많이 사용함
   - sqlalchemy의 orm을 사용하거나, query를 사용하거나 할 수 있음
- Flask_Migrate 라이브러리 : 파이썬을 이용해 테이블을 생성하고 컬럼을 추가할 수 있다.
   - 기본적으로 데이터 베이스를 만들려면, mysql 을 설치 한 후 데이터 베이스 접속을 통해 작업 가능
   - Flask_Migrate 라이브러리는 이 과정 대신 파이썬에서 테이블을 만들어 주는 기능
- `SQLite : 가벼운 데이터 베이스`
   - 소규모 프로젝트에서 주로 사용
   - SQLite로 빠르게 개발을 진행하고 규모가 커지면 다른 데이터 베이스를 사용하는 경우 많음
- confit.py 에 sqllite 실행 위치 설정
   - 지정한 path에 pro2.db 라는 파일로 저장 된다.
- `실행과정`
   - sqlite path 설정 : config.py ===> SQLALCHEMY_DATABASE_URL = 'sqlite:///{}'.format(os.path.join())
   - __init__.py 에 객체 생성 및 등록 :
      - db, migrate 객체 생성 : __init__ ===> db = SQLAlchemy(), migrate = Migrate()
      - app 객체에 config 파일 등록 : app.config.from_object(config)
      - app 객체에 db 객체 등록 : create_app() ===> db.init_app(app)
      - app 객체에 migrate 객체 등록 : create_app() ===> migrate.init_app(app, db)
      - sqlite 데이터 베이스 초기화 : FALSK_APP=__init__.py flask db init
         - migrations 디렉토리가 생성되고 db를 관리하기 위한 실행파일들이 생긴다.
   - model.py 에 테이블 생성 ORM 명령어를 클래스안에 입력한다.
      - 테이블 생성 하고 컬럼의 스키마 설정
      - class Question(db.Model) : Question 테이블 생성
      - class Answer(db.Model) : Answer 테이블 생성
   - 스키마 설정
      - primary_key = True : 이 테이블의 고유값을 의미함, 순차로 증가함
      - nullable = False : null 값 허용 여부, 디폴트값은 True
      - db.Integer(), db.String(200), db.Text(), db.DateTime() : 데이터 타입 설정
      - db.ForeignKey('quesion.id', ondelte='CASCADE') : 외부키 설정, 다른 테이블과 연결된 속성, ondelte는 연결된 속성이 삭제되면 같이 삭제되도록 설정함, CASCADE는 데이터베이스 명령어로 쿼리를 사용해야함, 파이썬 코드만으로도 삭제 될 수 있게 설정 가능
      - db.relationship('Question', backref=db.backref('answer_set')) : answer 테이블에서 question 테이블을 생성하는 명령어, question 테이블의 컬럼을 불러올 수 있다, backref는 역참조 기능, 즉 현재 question에 달린 여러 answer들을 answer_set으로 참조 할 수 있다.
   - __init__.py 에서 modles.py를 임포트
   - migrate로 리비전 파일 생성 : 데이터 베이스 작업을 위한 파일, 테이블 생성등에 관한 쿼리가 저장되어 있음, 무작위 숫자 이름.py
      - flask db migrate
   - 리비전 파일 실행
      - flask db upgrade
   - pro2.db 파일 생성 됨 : config.py에서 설정한 이름, SQLite의 데이터베이스의 데이터 파일이다.
- SQLiteBrowser 다운 받은 후 pro2.db 파일 열기하면 데이터 베이스 나온다.
- flask shell 실행하고 여기에서 db에 데이터를 생성하고, 삭제하고, 조회할 수 있다.
   - ORM 명령어를 사용한다. sql 문법하고 조금 다르다.
   - 데이터가 화면에 나오는 것 같지는 않다.

## 3. 게시판 서비스의 각종 기능 구현

### 1) view 파일을 기능별로 나누기
- blueprint 기능을 사용하여 엔드포인트를 기능별로 파일로 나눈다.
   - main_view.py, question_view.py, answer_view.py
   - __init__.py에서 app.register_blueprint(question_view.bp) 로 설정 추가

### 2) redirect와 url_for 함수 기능
- 엔드포인트의 URL이 복잡해지고 기존의 것이 변할 경우 템플릿 파일 등에서 이 URL을 수정하기가 어려워진다.
   - /question/detail/2 ===> /question/2/detail 이런식으로 변경 등...
- redirect와 url_for 함수를 사용하면 특정 엔드포인트의 라우팅 함수를 찾아서 연결시킬 수 있다.
   - from werkzeug.utils import redirect
   - from flask import url_for
   - redirect(url_for('question.qlist'))
      - 현재의 엔트포인트가 실행되면 redirect는 입력받은 URL로 연결을 설정해준다.
      - url_for()는 입력받은 블루프린트의 name에서 라우팅함수를 찾고, 이 라우팅함수의 URL 주소를 반환한다. 여기에서 question.qlist는 question 블루프린트에서 qlist라는 라우팅 함수를 의미한다.
- question_list.html 에서도 url_for() 함수를 사용할 수 있다.
- view 파일들 안에서 서로 사용할 수 있다.
   - bp.route('/') 인 엔드포인트에서 redirect(url_for('question.qlist')) 를 반환하도록 하면
   - / 주소를 입력하면 question.qlist의 URL 주소인, /question/list/ 로 연결되어, 질문의 리스트가 화면에 나온다.

### 3) url_for 함수
- 라우팅 함수, 정적 파일의 URL을 찾아서 반환한다.
- .py 파일에서 redirect() 함수 안에서 사용하거나
   - redirect(url_for('question.qlist')) : qlist 라우팅 함수
- .html 파일에서 사용할 수 있음
   - "{{url_for('<디렉토리명, 테이블의 속성값 등>', 인자값=인자값)}}" : 디렉토리명

### 4) html 파일에서 CSS 파일을 연결하여 페이지 꾸미기
- <link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
   - static 디렉토리의 style.css 파일을 연결한다는 의미
- html의 input text area와 push 버튼이 .css 파일의 값들을 따라서 조정 된다.

### 5) 플라스크의 폼 사용
- 플라스크의 form은 사용자가 입력 양식을 편하게 할 수 있는 기능과 입력 된 데이터를 검증해주는 기능을 한다.
   - validators 인수에서 DataRequired 값을 설정하여 입력된 데이터를 검증해준다.
   - form.validate_on_submit()으로 검증결과 값을 반환 받을 수 있다.
- 라이브러리 설치
   - pip install flask-wtf
   - 플라스크 환경변수 secret_key 필요 : 웹 사이트의 보안을 위해서 secret_key 기반 CSRF 토큰을 생성, 실제 웹에서 만들어진 데이터인지 외부에서 가짜로 만들어진 데이터인지 확인하는 과정
   - CSRF 토큰은 CSRF 공격을 막기위해 무작위로 만들어진 문자열
- forms.py 만들고 질문 등록용 form 등록
   - from flask_wtf import FlaskForm
   - class QuestionForm(FlaskForm) : FlaskForm 클래스를 상속받는 QuestionForm 클래스 생성
   - subject()와 content() 속성 : 플라스크의 폼에서 사용할 수 있는 속성은 여러가지가 있다.
      - StringField, TextAreaField 등...
      - StringField('title', validators=[DataRequired()]) : validators는 검증용 인수
         - DataRequired() : 필수항목인지 체크
         - Email() : 이메일 체크
         - Length() : 길이 체크 등등
      - validators=[DataRequired(), Email()] : 이런식으로 사용 가능
- 플라스크 폼을 설정 한 후 질문을 등록할 수 있는 엔드포인트 생성
- templates/question/question_form.html 생성
   - <form method="post" class="my-3"> : HTTP 통신의 methods 값을 post로 설정
   - html의 <form> 태그에는 보통 action="{{url_for()}}" 속성을 넣는다. action 속성을 지정하면 현재 html은 action에서 설정한 url에서만 사용이 가능하다. 템플릿을 다른 url에서도 사용하려면 <form> 태그에 action 속성을 설정하지 않으면 된다.

### 6) 네비게이션 바
- 메인 페이지로 돌아가는 기능
   - 모든 페이지에서 볼 수 있어야 한다.
   - <body> 태그 아래에 네비게이션 바 코드 추가 : 모든 화면의 위쪽에 고정되는 부트스트랩 컴포넌트
   - 또는 <body> 태그 아래에 {%include "navbar.html"%} include 기능을 사용하여 네비게이션 바의 html 파일을 불러 올 수 있다.
      - navbar.html 파일에 네비게이션 코드 저장 후 templates 파일에 저장
- 화면 상단에 로고 버튼을 넣고누르면 메인 페이지로 돌아간다.
   - sign up, login 버튼도 같이 넣는다.
   - 네비게이션 바의 오른쪽에 햄버거 메뉴 버튼이 자동으로 생성된다.
- 부트스트랩 자바스크립트 파일을 추가해야한다.
   - bootstrap zip 파일안에 있음
   - static 디렉토리에 붙여 넣는다.
   - static 디렉토리는 정형 파일들을 보관하는 디렉토리이다. 이미지, css, 자바스크립트 등...
- {%include ""%} : 반복적으로 사용하는 template를 html 파일로 따로 만들고 include 기능을 사용하여 불러 올 수 있다.

### 7) 페이징 기능
- 리스트가 많은 경우 다음 페이지로 넘겨준다.
- 플라스트 셀을 이용하여 질문 300개 생성
- question_view.py 에 /list 엔드포인트에 코드 추가
   - GET request에서 page 값을 가져온다.
      - page = request.args.get('page', type=int, default=1)
   - ORM의 question_list 객체에 paginate 함수를 적용하여 paging 기능을 추가한다.
      - question_list = question_list.paginage(page=page, per_page=10)
- question_list.html 파일에 question_list for 문에 pagination 객체의 items로 대체한다.
   - {% for question in question_list.items %}
- question_list 객체는 pagination 객체가 됨

### 8) 페이지 이동 기능
- pagination 객체의 속성값을 사용하여 페이지 이동기능을 구현할 수 있다.
   - 어려운 기능이다.
   - paginate 함수덕분에 구현이 수월하다.
- bootstrap의 pagination 컴포넌트를 사용하여 웹 페이지의 디자인을 보기 좋게 한다.
- bootstrap에 다양한 기능에 대한 예시들이 있다.

### 9) 데이터에 적용할 필터 만들기
- 데이터 입력시 현재 시각이 입력이 되는데, 초의 소수점까지 나오기때문에 보기에 불편하다.
   - 데이터 입력시 question_view.py와 answer_view.py에서 /create 엔드포인트의 라우팅 함수에서 각각 datetime.now() 값을 소수점 없이 초단위까지만 입력되도록 변경 하였다.
- 또는 filter.py 파일을 만들고 이러한 문제를 해결한다.
   - 필터 역할을 할 함수를 만든다.
      - def filter_datetime()
   - __init__.py 에서 함수를 임포트한 후 app 객체의 jinja_env.filters의 인수값으로 설정한다.
      - from .filter import filter_datetime
      - app.jinja_env.filters['datetime'] = format_datetime
      - 필터명으로 datetime을 설정 후 입력하면 format_datetime 함수가 호출 된다.
   - html에서 해당 필터를 사용해야하는 곳에 파이프를 사용하여 적용한다.
      - {question.create_date | datetime}

### 10) 게시물 일련번호 자동으로 매기기
- 번호 = 전체 게시물 수 - (현재 페이지 - 1) * 페이지당 게시물 수 - 나열인덱스
   - 나열 인덱스는 현재 페이지에서 게시할 수 있는 게시물의 인덱스
   - 현재 페이지에 나타낼 게시물이 5이면 0~4가 나열 인덱스가 된다.
- 이 공식을 사용하면 한페이지당 10개의 게시물이 들어가는 리스트에서 페이지에따라서 자동으로 번호가 매겨진다.
- question_list.html에 이 공식을 그대로 적용한다.
   - {{question_list.total - ((question_list.page - 1) * question_list.per_page) - loop.index0}}
   - pasination 객체각 적용 된 question_list의 속성값들을 사용하여 간편하게 적용할 수 있다.

### 11) 질문 제목 옆에 답변의 갯수 표시하기
- question_list.html 코드 추가
   - 제목 <td> 태그 안에 제목 아래에 코드 추가
   - {% if question.answer_set | length > 0%}
   - <span class="">{{question.answer_set | length}}</span>


### 12) 회원 가입 기능
- models.py 에 User 클래스 추가
   - models.py는 데이터 베이스의 테이블을 생성하는 파일
   - class User(db.Model) :
   - id, name, password, email, profile 컬럼과 스키마 정보 설정
- 터미널에서 migration 사용하여 models.py에서 만든 스키마로 데이터 베이스 업데이트
   - FLASK_APP=__init__.py flask db migrate
      - migration/versions 안에 리비전 .py 파일이 생성됨
      - 최신날짜인 파일이 방금 생성한 것
   - FLASK_APP=__init__.py flask db upgrate
      - 방금 생성한 리비전 파일로 데이터 베이스의 스키마를 업데이트 한다.
- SQLite Browser에서 User 테이블 확인
   - quey로 데이터 삽입
- 회원가입 폼 생성 : 회원가입 템플릿
   - form.py에 UserCreateForm(FlaskForm) 클래스 생성
   - username, password1, password2, email, profile 객체 생성
   - 각각 wtforms의 Field를 사용하여 생성한 후, validators=[] 인수에 필요한 검증 기준들을 넣는다.
   - password1은 EqualTo() 검증기능을 사용해 password2와 비교한다.
   - email은 Eamil() 검증기능을 사용한다. ===> 패키지 설치 필요 pip install eamil_validator
- auth_view.py 만들기
   - signup form class의 검증 기능을 적용한 데이터 저장 코드 생성
   - class UserCreatForm()
   - HTTP 요청이 POST 이면 user 데이터를 생성하도록 한다.
      - ORM 명령으로 데이터 베이스에서 form.username.data로 조회를 한 후, 결과값이 없으면 user 정보를 생성 한다.
      - password 컬럼의 값은 flask의 generate_password_hash() 기능을 사용하여 입력된 비밀번호 form.password1.data를 변형시켜 저장한다.
      - 정보 생성이 끝나면 main/index 페이지로 이동한다.
      - user name으로 검색했을 때 값이 존재하면 flash() 함수를 사용하여 에러메시지를 발생하도록 한다.
      - flash() get message 기능을 사용하여 html에서 사용하여 메시지를 화면에 나타낼 수 있다.
   - HTTP 요청이 GET 이면 singup 페이지를 보여주도록 한다.
- __init__.py에서 auth_view 블루 프린트를 추가해준다.
- signup.html 만들기
   - base.html 의 기본 틀을 사용한다.
   - csrf_token을 생성한 후, include 기능을 사용하여 form_error.html의 기능을 가져온다.
      - field 에러와 비밀번호 에러가 발생하면 메시지를 보여주는 부분.
   - user name, password, check password, email input를 구성한다.
   - create 버튼을 누르면 POST 요청을 보내게 되어 데이터를 저장한다.
- form_errors.html 만들기
   - signup.html 에서 include 기능을 사용하여 필드 에러와 비밀번호 에러 메시지 화면을 불러올때 사용된다.
   - field 에러는 form의 eorro의 값을 사용한다.
      - form.errors.items()
   - 비밀번호 에러는 auth_view.py에서 사용한 flash() 함수의 기능을 사용한다.
      - get_flashed_messages()에서 에러 메시지를 가져와 화면에 나타낸다.

### 13) 로그인과 로그아웃

#### 로그인
- form.py에 로그인 폼 클래스 생성
   - class UserLoginForm(FlaskForm)
   - username과 password를 입력받고 vlidators로 데이터를 검증하도록 한다.
- auth_view.py 파일에 로그인 엔드 포인트 생성
   - HTTP 요청으로 GET, POST를 받는다.
   - POST 요청이면 User 테이블에서 username에 해당하는 데이터를 user에 저장한다.
      - form.username.data
   - username에 해당하는 user 데이터가 없으면 erorr 값에 not exist user 문자열을 저장
   - user 데이터는 있지만, password가 불일치하는 경우 error 값에 not correct password 문자열 저장
      - werkzeug.security의 check_password_hash 모듈을 사용하여 데이터 베이스에 저장한 최초 패스워드와 현재 입력한 패스워드 값을 비교한다. 같은면 T, 다르면 F
   - user 데이터와 패스워드가 문제가 없으면 error는 None 값이고, 이 경우 session 데이터를 지운 후에 현재 입력받은 user의 id 값을 저장한다.
      - session.clear() ---> session['user_id'] = user.id
      - session은 웹 서버에서 저장하고 있는 데이터 메모리 공간
   - 입력 데이터에 대한 검증이 끝났으면 main 화면으로 연결한다.
   - error가 있으면 flash에 error 값을 전달하여 화면에 에러 메시지를 보여준다.
   - GET 방식의 요청이면 login.html 화면으로 이동하게 한다.
- login.html 파일 생성
   - user name과 password를 입력할 수 있는 창을 구성한다.
   - 에러가 있는 경우 include 기능을 사용하여 form_errors.html 페이지를 보여주도록 한다.
      - form_errors.html 은 필드값에 대한 error와 flash 기능을 사용한 error 메시지를 나타내도록 한다.
   - user name과 password를 입력한 후 login 버튼을 누르면 form 엘리먼트가 POST 방식의 HTTP 요청을 현재 주소인 auth/login에 보내게 된다.
- navbar.html 파일에 login 버튼의 연결 링크를 추가한다.
   - href={{url_for('auth.login')}} : auth 블루 프린트의 login 라우팅 함수의 엔드포인트 URL을 연결하라는 의미

#### 로그아웃
- navbar.html 파일에 로그인 버튼과 로그아웃 버튼 생성
   - login 라우팅 함수에서 로그인 성공 시 저장한 session['user_id'] = user.id 을 사용하여 로그인 상태를 확인 한다.
   - 이 값이 있으면, flask의 전역 변수인 g 객체에 user_id의 데이터(name, email, password)를 저장한다.
- navbar.html에 로그인과 로그아웃 상태의 버튼 표시하기
   - g.user 값을 사용하여
   - 로그인 이전에는 login 버튼을 활성화하고, 로그인 후에는 logout 버튼을 활성화 한다.
- auth_view.py에 logout 라이팅 함수 생성
   - logout 라우팅 함수가 실행되면 session.clear()를 실행하여 session에 저장된 user 데이터를 삭제한다.
- navbar.html에 logout 버튼의 주소를 연결한다.
   - href="{{url_for('auth.logout')}}"

### 14) 모델 수정 및 로그인 데코레이터 함수 사용
- SQLite의 flask ORM 사용시 오류 발생
   - 인덱스 등의 제약 조건의 이름을 MetaData 클래스를 사용하여 규칙을 설정해주어야 한다.
- models.py 파일에서 기존 테이블에 user_id, user 컬럼 추가
   - Question 클래스와 Answer 클래스에 user_id와 user 컬럼을 추가
   - 컬럼의 속성으로 nullable=False 로 설정하면 null 값을 허용하지 않는다는 의미
   - 리비전 파일 생성 후 업그레이드 하면 오류 난다.
      - flask db migrate -> flask db upgrade
   - 기존 데이터는 user_id 컬럼값이 없어서 null 값을 허용하지 않는 속성으로 생긴 오류
   - 이미 리비전 파일을 업그레이드 하면서 db upgrade 오류와 함께 해결해야한다.
      - nullable=True, sever_default=1 로 설정하고 migrate -> upgrade 다시 하기
      - server_default=1은 기존 데이터를 포함하여 모든 데이터의 값을 1로 입력한다.
         - default=1은 새로 생기는 데이터에만 1값을 입력한다.
      - nullable=False, server_default는 설정안함, 후 migrate -> upgrade 다시 하기
    - flask db migrate와 upgrade는 리비전 파일을 만들고 데이터 베이스에 업그레이드하는 과정인데 여기에서 리비전 파일의 상태를 조회할 수 있다.
       - flask db heads : 최종 버전의 이름 확인
       - flask db current : 현재 시점의 리비전 확인
       - flask db stamp heads : 최종 버전으로 변경
- answer_view와 question_view에서 user 값 입력
   - @bp.before_app_request 애너테이션에서 만든 g.user 값을 사용한다.
   - g 객체는 현재 api의 모든 파일에서 사용할 수 있다. import g
- 로그인, 아웃 상태 체크 데코레이터 함수 만들기
   - 로그아웃 인 경우 질문과 답변을 달기 위해서 로그인을 하도록 한다.
   - 이를 위해서 auth_view에 login_required 데코레이터 함수를 만들고 필요한 엔드포인트에 적용한다.
   - login_required 함수에서는 로그인이 된 경우 g.user 값이 존재하는 것을 조건으로하여, 이 값이 없을 시 현재 페이지의 url을 _next 변수에 저장한 후, login 페이지로 이동하게 한 후, 로그인 완료하면 다시 처음의 페이지로 넘어가도록 redirect한다.
      - return redirect(url_for('auth.login', next=_next))
   - /login 엔드포인트에 이와같은 url 연결 과정을 추가한다.
      - request.args.get('next', '') 값을 가져와서 로그인이 완료되면 이 url (로그인 페이지로 넘어오기 전의 페이지 url)로 이동하게끔 한다.
   - 데코레이션 함수를 auth_view.py 파일에서 만들었지만 이것을 다른 파일에서 임포트하여 사용할 수 있다.
      - from jump2.views.auth_view import login_required
- 로그인 데코레이터의 확인 조건은 GET 요청인지 여부인데, 답변 생성 페이지에서 send 버튼을 누르기 전에(post)는 GET 이므로 질문 입력이 가능한 상황이다.
- 이것을 로그아웃 상태에서 답변 입력 창을 비활성화하도록 한다.
   - question_detail.html에서 답변 입력창에 해당하는 <textarea> 엘리먼트안에 속성으로 g.user의 존재여부를 묻고 로그인 정보가 없는 경우 g.user 정보가 없는 경우는 입력창을 disabled 비활성화 처리를 한다.

### 15) 질문과 답변에 user name 나타내기
- question_list.html, question_detail.html 에 각각 username 값을 추가 해준다.
   - question_view.py의 /list에서 question_list.html에 question_list 값을 넘겨준다.
   - question_list 값은 pagination 된  질문 리스트 이다.
   - question_list.html에서 {% for question in question_list.items() %} 를 통해 question 테이블의 user 객체를 가져온다.
   - question 테이블의 user 객체는 relationship 함수로 만들어진 객체로 user 테이블에서 같은 id에 해당하는 값이다.
   - 따라서 question에서 user의 username을 질문 작성자 값으로 사용할 수 있다.
   - {{question.user.username}}
- 답변 작성자도 마찬가지로 answer 테이블의 relationship 객체인 user를 가져와서 usernamer을 사용한다.

### 16) 질문, 답변 수정 및 삭제 + 수정 시간 추가

#### modify 수정 추가
- models.py 에 Question, Answer 클래스에 modify_date 컬럼 스키마 추가
   - 수정 시간을 입력할 수 있는 컬럼 생성
   - nullalbel=True : 빈 값을 허용
- question_detail.html에 modify, delete 버튼 생성
   - <div class="card-body"> 안에 코드 추가
- question_view.py에 '/modify'엔드포인트 생성
   - 로그인 user와 데이터 생성 유저가 같은지 확인
      - if g.user != question.user
   - 다르면 flash() 에러 반환 후 question.detail 화면으로 redirect()
   - 같으면 method 값이 POST 인지 확인
      - if request.method == 'POST' :
      - POST 요청이면 (질문 데이터 생성 페이지에서 send 버튼을 누른 경우) form의 validate_on_submint() 함수로 데이터 검증 완료 후 수정 된 데이터 업데이트 및 수정 시간 저장
   - method 값이 GET 이면 (modify 버튼을 누른 경우)
      - QuestionForm(obj=question) 으로 질문 리스트 폼에 현재 수정하려는 질문 데이터 폼을 저장
      - question_form.html 질문 생성 페이지로 보낸다.

#### delete 삭제 추가
- question_detail.html 페이지에 delete 버튼 추가
   - delete 버튼을 누르면 바로 삭제 되는 것이 아니라 삭제 확인 메시지 창이 뜨도록 조건을 추가한다.
      - <a href="javascript:void(0)" class="delete btn btn-sm btn-outline-secondary">
   - 자바 스크립트를 사용하여 삭제 확인 메시지 창을 만든다.
      - base.html에 {% block script %}를 만들고,
      - question_detail.html의 delete 버튼 아래에 이 블록을 상속받아서 자바스크립트 코드를 넣는다.
      - really delete? 질문에 대해서 취소, 확인 버튼을 누른다.
      - 확인 버튼을 누르면 question.delte 엔드포인트로 연결되도록 한다.
- question_view.py에 '/delete' 엔드포인트 추가
   - delete 버튼을 누를때 함께 받은 question_id를 사용하여 데이터 조회
   - 삭제 하려는 질문 데이터를 question에 저장
   - 로그인 유저와 질문 데이터의 유저가 같은지 확인
      - if g.user != question.user :
   - 다르면 flash() 에러 발생 후 question.detail 로 연결
   - 같으면 현재 조회된 질문 데이터 question을 db에서 제거한다.
      - db.session.delete(question)
      - db.session.commit()
   - 데이터 제거 후 질문 데이터 목록 화면으로 연결한다.
      - redirect(url_for('question.list'))
- answer 답변 데이터의 수정, 삭제 기능도 위와 같은 방식으로 한다.
   - question_detail.html에 answer의 modify, delete 버튼을 생성한다.
   - answer_form.html 파일을 만들고 답변을 생성하는 페이지 코드를 저장한다.
      - question_form.html은 질문을 생성하는 페이지의 코드
   - modify 버튼을 answer_view.py의 modify 엔드포인트에 연결한다.
   - GET 요청시 modify 엔드포인트에서 answer_form.html 페이지로 연결하여 답변을 수정할 수 있게 한다.
   - POST 요청(send버튼)시 답변 데이터를 데이터베이스에서 수정하고 question_detail.html로 연결한다.
   - delete 기능도 위와 같은 방식으로 만든다.

### 17) 수정 시간 추가
- question_detail.html 에서 question의 create_date 표시 코드 위에 question.modify_date 코드 생성
- question_detail.html 에서 answer의 create_date 표시 코드 위에 answer.modify_date 코드 생성

### 18) 추천(좋아요) 기능 추가
- 질문과 답변에 좋아요 기능 추가
- many to many 방식의 관계형 테이블이 필요하다.
   - 한 user가 여러 content를 추천 할 수 있다.
   - 한 content가 여러 user의 추천을 받을 수 있다.
   - 따라서 many to many 방식의 테이블을 만들고 연결 한다.
<질문의 추천 기능>
- models.py 파일에서 question_voter 테이블을 생성 한다.
   - class Question() 형식의 선언적 형식으로 만들지 않고 직접 테이블을 만드는 방식으로 만든다.
      - question_voter = db.Table('question_voter', db.Column('user_id'), db.Column('question_id'))
   - user_id, question_id 컬럼을 만들고 각각 primary_key=True 지정한다. 이렇게 해야 many to many 관계가 성립한다.
   - db.ForeignKey('user.id', ondelete='') : User 테이블의 id와 외부키로 연결시킨다.
   - db.ForeignKey('question.id', ondelete='') : Question 테이블의 id와 외부기로 연결시킨다.
- Question 테이블에 voter relationship 객체를 만든다.
   - relationship() 은 컬럼이 아니라 관계 객체이다. 실제 데이터베이스의 테이블에 나오지 않는다.
   - relationship() 의 대상은 User 테이블이고, 인수로 secondary와 backref 를 사용한다.
   - secondary=question_voter : Question.voter로 추가된 값을 저장할 대상으로 question_voter 테이블을 사용한다는 의미
   - backref는 User 테이블과 연결된 question_voter의 연결된 값 즉 어떤 유저가 추천한 답변 리스트를 가져온다는 의미
- answer_voter, Answer.voter 도 같은 방식으로 생성한다.
- 데이터 베이스에 리비전 파일 업데이트
- question_detail.html 질문 추천 버튼 만들기
   - 버튼을 누르면 question blueprint의 vote 엔드포인트에 연결한다.
   - 자바스크립트 기능을 사용하여 버튼을 누르면 추천하겠냐는 질문창을 띄운다.
      - <a href="javascript:void(0)" data-uri="">
   - 버튼에 추천수를 표시한다. : {{question.voter | length}} : question 테이블의 voter relationship 에서 추천을 누른 사람의 갯수를 가져온다.
- question_detail.html 파일에 추천 스크립트를 생성한다.
   - delete 버튼에 대한 자바스크립트 파일 아래에 만든다.
   - {% block script%} <> {% endblock %} 사이에 삽입
- question_view.py 파일에 /vote 엔드포인트 생성
   - question_id에 대한 Question 테이블 데이터를 변수에 저장하여
   - _question.voter.append(g.user) 로 현재 로그인한 user 객체를 append 한다.
   - 이렇게 append 하면 voter의 secondary로 설정한 question_voter 테이블에 해당 유저의 아이디와 question.id 값이 저장된다.
- answer 추천 버튼도 같은 방식으로 생성한다.
- 선언적 테이블 생성과 명시적(?) 테이블 생성에 대해서 대강 알아봄
- sqlalchemy의 relationship의 사용법에 대해서 대강 알아봄
   - 그 속성으로 secondary의 기능도 대강 알아봄

### 19) 앵커 기능 추가
- 질문에 대한 답변을 생성하거나, 수정을 하고나면 스크롤이 페이지의 위쪽 부분으로 올라가게 된다.
- 이러한 문제를 해결하기 위해서 HTML의 앵커 태그를 사용할 수 있다.
   - URL 호출시 원하는 위치로 이동시켜준다.
      - URL 뒷쪽에 앵커의 위치가 추가 된다. localhost:5000/question/detail/1/#answer_5
- question_detail.html의 답변 카드 부분에 앵커 태그 삽입
   - <a id="answer_{answer.id}"></a>
- answer_view.py 파일에서 create, modify, vote 엔드포인트의 redirect 부분에 앵커를 호출하도록 수정
   - redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
      - localhost:5000/question/detail/1/ 이다음에 #answer_6 이렇게 붙는다.

### 20) 마크다운 기능 추가
- 질문, 답변을 입력할 때 마크다운 기능을 사용할 수 있도록 한다.
   - question_view.py의 detail 엔드포인트에서 question content와 answer content를 변환시킨다.
   - question.content는 Question 데이터 베이스 객체를 직접 수정하면 되고
   - answer.content는 질문에 대한 답변이 있는 경우에만, question.answer_set의 데이터를 변환한다.
- jump2 에서는 flask-markdown 라이브러리를 사용하도록 되어 있는데, 플라스크 버전이 업데이트 되면서 호환이 안되는 것 같다. 실행 안됨.
- 구글링을 통해 다른 방식으로 마크다운 기능을 사용할 수 있는 방법을 찾아냄
- question_view.py 파일에서 python의 markdown 라이브러리를 사용하여 기능을 추가 할 수 있다.
   - pip list에 이미 라이브러리가 기본으로 설치 되어 있다.
   - question_view.py 의 detail 엔드포인트에서 사용
      - question.content = markdown.markdown(question.content, extentions=['fenced_code'])
   - 이렇게 하면 마크다운 규칙을 사용하여 입력한 content를 markdown 언어로 변형 시켜준다.
- question_detail.html 파일에서 markdown 으로 변형한 컨텐츠를 보여주기.
   - question.content 를 보여주는 코드에서 safe 기능을 사용
   - {{question.content | safe}}
- 이렇게 하면 create 에서 마크다운 문장을 데이터 베이스에 저장 할 때 그대로 저장 되고, detail 엔드포인트에서 데이터베이스에서 content를 가져올 때 이 마크다운 언어를 HTML 로 변환하여 화면에 보여준다. modify 할 때도 데이터베이스에 저장 되어 있는 마크다운 언어 그대로 가져오므로 html 언어가 안 보인다.
- 답변의 markdown은 question.answer_set 을 수정하여 화면에 보여준다.
   - question.answer_set은 relationship 컬럼으로 데이터베이스에 저장 되는 것은 아니다.
   - question_view.py 파일에서 detail 엔드포인트의 코드를 수정한다.
   - detail 엔드포인트는 detail 페이지에 데이터를 넘겨주는 역할을 한다.
   - question 의 마크다운 처럼 answer 의 마크다운도 detail 엔드포인트에서 변환하여 보여주기만 한다.
   - question.answer_set 이 있다면, 즉 질문에 대한 답변이 존재한다면,
   - 그 답변을 하나씩 markdown.markdown()으로 변환하여 question.answer_set에 저장한 후 question_detail.html 에 넘겨준다.
- 마크다운 언어를 다시 텍스트로 변환 시키는 방법
   - <h2>안녕</h2>
   - 이러한 마크다운 언어를 원래 텍스트로 변형하여 나타낸다.
   - 구글링에서 html2text 라는 .py 을 모듈 임포트하여 사용하면 된다는 것을 알 수 있었다.
   - wget 으로 해당 파일의 링크 주소에서 다운 ===> form jump2.html2text import html2text ===> GET 부분에서 content를 html2text로 변형한다.
   - question.content = html2text(question.content)

### 21) 검색 기능 추가
- search 바 추가
   - 검색어 입력창과 search 버튼으로 이루어짐
- search 바 + page 바 연결 방식 바꾸기
   - class, id 등의 속성값을 바꿔 준다.
   - javascript에서 이 버튼들의 데이터를 불러오기 위함
   - search, before, page_num, next 버튼을 눌렀을 때 javascript로 데이터가 넘어가도록 한다.
- javascript에서 kw, page 등의 데이터를 추출한다.
   - 버튼을 눌렀을 때 발생한 이벤트에서 검색어(kw)와 페이지 번호(page)를 추출하여
   - form 태그를 호출하여 데이터를 넘겨준다. ---> submit()
- form 태그에서 javascript의 호출을 받아서 데이터를 사용하여 url을 만들고 엔드포인트에 넘겨준다.
   - page의 url은 /?page=1 이러한 형태였음
   - /?kw=검색어&page=1 : 이러한 url을 만들고 question_view.py의 /list 엔드포인트에 보낸다.
   - get 방식으로 kw와 page를 조합한 url로 만드는 이유 :
   - form 태그는 웹 페이지에 다양한 입력기능을 가능하게 해준다. 여러 속성값과 앨리먼트가 있다.
- 엔드포인트에서 kw 값으로 데이터 베이스의 데이터들을 조회한다.
   - subquery, outerjoin, join, filter query를 사용한다.
   - Question, Answer, User 테이블을 조회하기 위해서 subquery를 만들어 outerjoin한다.
   - 질문, 답변, 사용자를 각각 검색할 수 있다.
- javascript에서 언어 규칙을 정확하게 잘 입력해야 함 ;;;

      
## 4. Flask app 객체 기능
- <다른 객체>.init_app(app)
- app 객체에 다른 객체를 추가 해줄 수 있다.
   - db.init_app(app)
   - migrate.init_app(app, db)

## 5. SQLiteBrowser

### 1) SQLite의 GUI 프로그램
- RDBM 관리 프로그램
   - DBeaver, hidisql 같은 프로그램

### 2) 설치
- https://sqlitebrowser.org/dl/
- ubuntu 버전으로 설치
   - 우분투 버전 : 12.04.3 jemmy
   - sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser
   - sudo apt-get update
   - sudo apt-get install sqlitebrowser
- ppa 라는 도구를 사용하여 설치 하는 것 같다.
- DB Browser for SQLite 라는 아이콘 생성

### 3) 파일 열기
- 파일 ===> 데이터 베이스 열기 ===> .db 파일 열면 question, answer 테이블이 생성되어 있다.

## 6. web page

### 1) flask에서 web page 디렉토리
- templates : html 파일 자동 인식
- static : 정적 파일 자동 인식
   - 정적 파일 : 이미지, 자바스크립트(.js), 스타일시트(.css)

### 2) 웹 페이지 디자인
- static 디렉토리에 CSS 파일 저장
- HTML 표준 템플릿
   - HTML의 표준 템플릿을 따라야 어떤 곳에서 접속하더라도 정상적으로 작동한다.
   - html, head, body 엘리먼트가 있어야 하고, head 안에는 meat, title 엘리먼트 등이 있어야 한다.
- flask에 HTML 상속 기능이 있음
   - 표준 템플릿을 만들고 이것을 각각의 html 파일에서 상속 받아서 사용할 수 있다.
   - 표준 템플릿 : {%block content%} <상속 받은 html의 구조> {%endbolck%}
   - 상속 받는 템플릿 : {%extends 'base.html'%} {%block content%} <현재 페이지의 html의 구조> {%endbolck%}

### 3) 부트스트랩
- 사용하기 쉬운 웹 페이지 디자인 도구
- 트위터 개발 과정에서 만들어 짐
- 다운로드
   - 압축풀고 필요한 예시 .css 파일을 templates 디렉토리에 저장

### 4) flask-wtf : form 사용 도구
- 사용자가 데이터를 입력하기 편리하게 해주는 도구
- 입력 창을 표준화하여 자동으로 설정해준다.
   - 제목, 위치, 크기, 입력창 크기 등...

### 5) form 태그에 action 속성 여부
- <form method="post" class="my-3" action="{{url_for()}}">
   - form 태그에 action 속성을 넣는게 일반적
   - action 속성은 url_for로 한정시킨다.
   - 즉 url_for의 url이 입력되는 경우만 현재 .html 파일을 사용하겠다는 것
   - 같은 템플릿을 여러번 사용하는 경우 action 속성을 넣지 않는다.

### 6) 데이터를 입력해도 db에 저장이 안되는 이유?
- question_view.py에 ORM 사용하여 데이터 입력 부분을 생성한 후에도 db에 저장이 안된다?
- 1. <form> 태그의 method와 endpoint의 methods를 일치 시켜줘야 한다.
- 2. 또한 form.validat_on_submit() 즉 입력값 검증 부분에서 error 가 나지 않아야 한다.
   - error sign 을 반환하도록 필드를 만든다.
   - 입력값이 기준에 맞지 않거나, 비어 있는 입력값인 경우 error 발생
- 3. CSRF token error
   - CSRF 공격을 방지하기 위한 CSRF token이 생성되지 않았다는 error
   - .html 코드에 {{form.csrf-token}} 코드를 넣어준다.

### 7) question create 에서 error 가 발생한 경우 입력한 데이터를 유지하는 방법
- <input> 태그의 속성으로 value="{{form.subject.data or ''}}" 코드 입력
- <textarea> 태그의 앨리먼트로 {{form.content.data or ''}} 코드 입력
- 이미 전송한 데이터를 다시 설정하도록 해준다.
- or '' : GET 방식으로 요청되는 경우 기존 입력값이 없으면 None 으로 출력함, 즉 값이 사라지는데, 이렇게 하면 form.subject.data, form.content.data에 값이 없을때 ''이 출력된다.

## 7. AWS 서버

### 1) 고정 IP와 방화벽
- 다른 컴퓨터가 서버에 접속하기 위해서는 고정 IP와 방화벽 설정이 필요함
- AWS 서비스 마다 생성, 설정 방식이 조금씩 다르다.
- 고급 서비스 일 수록 복잡하고 기능이 다양함
- HTTP 기본 포트 80, SSH 기본 포트 22, 내가 만든 api의 기본포트 5000
- 5000 포트에 대한 방화벽 설정을 해제해줘야 다른 컴퓨터에서 접속이 가능하다.

### 2) SSH
- `네트워크 상의 다른 컴퓨터에 접속하거나, 원격 시스템 (서버)에 명령을 내리거나 수행할 수 있도록 해주는 프로토콜`
   - 이러한 SSH 프로토콜을 사용할 수 있도록 해주는 도구 : SSH 프로그램
   - SSH 프로그램을 사용하려면 프라이빗 키 혹은 SSH 키를 생성 하고 접속시에 인증해야한다.
   - 서비스마다 인증 키의 명칭이나 기능은 조금씩 다르다.
   - SSH 클라이언트 : 서버에 접속하기 위한 도구, = 터미널
   - 여러가지 SSH 클라이언트 즉 터미널 프로그램이 존재한다.
      - jump2flask는 윈도우 환경 기반으로 터밀 프로그램을 따로 다운로드 받아서 사용 mobaxterm
      - 우분투나 mac은 기존 터미널을 사용한다.
      - 접속 방식은 ssh -i <ssh key> ubuntu@<고정 IP>
   - SSH .pem 파일의 권한 에러가 생길 수 있음
      - chmod 600 <.pem>
- SSH 클라이언트 프로그램 즉 터미널을 사용하여 AWS에 생성한 가상 서버에 접속, 서버 환경 설정
   - host name 변경 : sudo hostnamectl set-hostname <원하는 이름>
      - 기본 host name은 고정 IP 주소로 되어 있음
      - 바꿔도 되고 안 바꿔도 된다.
      - 서버 리스타트 해야 적용 됨 : sudo reboot
   - host name 확인 : hostname
   - 서버의 시간 설정
      - 시간 확인 : date
      - 한국시간으로 설정 : sudo in -sf /usr/share/zoneinfo/Asia/Seoul/etc/localtime

### 3) 가상 서버에 api 관련 파일 설치 및 github 다운로드
- api 실행에 필요한 가상 환경 생성 : conda 또는 python venv
- api 실행에 필요한 패키지, 라이브러리 설치
- git hub 에서 repo clone : 인증 절차가 필요함
   - git hub 아이디, 비밀번호 입력
   - config 파일 수정하면 한 번 인증한 후에는 인증 안해도 됨
- 서버에서 flask run
   - flask 기본 setting
      - export FLASK_APP=<api 소스코드 파일 명>
      - export FLASK_DEBUG=true
      - config 파일 구분에 따른 설정 : APP_CONFIG_FILE=~/jump2/config/production.py
   - 데이터 베이스 초기화
      - SQLite 데이터 베이스의 초기화 : flask db init : migrations 디렉토리가 생성된다.
      - 데이터 베이스 서버의 리비전 파일 생성 및 업데이트 : flask db migrate, flask db upgrade
   - api 실행시 --host=0.0.0.0 은 외부에서 접속 할 수 있도록 아이피를 개방한다는 의미
- http://<고정 IP>:5000

### 4) 서버와 개발환경을 위한 config 분리하기
- 서버환경과 개발환경의 큰 차이 : config.py 파일의 SECRET_KEY 환경 변수의 차이
   - SECRET_KEY는 flask가 어떤 값을 암호화할 때 사용하는 중요한 환경 변수이다.
- 로컬의 개발환경에서는 SECRET_KEY로 단순 값 사용 : adminadmin1234 등
   - 서버환경에서는 SECRET_KEY를 단순한 문자열 조합은 사용하면 안된다.
- 환경파일 분리하기
   - config.py 모듈의 패키지 구조화
   - config/ : 디렉토리명
   - __init__.py : config 디렉토리가 "패키지"라는 것을 알려 주는 파일, 아무 내용이 없어도 됨.
   - default.py : 모든 환경에서 공통으로 사용할 변수
   - production.py : 서버 환경에서 사용할 변수
   - development.py : 개발 환경에서 사용할 변수
      - os.urandom(16) : 무작위 16자리 바이트 문자열로 SECRET_KEY를 사용
      - 또는 해쉬 암호 생성 라이브러리 사용
- __init__.py 파일의 create_app 함수에서 app.config 설정을 변경해준다.
   - 기존에는 config.py 파일을 임포트하여 사용
   - config 파일을 개발 환경과 서버 환경용으로 구분하였음
   - app.config.from_envvar('APP_CONFIG_FILE')을 설정하면 api 실행시 APP_CONFIG_FILE의 경로를 지정해 주어야 한다.
      - APP_CONFIG_FILE=~/jump2/config/production.py

### 5) 정적 페이지 요청, 동적 페이지 요청
- `웹 브라우저의 URL 요청에 따라서 크게 2가지로 나뉜다.`
   - 정적 페이지 요청 : .js, .css, .jpg, .png 와 같은 정적 데이터를 요청하는 행위, 정적 데이터는 값이 변하지 않는다 항상 그대로 이다.
   - 동적 페이지 요청 : 게시판의 URL /question/list 는 데이터가 바뀔 때마다 서버의 데이터베이스에서 다른 질문 목록을 보여준다. 즉 같은 URL을 요청 했는데 다른 결과를 보여주는 것.
- 정적 페이지 요청은 간단하지만 동적 페이지 요청은 복잡하다.
- `WSGI (web server gateway interface)`
   - 위스키
   - 웹 서버가 동적 페이지 요청을 처리하기 위해서 파이썬 프로그램을 호출해야하는데 이것을 위한 서버
   - 웹 브라우저 ---> 동적 페이지 요청 ---> 웹 서버 ---> WSGI 서버 호출 ---> WSGI 애플리케이션 호출 ---> 파이썬 프로그램 호출 ---> 동적 페이지 요청 처리
   - WSGI 서버의 종류 : Gunicorn, uwsgi 등이 있다.
   - WSGI 애플리케이션 : flask, django 등
   - WSGI 서버는 웹 서버와 WSGI 애플리케이션의 가운데에서 실행된다 : 미들웨어(middleware), 컨테이너(container)라고 부르기도 한다.
- 정적 페이지 요청은 웹 서버가 처리하고, 동적 페이지 요청은 WSGI서버->WSGI애플리케이션이 처리한다.
- flask run으로 실행되는 서버는 플라스크의 내장 서버이다.
   - 웹 서버와 WSGI 서버의 기능을 한다.
   - 대량 요청, 동시 요청 처리 등을 처리하기 어렵다.

### 6) WSGI 서버 : Gunicorn
- `Gunicorn`
   - 구니콘
- 운영 환경 = aws 가상 서버 = 서버 환경
- 구니콘 설치
   - conda activate backendenv
   - pip install gunicorn
- 구니콘으로 api 실행 (실행파일 설정을 잘 못해서 구니콘 docs 등 뒤져봄.., jump2.__init__, __init__ 다 아니고 jump2 가 맞음)
   - gunicorn --bind 0:5000 "jump2:create_app()"
   - --bind는 포트를 구분하는 단위 같은것 0:5000 은 5000번 포트를 사용한다는 의미
   - 서비스를 실행할 모듈의 명칭과 팩토리를 지정해 준다. (지정하는 방식 다양함)
- 구니콘의 unix 소켓을 사용
   - unix 계열의 시스템인 ubuntu 에서는 socket을 사용하여 api를 실행해야 더 성능이 좋다.
   - gunicorn --bind unix:/tmp/jump2.sock "jump2:create_app()"
   - 0:5000 포트 대신 unix의 socket을 사용한다는 의미, /tmp/jump2.sock 파일이 만들어진다.
   - unix 소켓을 사용하여 api를 실행하면 웹 페이지가 뜨지 않는다. 구니콘은 동적 페이지 요청에만 응답한다.
   - 따라서 정적 페이지 요청을 처리할 nginx 웹 서버를 적용해 주어야 한다.
- 구니콘 unix 소켓을 system의 service로 설정하면 가상 서버 접속시 바로 실행 된다.
   - /etc/systemd/system 디렉토리에 jump2.service 파일을 생성한다.
   - service 파일의 양식이 있음
   - 서비스 실행 : sudo systemctl start jump2.service
   - 서비스 재실행 : sudo systemctl restart jump2.service
   - 서비스 정지 : sudo systemctl stop jump2.service
   - 서비스 상태 : sudo systemctl status jump2.service
   - 서비스 활성화 : sudo systemctl enabled jump2.service

### 7) nginx
- 웹 서버의 일종 : 성능이 매우 높고, 파이썬 웹 프레임워크인 장고, 플라스크에서 많이 사용함
   - 엔진엑스
   - gunicorn의 unix socket으로 서버에 연결한 경우, WSGI 서버와 연결을 시켜주려면 Nginx 웹 서버가 필요함
   - gunicorn의 unix socket으로 서버에 연결한 경우 정적 파일 요청에 대해 응답하지 못한다.
- 설치
   - sudo apt install nginx
- nginx 설정 디렉토리 : sites-available 에서 설정 파일을 만들고, sites-enabled 에서 설정 파일을 등록한다.
   - nginx 설정 파일이 있는 디렉토리 : /etc/nginx/sites-available
   - nginx 설정 파일 등록 디렉토리 : /etc/nginx/sites-enabled
      - 여러가지 설정 파일중에서 활성화하고 싶은 것을 링크로 관리하는 디렉토리이다.
- nginx 설정 파일
   - sudo 권한으로 생성해야함
   - 기본 포트 설정, server_name, 특정 URL 일때 nginx 또는 gunicorn이 처리하도록 설정
   - /static (정적 페이지 요청) URL 요청을 받으면 nginx 가 처리하여 static 디렉토리의 파일을 읽어들인다.
   - /static 요청 이외의 URL 요청은 (동적 페이지 요청) gunicorn의 유닉스 소켓이 처리하도록 한다.
- nginx 설정 파일 등록
   - /etc/nginx/sites-enabled 디렉토리 이동 후 링크 설정: sudo ln -s /ect/nginx/sites-available/jump2
   - jump2 설정 파일이 활성화 된다. 
- nginx 실행
   - 리눅스 시스템의 systemctl로 실행하는 방식, gunicorn 서비스로 등록 후 실행하는 것과 같음
      - 실행 : sudo systemctl start nginx.service 또는 그냥 nginx만 입력 해도 됨
      - 재실행 : sudo systemctl restart nginx
      - 실행상태 : sudo systemctl status nginx
      - 실행정지 : sudo systemctl stop nginx
   - 설정 파일의 내용 오류 확인 : sudo nginx -t
- 연결이 안되는 문제
   - 1. ec2의 포트 방화벽 해제 설정
      - nginx 설정파일에서 HTTP 포트로 80을 설정하였으므로 EC2에서도 80 포트에 대한 방화벽을 해제 해야함
      - EC2 ===> 보안그룹 ===> 인바운드 규칙 설정 ===> TCP, 80, 0.0.0.0 설정 후 저장 
      - nginx가 실행 되고 있지 않으므로 unix 소켓을 통해 반환 된 css 화면만 보인다. 
   - 2. nginx.conf의 사용자 설정   
      - 고정ip/static/bootstrap.min.css 에 연결하면 nginx 웹 서버가 정적 파일이 있는 static 디렉토리에서 .css 파일을 불러와야 하는데 403 error 가 뜬다.
      - 403 에러는 권한이 없다는 뜻, 즉 nginx 가 무언가에 접근하려고 하는데 권한이 없다는 것.
      - chomod 로 접근이 필요한 디렉토리의 권한을 변경해준다. (여기에서는 권한 문제는 아니었던 것 같다.)
         - chmod -R 755 static : static 디렉토리와 하위의 모든 파일에 755 권한 지정
      - ls -al로 User와 Group 명을 확인 할 수 있다. 이 user와 group 명을 nginx.conf 파일에 설정 해준다.
      - sudo find / -name nginx.conf : nginx.conf 파일의 위치를 반환한다.
      - .conf 파일의 맨 위에 user ; 라인에 user와 group 명을 입력한다.
         - user ubuntu ubuntu ; 
      - 403 error 해결!!!
- nginx 웹 서버와 gunicorn 을 사용한 웹 페이지 연결 성공!!!

## 8. 운영환경 + 로깅적용
- 운영환경에서 실행한 웹 페이지는 에러 등이 표시되면 안된다.
   - FALSK_DEBUG=false 로 변경
- FLASK_DEBUG를 비활성화하면 internal server error 라는 메시지가 뜬다.
   - 어떤 에러인지 알 수 없으므로, HTTP 요청 응답에 관한 처리 과정을 따로 로그파일에 저장하도록 한다.
- 로깅적용
   - 파이썬의 기본 logging 모듈을 사용하여 로깅을 체크하도록 한다.
   - production.py 파일에 logging 모듈의 dictConfig를 사용하여 설정한다.
   - 로그 출력 형식, 출력 방법(handler) 등의 값을 설정할 수 있다.
   - 로그 레벨 : 단계를 설정하면 그 이상의 단계들을 출력한다.
      - logging.debug : 디버깅 목적 출력
      - logging.info : 일반 정보 출력
      - logging.warning : 경고 정보 출력 (작은 문제 발생)
      - logging.error : 오류 정보 출력 (큰 문제 발생)
      - logging.critical : 아주 심각한 문제 출력
   - logs 디렉토리 만들고 api에 접속하면 로그 정보들이 담긴 파일이 자동으로 생성된다.
   - FLASK_DEBUG=true 일때의 오류 내용 등이 담겨 있음
- app에서 직접 로그를 출력하도록 적용
   - main_view.py에 적용
   - current_app을 사용하여 현재 웹 페이지이의 로그 정보를 가져온다.
   - current_app.logger.info("INFO 레벨로 출") : 로그 레벨을 설정할 수 있다.
   - current_app.logger를 사용하면 자세한 내용이 로그 파일에 기록되지는 않는다. 정한 문자열대로 기록된다.

## 9. HTTPS와 SSL 
- (( 도메인 설정 등의 이유로 실행은 안해봄 ))
- 클라이언트(브라우저)와 서비스(서버, api) 사이에 주고 받는 데이터를 암호화해야 안전하다.
- HTTP 통신은 암호화가 안된다.
   - 브라우저의 URL 창에 주의요함 이런 문구가 떠있다.
- HTTPS는 HTTP에 SSL기능을 더한 프로토콜
   - SSL : Secured Socket Layer
- HTTPS를 적용하기 위해서는 SSL 인증서가 필요하다.
   - SSL 인증서를 발급받아서 Nginx에 적용하면 HTTPS 프로토콜을 사용할 수 있다.
- SSL 인증서 발급
   - 도메인 주소가 있어야 인증서 발급 할수 있음.
   - 인증 기관 : Comodo, Thawte, GeoTrust, DigiCert 등
   - 브라우저에 인증기관 정보가 등록 되어 있어서 인증서를 발급받고 설정하면 자동으로 파악한다.
   - 이러한 인증기관의 인증서 발급은 유료
   - 무료로 인증서를 발급할 수 있음 : Let's Encrypt 서비스
   - certbot 설치
      - sudo apt install certbot
      - sudo apt install python3-certbot-nginx
   - Encrypt 인증서 발급
      - sudo certbot certonly --nginx
- 인증서 생성 : 디렉토리에 저장된다.
   - /etc/letsencrypt/live/<도메인명>/fullchain.pem
   - /etc/letsencrypt/live/<도메인명>/privkey.pem
- nginx 설정 파일에 적용
   - HTTP 는 80포트, HTTPS는 443 포트를 사용한다.
   - 위의 인증서가 저장 된 디렉토리 path를 설정파일에 등록한다.
- EC2에서 방화벽 설정
   - nginx 설정에서 사용한 포트에 대한 방화벽을 해제해야 한다.
- HTTPS로 접속하면 "주의요함" 메시지가 없어져있다.

