from flask import Flask, render_template, request, redirect #render_template으로 html파일 렌더링
import os
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
from models import db, Fcuser
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask import session
from flask import flash

app = Flask(__name__, static_folder= "./static")
app.secret_key = 'supersecretkey'
#GET = 페이지가 나오도록 요청. POST = 버튼을 눌렀을때 데이터를 가지고오는 요청/ 요청정보확인하려면 request 임포트 필요
@app.route('/register', methods=['GET','POST'])
def register():   #get 요청 단순히 페이지 표시 post요청 회원가입-등록을 눌렀을때 정보 가져오는것
    form = RegisterForm()
    if form.validate_on_submit(): 
        fcuser = Fcuser()  #models.py에 있는 Fcuser 
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username') 
        fcuser.password = form.data.get('password')
        db.session.add(fcuser)  # id, name 변수에 넣은 회원정보 DB에 저장 
        db.session.commit()  #커밋
        
        return redirect('/') #post요청일시는 '/'주소로 이동. (회원가입 완료시 화면이동)    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])  
def login():  
    form = LoginForm() #로그인 폼 생성
    if form.validate_on_submit(): #유효성 검사
        session['userid'] = form.data.get('userid') #form에서 가져온 userid를 session에 저장
    
        return redirect('/') #로그인에 성공하면 홈화면으로 redirect        
    return render_template('login.html', form=form)

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('unity.html',userid=userid)    # 이번 포스팅에는 필요없음(지난포스팅꺼)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발, 
    
    app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx' 
    csrf = CSRFProtect()
    csrf.init_app(app)
    with app.app_context():    
        db.init_app(app) #app설정값 초기화
        db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
        db.create_all() #DB생성

    app.run(host='127.0.0.1', port=5000, debug=True) 