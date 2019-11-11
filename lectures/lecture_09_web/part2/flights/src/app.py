import logging

from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/flights')
async def hello(request):
    return web.Response(text="Hello, world")


log = logging.getLogger('app')
log.setLevel(logging.INFO)
f = logging.Formatter(
    '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setFormatter(f)
log.addHandler(ch)


app = web.Application(logger=log)
app.add_routes(routes)
