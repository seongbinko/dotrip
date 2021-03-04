from datetime import datetime
from bson.objectid import ObjectId
import base64
import datetime as dt
import jwt
import hashlib
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)
SECRET_KEY = 'DOTRIP'

client = MongoClient('localhost', 27017)
db = client.dbdotrip

@ app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect("reviews")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/login')
def login():
    token_expired = request.args.get("token_expired")
    return render_template('login.html', token_expired=token_expired)


@ app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@ app.route('/sign-up')
def register():
    return render_template('sign-up.html')


@ app.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwConfirm_receive = request.form['pwConfirm_give']

    check_duplicate_user = db.user.find_one({'id': id_receive})

    if check_duplicate_user is not None:
        if check_duplicate_user['id'] == id_receive:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디가 존재합니다.'})

    if pw_receive != pwConfirm_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 서로 일치하지 않습니다.'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, })

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '예기치 못한 오류가 발생하였습니다.'})


@app.route('/reviews', methods=['GET'])
def show_reviews():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        total_count = int(db.reviews.count())
        review_data = list(db.reviews.find({}).sort("review_create_date", 1).limit(12))
        reviews = []

        for review in review_data:
            review['_id'] = str(review['_id'])
            reviews.append(review)
        return render_template('reviews.html', reviews=reviews, count=len(reviews),total_count=total_count)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/api/reviews', methods=['GET'])
def get_reviews_by_index():

    skipIndex = int(request.args.get("skipIndex"))
    limit = int(request.args.get("limit"))
    review_data = list(db.reviews.find({}).sort("review_create_date", 1).skip(skipIndex).limit(limit))
    reviews = []
    for review in review_data:
        review['_id'] = str(review['_id'])
        reviews.append(review)
    return jsonify({'reviews': reviews})


@app.route('/review_save')
def review_save():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('review_save.html', id=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

@app.route('/reviews/<review_id>', methods=['GET'])
def detail_reviews(review_id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        review = db.reviews.find_one({'_id': ObjectId(review_id)})
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('review_detail.html', review=review, user=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/review_update/<id_data>')
def review_update(id_data):
    author_info = db.reviews.find_one({"_id": ObjectId(id_data)})
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        if author_info['author'] == payload['id']:
            return render_template('review_update.html', id=payload['id'], data=author_info)
        else:
            return redirect("/reviews/" + id_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/api/reviews', methods=['POST'])
def save_reviews():
    title = request.form['title_give']
    content = request.form['content_give']
    file = request.files["file_give"]

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.user.find_one({"id": payload['id']})

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/img/{filename}.{extension}'

    file.save(save_to)

    doc = {
        'review_title': title,
        'review_content': content,
        'review_file': f'{filename}.{extension}',
        'review_create_date': today.strftime('%Y.%m.%d.%H.%M.%S'),
        'author': user_info['id']

    }

    db.reviews.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@ app.route('/api/reviews', methods=['PUT'])
def update_reviews():
    title = request.form['title_give']
    content = request.form['content_give']
    file_id = request.form['id_give']
    file = request.files.get("file_give")

    today = datetime.now()

    doc = {
        'review_title': title,
        'review_content': content,
        'review_modified_date': today.strftime('%Y.%m.%d.%H.%M.%S'),
    }

    if file is not None:
        extension = file.filename.split('.')[-1]
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'
        save_to = f'static/img/{filename}.{extension}'
        file.save(save_to)
        doc['review_file'] = f'{filename}.{extension}'

    db.reviews.update_one({'_id': ObjectId(file_id)}, {'$set': doc})

    return jsonify({'msg': '수정 완료!'})


@ app.route('/api/reviews', methods=['DELETE'])
def delete_reviews():

    file_id = request.args.get("id_give")

    db.reviews.delete_one({'_id': ObjectId(file_id)})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
