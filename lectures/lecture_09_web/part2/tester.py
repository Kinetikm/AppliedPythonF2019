import logging
import random

import aiohttp
from aiohttp import web

log = logging.getLogger('app')
log.setLevel(logging.INFO)
f = logging.Formatter(
    '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setFormatter(f)
log.addHandler(ch)

routes = web.RouteTableDef()


@routes.post('/callme')
async def hello(request: web.Request):
    try:
        data = await request.json()
        host = data.get('host')
        port = int(data.get('port'))
        api_method = data.get('api_method')
        student_lastname = data.get('student_lastname')
        if host is None or port is None or api_method is None:
            raise Exception
    except Exception as e:
        return web.json_response({'error': f'User err: {str(e)}'}, status=400)

    username = f'terebonka{random.randint(0, 100)}'
    age = random.randint(18, 100)
    sale = round(age / 7)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f'http://{host}:{port}/registration',
                                    json={'username': username, 'age': age}) as response:
                token = (await response.json())['token']
        except Exception as e:
            return web.json_response({'error': f'Request err: {str(e)}'}, status=403)

        try:
            async with session.post(f'http://{host}:{port}/login', json={'token': token}) as response:
                pass
        except Exception as e:
            return web.json_response({'error': f'Login err: {str(e)}'}, status=404)

        try:
            async with session.get(f'http://{host}:{port}/{api_method}') as response:
                answer = await response.json()
        except Exception as e:
            return web.json_response({'error': f'Server err: {str(e)}'}, status=418)

        if username == answer.get('username') and age == answer.get('age') and sale == answer.get('sale'):
            with open('amazing_students.txt', 'a') as f:
                f.write(f'{student_lastname}\n')
            return web.json_response({'success': f'You are amazing, {student_lastname}!'})
        else:
            return web.json_response({
                'error': f'Almost done, but nope. Should be username: {username}, age: {age}, sale: {sale}. '
                         f'Response: {answer}'},
                status=426)


app = web.Application(logger=log)
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8081)
