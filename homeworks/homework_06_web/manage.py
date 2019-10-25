#!/usr/bin/env python
from flask_script import Manager
from app import create_app
import logging


app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)\
                                   s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("Program started")
    manager.run()
