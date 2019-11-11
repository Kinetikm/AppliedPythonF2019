from aiohttp import web

from app import app, log


def main():
    log.info("Start flights aplication")
    web.run_app(app, host='0.0.0.0', port=8000, access_log=log)


if __name__ == "__main__":
    main()
