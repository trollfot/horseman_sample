import cgi
import typing
import horseman.parsing
from roughrider.routing.components import RoutingRequest


class ContentType(typing.NamedTuple):
    raw: str
    mimetype: str
    options: dict


class Request(RoutingRequest):

    __slots__ = (
        '_data'
        'app',
        'content_type',
        'environ',
        'method',
        'route',
    )

    def __init__(self, app, environ, route):
        self._data = ...
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
        if self._data is not ...:
            return self.get_data()

        if content_type := self.content_type:
            self.set_data(horseman.parsing.parse(
                self.environ['wsgi.input'], content_type.raw))

        return self.get_data()
