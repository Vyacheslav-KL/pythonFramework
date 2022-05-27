from wsgiref.simple_server import make_server
from framework.main import Framework
from views import routes

app = Framework(routes)

with make_server('', 8080, app) as httpd:
    print('Launch on port 8080...')
    httpd.serve_forever()
