import re
import logging
from logging.handlers import RotatingFileHandler

import requests

from flask import Flask, jsonify, request, session


app = Flask(__name__)


def get_github_user(username, auth=None):
    url = "https://api.github.com/users/%s" % username
    auth = auth if auth else {}
    try:
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError) as err:
        app.logger.error(err.response.text)
        return
    user = {}
    user['name'] = resp.json().get('name')
    user['email'] = resp.json().get('email')
    user['location'] = resp.json().get('location')
    user['repos'] = resp.json().get('public_repos')
    return user


def get_github_followers(username, auth=None):
    url = "https://api.github.com/users/%s/followers" % username
    auth = auth if auth else {}

    if 'page' in request.args:
        url += "?page=%s" % request.args.get('page')

    try:
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError) as err:
        app.logger.error(err.response.text)
        return

    followers = []
    for follower in resp.json():
        user = get_github_user(follower.get('login'), auth)
        followers.append(user)

    return {'data': followers, 'link': resp.headers.get('Link')}


def jsonify_followers(followers, user):
    resp = jsonify(followers['data'])
    try:
        link = re.sub('https://api.github.com.user/\d+/',
                      '%sapi/v1/%s/' % (request.url_root, user),
                      followers['link'])
    except TypeError:
        app.logger.error("no 'Link' header")
    else:
        resp.headers.add('Link', link)

    return resp


@app.route('/api/v1/followers', methods=['GET'])
def get_followers():
    if 'auth' not in session:
        return None

    auth = session['auth']
    user = auth[0]
    followers = get_github_followers(user, auth)

    return jsonify_followers(followers, user)


@app.route('/api/v1/<string:user>/followers', methods=['GET'])
def get_user_followers(user):
    if 'auth' in session:
        auth = session['auth']
        followers = get_github_followers(user, auth)
    else:
        followers = get_github_followers(user)

    return jsonify_followers(followers, user)


@app.route('/api/v1/newpr/<string:owner>/<string:repo>', methods=['POST'])
def create_pr(owner, repo):
    url = "https://api.github.com/repos/%s/%s/pulls" % (owner, repo)
    data = request.form.to_dict()
    try:
        r = requests.post(url, data=data)
        r.raise_for_status()
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError) as err:
        app.logger.error(err.response.text)
        return jsonify({'error': err.response.text})
    return jsonify(r.text)


@app.route('/api/v1/login', methods=['GET'])
def github_login():
    url = "https://api.github.com/user"
    auth = (request.authorization.get('username'),
            request.authorization.get('password'))
    try:
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError) as err:
        app.logger.error(err.response.text)
        return jsonify({'error': err.response.text})
    if resp.status_code == 200:
        session['auth'] = auth
    return jsonify(resp.json())


if __name__ == '__main__':
    handler = RotatingFileHandler('api.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
