from flask import current_app
import sqlite3
from timeboard_service.utils.exception import ApiException


def get_info(_id, stat_type):
    curs = None
    res = None

    try:
        curs = sqlite3.connect(current_app.config["DATABASE"])

        if stat_type == 1:
            res = curs.execute("SELECT AVG(time) avg_time FROM statistic WHERE req_type=(?) GROUP BY req_type",
                               (_id,)).fetchone()
        elif stat_type == 2:
            res = curs.execute("SELECT MIN(time) min_time FROM statistic WHERE req_type=(?) GROUP BY req_type",
                               (_id,)).fetchone()
        elif stat_type == 3:
            res = curs.execute("SELECT COUNT(*) count FROM statistic WHERE req_type=(?) GROUP BY req_type",
                               (_id,)).fetchone()
        else:
            res = curs.execute("SELECT id, time FROM "
                               "(SELECT id, time, PERCENT_RANK() OVER(ORDER BY time) LengthPercentRank FROM statistic "
                               "WHERE req_type=(?)) WHERE LengthPercentRank <= 0.10",
                               (_id,)).fetchall()

    except Exception as e:
        raise ApiException(500, "Database error", str(e))
    finally:
        if curs:
            curs.close()

    if res is None:
        raise ApiException(404, "Bad req_type parameter", "Such req_type doesnt exist")

    return res
