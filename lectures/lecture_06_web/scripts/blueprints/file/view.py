import os
import time

from flask import Blueprint, abort, request, jsonify, current_app as app

file_view = Blueprint('file_view', __name__)


# Загрузка файла
@file_view.route('/<token>', methods=['POST'])
def upload_file(token):
    if token not in app.config['MEMORY']:
        abort(404)

    if 'file' not in request.files or not request.files['file'].filename:
        abort(400)

    filename = token + str(time.time())
    request.files['file'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return '', 204


# Получение названия загруженных файлов пользователя
@file_view.route('/<token>', methods=['GET'])
def list_files(token):
    if token not in app.config['MEMORY']:
        abort(404)

    files = next(os.walk(app.config['UPLOAD_FOLDER']))[2]
    return jsonify([
        file for file in files if file.startswith(token)
    ])


# Удаление файла
@file_view.route('/<token>/<filename>', methods=['DELETE'])
def delete_file(token, filename):
    if token not in app.config['MEMORY']:
        abort(404)

    if not filename.startswith(token):
        abort(404)

    abs_path_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(abs_path_filename):
        abort(404)

    os.remove(abs_path_filename)
    return '', 204
