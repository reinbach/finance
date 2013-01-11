from functools import wraps

from flask import jsonify, request

def check_auth(username, password):
    """Check is username password combination is valid"""
    #TODO change this to be more practical
    return username == "admin" and password == "secret"

def authenticate():
    """Sends 401 response that enables basic auth"""
    message = {'message': 'Authenticate.'}
    res = jsonify(message)
    res.status_code = 401
    res.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return res

def requires_auth(f):
    """Checks whether user is logged in or raises error 401"""
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorator

def register_api(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)

    app.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=['GET',]
    )
    app.add_url_rule(
        url,
        view_func=view_func,
        methods=['POST',]
    )
    app.add_url_rule(
        "{url}<{pk_type}:{pk}>".format(url=url, pk_type=pk_type, pk=pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )