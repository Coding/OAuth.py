from config import Config
from bottle import route, run, static_file, request, redirect
from urllib import parse
import os

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
    full_path = os.path.join(Config['staticRoot'], path)
    if os.path.isdir(full_path): # try file
        path = os.path.join(path, 'index.html')
    return static_file(path, Config['staticRoot'])


run(debug=True, reloader=True)
