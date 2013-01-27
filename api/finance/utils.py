from datetime import timedelta
from functools import wraps, update_wrapper

from flask import current_app, jsonify, make_response, request, session

def check_auth(username, password):
    """Check is username password combination is valid"""
    from models import User
    u = User.query.filter(User.username == username).first()
    if u is not None and u.check_password(password):
        return True
    return False

def authenticate():
    """Sends 401 response that enables basic auth"""
    message = {'message': 'Authenticate.'}
    res = jsonify(message)
    res.status_code = 401
    res.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return res

def requires_auth(f):
    """Checks whether user is logged in or raises error 401

    User able to have been logged in already and have session variable
    Or user is passing in authorization information
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if request.method != 'OPTIONS':
            auth = request.authorization
            if (not auth or not check_auth(auth.username, auth.password)) and 'logged_in' not in session:
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
        "{url}/<{pk_type}:{pk}>".format(url=url, pk_type=pk_type, pk=pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
                resp.status_code = 204
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers

            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator