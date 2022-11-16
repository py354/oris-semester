import config
from app import app
from .models.database import DataBase
from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

db = DataBase.instance(config.DATABASE_URI)


@app.route('/')
def index():
    return "Hello world"


@app.route('/items/', methods=['POST', 'GET'])
@app.route('/items/<server>/')
def get_items(server=None):
    if server:
        return jsonify(db.get_items(server))
    elif request.method == 'GET':
        return jsonify(db.get_items())

    data = request.json
    if 'ids' in data and type(data['ids']) is list:
        result = []
        for item_id in data['ids']:
            rows = db.get_item(item_id)
            if len(rows) == 1:
                result.append(rows[0])
        return jsonify(result)
    return jsonify([])


@app.route("/auth/", methods=['POST'])
def auth():
    data = request.json
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'result': 'bad'})

    if len(data['login']) not in range(6, 20) or len(data['password']) not in range(6, 100):
        return jsonify({'result': 'bad'})

    users = db.get_users_with_login(data['login'])
    if len(users) != 1:
        return jsonify({'result': 'not_found'})

    user = users[0]
    if not check_password_hash(user['password'], data['password']):
        return jsonify({'result': 'not_found'})

    session.permanent = True
    session['id'] = user['id']
    return jsonify({'result': 'ok', 'data': {'id': user['login']}})


@app.route("/registration/", methods=['POST'])
def registration():
    data = request.json
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'result': 'bad'})

    if len(data['login']) not in range(6, 20) or len(data['password']) not in range(6, 100):
        return jsonify({'result': 'bad'})

    users = db.get_users_with_login(data['login'])
    if len(users) > 0:
        return jsonify({'result': 'already_exist'})

    db.create_user(data['login'], generate_password_hash(data['password']))
    users = db.get_users_with_login(data['login'])
    if len(users) != 1:
        return jsonify({'result': 'problems'})

    user = users[0]
    session.permanent = True
    session['id'] = user['id']
    return jsonify({'result': 'ok', 'data': {'id': user['login']}})


@app.route("/get_account_info/")
def get_account_info():
    if 'id' in session:
        users = db.get_users_with_id(session['id'])
        if len(users) == 1:
            user = users[0]
            return jsonify({'result': 'ok', 'data': {
                'login': user['login'],
                'cart': user['cart'],
                'email': user['email'],
                'is_admin': user['isadmin'],
                'photo_filename': user['photofilename'],
            }})

    return jsonify({'result': 'bad'})


@app.route("/delete_item/", methods=['POST'])
def delete_item():
    data = request.json
    if not data or 'item_id' not in data or 'id' not in session:
        return jsonify({'result': 'bad'})

    users = db.get_users_with_id(session['id'])
    if len(users) != 1 or not users[0]['isadmin']:
        return jsonify({'result': 'bad'})

    db.delete_item(data['item_id'])
    return jsonify({'result': 'ok'})


@app.route("/add_item/", methods=['POST'])
def add_item():
    data = request.json
    if not data or 'id' not in session:
        return jsonify({'result': 'bad'})

    for prop in ['server', 'name', 'desc', 'price', 'photo']:
        if prop not in data:
            return jsonify({'result': 'bad'})

    users = db.get_users_with_id(session['id'])
    if len(users) != 1 or not users[0]['isadmin'] or not data['price'].isnumeric():
        return jsonify({'result': 'bad'})

    db.add_item(data['name'], data['desc'], data['server'], int(data['price']), data['photo'])
    return jsonify({'result': 'ok'})




