from flask import Flask, request, jsonify, abort
from validator import validator
from flights import Flights
import datetime

app = Flask(__name__)

flights = Flights()


@app.route('/flights', methods=['GET'])
def get_flights():
    log_file = open('logs.txt', 'a')
    print("--------------------------------------", file=log_file)
    print("Request: GET, Time: ", datetime.datetime.now(), file=log_file)
    arg_dct = request.args
    fltr = {}
    if len(arg_dct) == 0:
        answ = flights.get()
        if len(answ) == 0:
            print("Method: GET, Time: ", datetime.datetime.now(), file
                  =log_file)
            print("Status: ", 400, ", Reason: ",
                  "Empty list of flights. Append something"
                  " before using get-method.",
                  file=log_file)
            log_file.close()
            abort(400,
                  "Empty list of flights. Append something"
                  " before using get-method.")
        print("Method: GET, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", 200, ", Reason: ", "OK", file=log_file)
        log_file.close()
        return jsonify(flights.get())
    for t in arg_dct.keys():
        if t in ['id', 'departure', 'arrival', 'flight_time', 'airport',
                 'plane']:
            fltr[t] = arg_dct.get(t)
    answ = flights.get(fltr)
    if len(answ) == 0:
        print("Method: GET, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", 404, ", Reason: ",
              f"Flight with current mask {arg_dct} not found."
              f" Try another mask.",
              file=log_file)
        log_file.close()
        abort(404,
              f'Flight with current mask {arg_dct} not found.'
              f' Try another mask.')
    print("Method: GET, Time: ", datetime.datetime.now(), file=log_file)
    print("Status: ", 200, ", Reason: ", "OK", file=log_file)
    log_file.close()
    return jsonify(answ)


@app.route('/flights', methods=['POST'])
def post_flight():
    log_file = open('logs.txt', 'a')
    print("--------------------------------------", file=log_file)
    print("Request: POST, Time: ", datetime.datetime.now(), file=log_file)
    arg_dct = request.json
    print(f"Args: {arg_dct}", datetime.datetime.now(), file=log_file)
    if len(arg_dct) == 0:
        print("Method: POST, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", 400, ", Reason: ", f"Bad args {arg_dct}", file
              =log_file)
        log_file.close()
        abort(400, f"Bad args {arg_dct}")
    res = validator('POST', arg_dct)
    if res[0] == 200:
        ans = flights.append(arg_dct)
        if ans == 1:
            print("Method: POST, Time: ", datetime.datetime.now(), file
                  =log_file)
            print("Status: ", 400, ", Reason: ", "Item already added", file
                  =log_file)
            log_file.close()
            abort(400, "Item already added")
    else:
        print("Method: POST, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", res[0], ", Reason: ", res[1], file=log_file)
        log_file.close()
        abort(res[0], res[1])
    print("Method: POST, Time: ", datetime.datetime.now(), file=log_file)
    print("Status: ", 200, ", Reason: ", "OK", file=log_file)
    log_file.close()
    return jsonify({"data": arg_dct})


@app.route('/flights/<int:flight_id>', methods=['PUT'])
def put_flight(flight_id):
    log_file = open('logs.txt', 'a')
    print("--------------------------------------", file=log_file)
    print("Request: PUT, Time: ", datetime.datetime.now(), file=log_file)
    arg_dct = request.json
    print(f"Args: {arg_dct}", datetime.datetime.now(), file=log_file)
    if len(arg_dct) == 0:
        print("Method: PUT, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", 400, ", Reason: ", f"Bad args {arg_dct}", file
              =log_file)
        log_file.close()
        abort(400, f"Bad args {arg_dct}")
    res = validator('PUT', arg_dct)
    if res[0] == 200:
        if arg_dct['id'] != flight_id:
            print("Method: PUT, Time: ", datetime.datetime.now(), file
                  =log_file)
            print("Status: ", 400, ", Reason: ", "Incorrect id", file=log_file)
            log_file.close()
            abort(400, "Incorrect id")
        ans = flights.update(arg_dct)
        if ans == 1:
            print("Method: PUT, Time: ", datetime.datetime.now(), file
                  =log_file)
            print("Status: ", 400, ", Reason: ", "Item already added", file
                  =log_file)
            log_file.close()
            abort(400, "Item already added")
    else:
        print("Method: PUT, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", res[0], ", Reason: ", res[1], file=log_file)
        log_file.close()
        abort(res[0], res[1])
    print("Method: POST, Time: ", datetime.datetime.now(), file=log_file)
    print("Status: ", 200, ", Reason: ", "OK", file=log_file)
    log_file.close()
    return jsonify({"data": arg_dct})


@app.route('/flights/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    log_file = open('logs.txt', 'a')
    print("--------------------------------------", file=log_file)
    print(f"Request: DELETE, id: {flight_id}, Time: ", datetime.datetime.now(),
        file=log_file)
    ans = flights.pop(flight_id)
    if ans == 1:
        print(
            f"Method: DELETE, id: {flight_id}, Time: ",
            datetime.datetime.now(),
            file=log_file)
        print("Status: ", 400, ", Reason: ", "Bad id", file=log_file)
        log_file.close()
        abort(400, "Bad id")
    else:
        print("Method: DELETE, Time: ", datetime.datetime.now(), file=log_file)
        print("Status: ", 200, ", Reason: ", "OK", file=log_file)
        log_file.close()
        return jsonify({"data": ans})


if __name__ == "__main__":
    log_file = open('logs.txt', 'a')
    print("--------------------------------------", file=log_file)
    print("New session started: ", datetime.datetime.now(), file=log_file)
    print("--------------------------------------", file=log_file)
    log_file.close()
    app.run()
