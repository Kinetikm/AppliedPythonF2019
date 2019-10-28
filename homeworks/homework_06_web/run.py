#!flask/bin/python
import os
from flask_script import Manager
from logging.handlers import RotatingFileHandler
from app import create_app
import logging

app = create_app()
app_manager = Manager(app)


if __name__ == '__main__':
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        logger = logging.getLogger('app')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.info('App startup')
    app_manager.debug = True
    app_manager.run()
