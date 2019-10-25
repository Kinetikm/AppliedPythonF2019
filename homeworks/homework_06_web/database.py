import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='verepa40', host='localhost')
cursor = conn.cursor()


def format_in_dict(rec):
    new_view = {}
    new_view["Id"] = rec[0]
    new_view["Number"] = rec[1]
    new_view["Departure time"] = rec[2].strftime("%H:%M")
    new_view["Arrival time"] = rec[3].strftime("%H:%M")
    new_view["Flight time"] = rec[4].strftime("%H:%M")
    new_view["Destination airport"] = rec[5]
    new_view["Type of aircraft"] = rec[6]
    return new_view


def get_all_flight():
    cursor.execute("SELECT * FROM flight")
    records = cursor.fetchall()
    for i, rec in enumerate(records):
        records[i] = format_in_dict(rec)
    return records


def get_one_flight(id):
    cursor.execute(f"SELECT * FROM flight WHERE id='{id}'")
    result = cursor.fetchall()

    return format_in_dict(result[0]) if result else None


def add_flight(data):
    query = "SELECT * FROM flight WHERE id={} OR (name='{}' AND dept_time='{}' AND arr_time='{}' " \
            "AND travel_time='{}' AND airport='{}' AND type='{}')"
    cursor.execute(query.format(data['id'], data["name"], data["dept_time"], data["arr_time"],
                                data["travel_time"], data["airport"], data["type"]))

    result = cursor.fetchall()

    if result:
        return format_in_dict(result[0])
    else:
        query = "INSERT INTO flight(id, name, dept_time, arr_time, travel_time, airport, type) VALUES " \
                "({}, '{}', '{}', '{}', '{}', '{}', '{}')"
        cursor.execute(query.format(data["id"], data["name"], data["dept_time"], data["arr_time"],
                                    data["travel_time"], data["airport"], data["type"]))
        conn.commit()
        return "Post added"


def change_flight(id, data):
    query = "UPDATE flight SET name='{}', dept_time='{}', arr_time='{}'," \
            "travel_time='{}', airport='{}', type='{}' WHERE id={}"
    cursor.execute(query.format(data["name"], data["dept_time"], data["arr_time"],
                                data["travel_time"], data["airport"], data["type"], id))


def delete_flight(id):
    cursor.execute(f"DELETE FROM flight WHERE id={id}")
    conn.commit()