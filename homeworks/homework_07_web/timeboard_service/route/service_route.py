from flask import Blueprint, request, jsonify, g
from timeboard_service.service import service as sv

bp = Blueprint("service", __name__, url_prefix='/service')


@bp.route("/rows", methods=['GET', 'POST'])
def handle_flights():
    if request.method == 'GET':
        offset = request.args.get('offset', type=int)
        limit = request.args.get('limit', type=int)
        dep_time = request.args.get('dep_time', type=str)

        data = sv.show_all(offset, limit, dep_time)
        g.req_type = 1
        return jsonify({"flights": data})
    else:
        body = request.json

        data = sv.add_flight(body)
        g.req_type = 2
        return jsonify({"inserted": data}), 201


@bp.route("/rows/<int:_id>", methods=['GET', 'PUT', 'DELETE'])
def handle_flight(_id):
    if request.method == 'GET':
        data = sv.show_flight(_id)
        g.req_type = 3
        return jsonify({"flight": data})
    elif request.method == 'PUT':
        body = request.json
        data = sv.update_flight(body, _id)
        g.req_type = 4
        return jsonify({"updated": data})
    else:
        sv.del_flight(_id)
        g.req_type = 5
        return jsonify({"success": True}), 204
