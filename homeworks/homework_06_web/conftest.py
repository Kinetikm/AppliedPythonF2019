import pytest
from sqlalchemy import create_engine

from auth.application import app, routes
from models.model import Base


@pytest.fixture()
def auth_test_client():

    app.config['DATABASE'] = app.config['TEST_DATABASE']
    testing_client = app.test_client(use_cookies=True)
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture()
def auth_init_database():
    engine = create_engine(app.config['DATABASE'])
    Base.metadata.create_all(engine)

    yield auth_init_database
    Base.metadata.drop_all(engine)
    pass
