import uuid

from flask import Blueprint, abort, request, jsonify, current_app as app


auth_view = Blueprint('auth_view', __name__)


# Обработка POST запроса
@auth_view.route('/', methods=['POST'])
def auth():
    content = request.json
    if not content:
        return abort(418)  # Я чайник

    # Валидация данных
    name, surname, age = content.get('name'), content.get('surname'), content.get('age')
    if not (name and surname and isinstance(age, int) or age >= 0):
        return abort(400)

    # Логгирование запроса
    app.logger.debug('Auth %s %s!', name, surname)

    token = str(uuid.uuid4())
    # Сохранение запроса
    app.config['MEMORY'][token] = {
        'name': name,
        'surname': surname,
        'age': age,
    }
    return jsonify({'token': token})


# Обработка PATCH запроса с параметром в URL
@auth_view.route('/<token>', methods=['PATCH'])
def update(token):
    if token not in app.config['MEMORY']:
        abort(404)  # Не найдено

    content = request.json
    if not content:
        return abort(418)  # Я чайник

    # Валидация данных
    name, surname, age = content.get('name'), content.get('surname'), content.get('age')
    if name == '' or surname == '' or not isinstance(age, int) or age < 0:
        return abort(400)

    # Логгирование запроса
    app.logger.debug('Update %s %s!', app.config['MEMORY'][token]['name'], app.config['MEMORY'][token]['surname'])

    # Сохранение запроса
    for field, value in content.items():
        if field in app.config['MEMORY'][token]:
            app.config['MEMORY'][token][field] = value

    return '', 204  # Ответ без контента


# Обработка GET запроса с параметром в URL
@auth_view.route('/<token>')
def info(token):
    if token not in app.config['MEMORY']:
        abort(404)
    return jsonify(app.config['MEMORY'][token])


# Обработка DELETE запроса с параметром в URL
@auth_view.route('/<token>', methods=['DELETE'])
def delete(token):
    if token not in app.config['MEMORY']:
        abort(404)
    del app.config['MEMORY'][token]
    return '', 204
