from flask import Flask

app = Flask(__name__)

# export FLASK_ENV=development
# export FLASK_APP=server.py
# flask run --host=127.0.0.1


@app.route('/user_info/<user_id>/')
def user_info_handler(user_id):
    return f'user_info_handler: str:{isinstance(user_id, str)} -> {user_id}'


@app.route('/user_info_int/<int:user_id>/')
def user_info_int_handler(user_id):
    return f'user_info_int_handler: int:{isinstance(user_id, int)} -> {user_id}'


@app.route('/user_info_two/<int:user_id1>/<int:user_id2>/')
def user_info_two_handler(user_id1, user_id2):
    return f"user_info_two_handler: {','.join(map(str, (user_id1, user_id2)))}"
