import json

from config import Config
from bottle import route, run, static_file, request, redirect, response
from urllib import parse, request as urllib_request
import os
import logging

__COOKIE_SECRET_KEY = Config['appClientId'] + ':' + Config['appClientSecret']

logging.basicConfig(
    level=logging.DEBUG
)


def coding_host():
    if not Config['isEnterprise']:
        return 'https://coding.net'
    return 'https://%s.coding.net' % Config['enterpriseName']


def build_auth_url(redirect_url):
    callback_url = Config['callback']
    if redirect_url:
        callback_url += '/redirect/' + parse.quote(parse.quote(redirect_url))
    url = coding_host() + '/oauth_authorize.html?client_id=%s&redirect_uri=%s&response_type=code&scope=user' % (
        Config['appClientId'],
        callback_url
    )
    return url


def with_login():
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = request.get_cookie("account", secret=__COOKIE_SECRET_KEY)
            if not name:
                redirect('/login?redirect=' + parse.quote(request.url))
                return
            logging.debug(name + ' visited')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def user_info_by_code(code):
    if not code:
        return None
    request_url = coding_host()
    request_url += '/api/oauth/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&code=%s' % (
        Config['appClientId'],
        Config['appClientSecret'],
        code,
    )
    logging.debug(request_url)
    try:
        res = urllib_request.urlopen(request_url)
        content = res.read()
        logging.debug(content)
        json_content = json.loads(content)
        access_token = json_content['access_token']
        request_url = coding_host() + '/api/current_user?access_token=' + access_token
        logging.debug(request_url)
        res = urllib_request.urlopen(request_url)
        content = res.read()
        logging.debug(content)
        json_content = json.loads(content)
        assert json_content['code'] == 0
        return json_content['data']
    except Exception as e:
        logging.info(e)
    return None


@route('/login')
def login():
    redirect_url = request.query.redirect
    redirect(build_auth_url(redirect_url))


@route('/should_login')
def should_login():
    name = request.get_cookie("account", secret=__COOKIE_SECRET_KEY)
    logging.debug(name)
    if name:
        return 'already here ' + name
    login()


@route('/login/callback')
def login_callback():
    return login_callback_redirect(None)


@route('/login/callback/redirect/<path:path>')
def login_callback_redirect(path):
    user_info = user_info_by_code(request.query.code)
    if user_info and isinstance(user_info, dict) and 'name' in user_info and user_info['name']:
        response.set_cookie("account",
                            user_info['name'],
                            secret=__COOKIE_SECRET_KEY,
                            max_age=86400,
                            path='/')
        if not path:
            return 'login succeed'
        logging.debug(path)
        redirect(path)
        return
    return 'login failed'


@route('/<path:path>')
@with_login()
def static_all(path):
    full_path = os.path.join(Config['staticRoot'], path)
    if os.path.isdir(full_path):  # try file
        path = os.path.join(path, 'index.html')
    return static_file(path, Config['staticRoot'])


run(host='0.0.0.0', server='auto', port=Config['port'])
