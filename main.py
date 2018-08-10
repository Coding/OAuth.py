from config import Config
from bottle import route, run, static_file, request, redirect
from urllib import parse

__COOKIE_SECRET_KEY = Config['appSecretId'] + ':' + Config['appSecretKey']


def with_login():
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = request.get_cookie("account", secret=__COOKIE_SECRET_KEY)
            if not name:
                redirect('/login?redirect=' + parse.urlencode(request.url))
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


@route('/login')
def login():
    name = request.get_cookie("account", secret=__COOKIE_SECRET_KEY)
    if name:
        pass
    pass


@route('/login/callback')
def login_succeed():
    pass


@route('/<path:path>')
def static_all(path):
    return static_file(path, Config['staticRoot'])


run(debug=True)
