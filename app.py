import hashlib
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbdotrip

# HTML 화면 보여주기


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/api/reviews', methods=['POST'])
def save_reviews():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/img/{filename}.{extension}'

    file.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
#SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
#import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
#import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;

# session 관련 정보
app.secret_key = b'aaa!111/'


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.user.find_one({"id": payload['id']})
    #     return render_template('index.html', nickname=user_info["nick"])
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    if 'user_id' in session:
        print(session)

        user_info = db.user.find_one({"id": session['user_id']})
        return render_template('index.html', id=user_info["id"])
    else:
        return redirect(url_for("login", msg="세션 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign-up')
def register():
    return render_template('sign-up.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # 리턴 값은 존재하지 않음
    db.user.insert_one({'id': id_receive, 'pw': pw_hash, })

    # 회원 가입 후 로그인 처리 까지 진행
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        # payload = {
        #     'id': id_receive,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds= 10)
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # #.decode('utf-8')

        # # token을 줍니다.
        # return jsonify({'result': 'success', 'token': token})
        session['user_id'] = id_receive
        return jsonify({'result': 'success'})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        # payload = {
        #     'id': id_receive,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')#.decode('utf-8')
        # token을 줍니다.
        # return jsonify({'result': 'success', 'token': token})
        session['user_id'] = id_receive
        return jsonify({'result': 'success'})

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop('user_id', None)
        return jsonify({'result': 'success'})
    except session.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '정상적인 요청이 아닙니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
