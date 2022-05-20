from os import path
from pathlib import Path

from framework.content_types import CONTENT_TYPES_MAP
from framework.requests import Get, Post


class PageNotFound:
    def __call__(self, request):
        return '404 error', '404 Page not found'


class Framework:

    def __init__(self, route_obj):
        self.route_list = route_obj
        self.types_map = CONTENT_TYPES_MAP
        self.static_url = '/static/'
        self.static_dir = path.join(Path(__file__).resolve().parent.parent,
                                    'staticfiles')

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        request = {
            'method': environ['REQUEST_METHOD']
        }
        # print(environ)
        if not path.endswith('/'):
            path = f'{path}/'

        if environ['REQUEST_METHOD'] == 'POST' and environ['CONTENT_LENGTH']:
            request_params = Post(environ)
            request_params.get_params()
            request['data'] = request_params.result
            request_params.decode_result()
            print(request_params.decoded_result)

        if environ['REQUEST_METHOD'] == 'GET' and environ['QUERY_STRING']:
            request_params = Get(environ)
            request_params.get_params()
            request['request_params'] = request_params.result
            print(request_params.result)

        if path in self.route_list:
            view = self.route_list[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path.startswith(self.static_url):
            file_path = path[len(self.static_url):len(path)-1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(file_path)
        else:
            view = PageNotFound()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        start_response(code, [('Content-Type', content_type)])
        return [body]

    def get_content_type(self, file_path):

        file_name = path.basename(file_path).lower()
        extension = path.splitext(file_name)[1]
        return self.types_map.get(extension, 'text/html')

    def get_static(self, file_path):

        path_to_file = path.join(self.static_dir, file_path)
        with open(path_to_file, 'rb') as file:
            content = file.read()
        status = '200 Ok'
        return status, content
