from functools import wraps

from flask import jsonify, request, session

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
        "{url}<{pk_type}:{pk}>".format(url=url, pk_type=pk_type, pk=pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )