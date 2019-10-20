from flask import Blueprint, abort, request, jsonify, current_app as app


admin_view = Blueprint('admin_view', __name__)


# DRY Проверяем заголовок только в одном месте
def check_admin(func):
    def wrapper(*args, **kwargs):
        if request.headers.get('Secret-Word') != 'Dratuti':
            abort(403)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_view.route('/all_users')
@check_admin
def all_users_wrap():
    return jsonify([user for user in app.config['MEMORY'].values()])


@admin_view.route('/all_tokens')
@check_admin
def all_tokens_wrap():
    return jsonify(list(app.config['MEMORY'].keys()))
