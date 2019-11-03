from flask import Blueprint, jsonify
from timeboard_service.service import statistic as st


bp = Blueprint("statistic", __name__, url_prefix='/statistic')


@bp.route("/average/<int:_id>", methods=['GET'])
def average_time(_id):
    res = st.get_info(_id, 1)

    return jsonify({'statistic': round(res[0], 3)})


@bp.route("/min/<int:_id>", methods=['GET'])
def min_time(_id):
    res = st.get_info(_id, 2)

    return jsonify({'statistic': round(res[0], 3)})


@bp.route("/count/<int:_id>", methods=['GET'])
def count(_id):
    res = st.get_info(_id, 3)

    return jsonify({'statistic': round(res[0], 3)})


@bp.route("/percentile/<int:_id>", methods=['GET'])
def percentile(_id):
    res = st.get_info(_id, 4)

    data = []
    if len(res):
        data = [{'id': re[0], 'time': re[1]} for re in res]

    return jsonify({'statistic': data})
