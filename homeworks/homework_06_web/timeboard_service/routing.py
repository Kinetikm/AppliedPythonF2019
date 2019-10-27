from flask import Blueprint, request, jsonify, abort
import json
from timeboard_service.storage import get_fd
from timeboard_service.functions import show_all, show_flight, add_flight, update_flight, del_flight
from marshmallow import ValidationError

bp = Blueprint("api", __name__)


@bp.route("/rows", methods=['GET', 'POST'])
def handle_flights():
    fd = get_fd()
    data = json.loads(fd.read())

    if request.method == 'GET':
        offset = request.args.get('offset')
        count = request.args.get('count')
        dep_time = request.args.get('dep_time')

        data = show_all(data, offset, count, dep_time)
        return jsonify(data) if data is not None else abort(412, "Bad query params")
    elif request.method == 'POST':
        body = request.json
        try:
            data = add_flight(body, data)
        except ValidationError as e:
            abort(400, e.messages)
        fd.seek(0)
        json.dump(data, fd)
        return jsonify(data)
    else:
        abort(405, "Bad HTTP method")


@bp.route("/rows/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def handle_flight(id):
    fd = get_fd()
    data = json.loads(fd.read())

    if request.method == 'GET':
        data = show_flight(data, id)
        return jsonify(data) if data is not None else abort(404, "Invalid index")
    elif request.method == 'PUT' or request.method == 'DELETE':
        if request.method == 'PUT':
            body = request.json
            data = update_flight(body, data, id)
        elif request.method == 'DELETE':
            data = del_flight(data, id)

        fd.seek(0) if data is not None else abort(404, "Invalid index")
        fd.truncate(0)
        json.dump(data, fd)
        return jsonify(data)
    else:
        abort(405, "Bad HTTP method")
