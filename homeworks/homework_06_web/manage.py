import logging
from flask_script import Manager
from flask import Flask
import app.firstmodule.controllers as firstmodule


app = Flask(__name__)
app.register_blueprint(firstmodule.module)
manager = Manager(app)

if __name__ == '__main__':
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('reqs.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)\
                                   s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    manager.run()
