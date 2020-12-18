import cgi
import collections
import typing
import horseman.parsing
from horseman.meta import Overhead


class ContentType(typing.NamedTuple):
    raw: str
    mimetype: str
    options: dict


class Request(Overhead):

    __slots__ = (
        '_data'
        '_db',
        '_extracted',
        'app',
        'content_type',
        'environ',
        'method',
        'route',
    )

    def __init__(self, app, environ, route):
        self._data = {}
        self._db = None
        self._extracted = False
        self.app = app
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].upper()
        self.route = route
        if 'CONTENT_TYPE' in self.environ:
            ct = self.environ['CONTENT_TYPE']
            self.content_type = ContentType(ct, *cgi.parse_header(ct))
        else:
            self.content_type = None

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def extract(self):
        if self._extracted:
            return self.get_data()

        self._extracted = True
        if content_type := self.content_type:
            self.set_data(horseman.parsing.parse(
                self.environ['wsgi.input'], content_type.raw))

        return self.get_data()
