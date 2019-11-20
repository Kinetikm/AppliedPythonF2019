from create_auth_db import app, db, jsonify, request, Cookies
import re
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

# NOTE: This is just a basic example of how to enable cookies. This is
#       vulnerable to CSRF attacks, and should not be used as is. See
#       csrf_protection_with_cookies.py for a more complete example!


app.config['JWT_TOKEN_LOCATION'] = ['cookies']

app.config['JWT_ACCESS_COOKIE_PATH'] = '/'

app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this!

jwt = JWTManager(app)

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


@app.route('/registration', methods=['POST'])
def register():
    email = request.json.get('email', None)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    password_conf = request.json.get('password_conf', None)
    if password != password_conf:
        return 'Passwords dont match', 400
    if not (re.search(regex, email)):
        return 'Wrong email format', 400
    if db.session.query(Cookies).filter(Cookies.username == username).count() != 0:
            return 'Username already exists', 400
    data = {
        'email': email,
        'username': username,
        'password': password
        }
    user = Cookies(**data, cookie='')
    db.session.add(user)
    db.session.commit()
    return 'Registration successful', 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if db.session.query(Cookies).filter(Cookies.username == username).filter(Cookies.password == password).count() == 1:
        access_token = create_access_token(identity=username)
        db.session.query(Cookies).filter(Cookies.username == username).update({"cookie": str(access_token)})
        db.session.commit()
        resp = jsonify('login successful')
        set_access_cookies(resp, access_token)
        return resp, 200
    return 'incorrect login or password', 401


@app.route('/logout', methods=['GET'])
@jwt_required
def logout():
    resp = jsonify('logged out')
    username = get_jwt_identity()
    db.session.query(Cookies).filter(Cookies.username == username).update({"cookie": ""})
    db.session.commit()
    unset_jwt_cookies(resp)
    return resp, 200


@app.route('/check', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return username, 200


if __name__ == '__main__':
    app.run(port=8000)
