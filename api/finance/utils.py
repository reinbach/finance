from flask import abort, g

def user_required(f):
    """Checks whether user is logged in or raises error 401"""
    def decorator(*args, **kwargs):
        if not hasattr(g, 'user') or not g.user:
            abort(401)
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