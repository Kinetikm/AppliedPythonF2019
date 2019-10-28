#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, abort
from multiprocessing import Manager, Process
import requests
from requests.exceptions import ConnectionError
import random
import logging

from statistic_loader import ProcessManager


app = Flask(__name__)
checked_queue = Manager().Queue()


@app.route("/callme", methods=['POST'])
def callme():
    data = request.json
    if data is None:
        return "Content type error"
    host = data.get("ip", None)
    port = data.get("port", None)
    app.logger.info("Got request from {}:{}".format(host, port))
    if host and port:
        try:
            resp = requests.get("http://{}:{}/check".format(host, port))
        except ConnectionError as ex:
            app.logger.error("Connection error to {}:{}/check".format(host, port))
            abort(500)
        if resp.status_code == 200:
            app.logger.info("Start processing for {}:{}".format(host, port))
            checked_queue.put("{}:{}".format(host, port))
        else:
            app.logger.warning("Reponse error for {}:{} with code {}".format(host, port, resp.status_code))
            abort(resp.status_code)
        return "Nice"
    abort(500)


if __name__ == "__main__":
    logging.basicConfig(filename='simple_flask.log', format='%(asctime)s.%(msecs)05d %(levelname)s [%(process)d] '
                                                            '%(module)s.%(funcName)s:%(lineno)d %(message)s',
                        level=logging.DEBUG)
    process_manager = ProcessManager(checked_queue, 7, app.logger)
    process_manager.start()
    app.run(host="0.0.0.0", port="8070", debug=True)
