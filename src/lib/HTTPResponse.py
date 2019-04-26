# stdlib
import logging

# third party lib
from flask import jsonify, make_response
from requests import Request, Session

# internal lib
from lib.settings import ServerHTTP


def create_response(code, msg=None):
    """
    Convenience method for flask.make_response(flask.jsonify(msg), code)

    If no message is supplied, a generic message will be returned based on the code provided

    :param code:            The HTTP status code
    :param msg:             Any message to be included in the response
    """
    status = 'OK'
    if code is not 200:
        status = 'error'
    if msg is None:
        if code is 200:
            msg = 'success'
        elif code is 404:
            msg = 'Not found'
        elif code is 400:
            msg = 'User error; please check request'
        else:
            msg = 'Unknown error'
    envelope = {
        'status': status,
        'msg': msg
    }
    return make_response(jsonify(envelope), code)


def respond_to_server(path, verb, msg=None, client_name=None):
    url = f'http://{ServerHTTP.external_host}:{ServerHTTP.port}/{path}'
    # logging.info(f'Got request to respond to server at {url} by {verb}ing')

    s = Session()
    req = Request(method=verb, url=url, data=msg, params={'client_name': client_name})
    prepped = req.prepare()
    resp = s.send(prepped)
    # logging.info(resp.json())