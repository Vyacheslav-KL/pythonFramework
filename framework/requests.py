import quopri
import html


class Get:

    def __init__(self, environ):
        self.environ = environ['QUERY_STRING']
        self.result = {}

    def get_params(self):
        params = self.environ.split('&')
        self.result = {k: v for k, v in [i.split('=') for i in params]}


class Post:

    def __init__(self, environ):
        self.data = environ['wsgi.input']
        self.content_len = int(environ['CONTENT_LENGTH'])
        self.result = {}
        self.decoded_result = {}

    def get_params(self):
        data = self.data.read(self.content_len).decode(encoding='utf-8')
        params = data.split('&')
        self.result = {k: v for k, v in [i.split('=') for i in params]}

    def decode_result(self):
        for k, v in self.result.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            self.decoded_result[k] = html.unescape(
                quopri.decodestring(val).decode('utf-8'))
