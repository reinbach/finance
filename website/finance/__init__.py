import os

from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware, wrap_file

class Website(object):

    def dispatch_request(self, environ, request):
        filename = request.path if request.path != "/" else "index.html"
        try:
            fp = open('app/%s' % filename, 'rb')
        except IOError:
            raise NotFound()
        return Response(wrap_file(environ, fp), mimetype='text/html')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(environ, request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(with_static=True):
    app = Website()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app, {
                '/css': os.path.join(os.path.dirname(__file__), 'app/css'),
                '/img': os.path.join(os.path.dirname(__file__), 'app/img'),
                '/js': os.path.join(os.path.dirname(__file__), 'app/js'),
                '/lib': os.path.join(os.path.dirname(__file__), 'app/lib'),
            }
        )
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=True)