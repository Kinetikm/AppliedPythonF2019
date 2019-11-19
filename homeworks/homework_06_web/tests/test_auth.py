import json


def test_registration(auth_test_client, auth_init_database):
    resp = auth_test_client.post('/registration',
                                 data=json.dumps({'login': 'user1', 'email': 'user1@mail.ru', 'password': '123'}),
                                 content_type='application/json')
    assert resp.status_code == 200
    # user exist
    resp = auth_test_client.post('/registration',
                                 data=json.dumps({'login': 'user1', 'email': 'user1@mail.ru', 'password': '123'}),
                                 content_type='application/json')
    assert resp.status_code == 400
    # invalid email
    resp = auth_test_client.post('/registration',
                                 data=json.dumps({'login': 'user1', 'email': 'user1@mail', 'password': '123'}),
                                 content_type='application/json')
    assert resp.status_code == 400


def test_login(auth_test_client, auth_init_database):
    auth_test_client.post('/registration',
                          data=json.dumps({'login': 'user1', 'email': 'user1@mail.ru', 'password': '123'}),
                          content_type='application/json', )
    resp = auth_test_client.post('/login',
                                 data=json.dumps({'login': 'user1', 'password': '123'}),
                                 content_type='application/json')
    assert resp.status_code == 204
    assert resp.headers.getlist('Set-Cookie')
    # incorrect password
    resp = auth_test_client.post('/login',
                                 data=json.dumps({'login': 'user1', 'password': '13'}),
                                 content_type='application/json')
    assert resp.status_code == 401
    assert not resp.headers.getlist('Set-Cookie')


def test_about_me(auth_test_client, auth_init_database):
    email = 'user1@mail.ru'
    username = 'user1'
    auth_test_client.post('/registration',
                          data=json.dumps({'login': username, 'email': email, 'password': '123'}),
                          content_type='application/json', )
    resp = auth_test_client.post('/login',
                                 data=json.dumps({'login': 'user1', 'password': '123'}),
                                 content_type='application/json')
    cookies = resp.headers.get('Set-Cookie')
    resp = auth_test_client.get('/about_me', headers={'Cookie': cookies})
    data = json.loads(resp.data)
    assert data['email'] == email
    assert data['username'] == username
