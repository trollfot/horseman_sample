import inspect
from dataclasses import dataclass, field
from functools import partial
from typing import Mapping, Optional, NamedTuple, Callable, Type

import autoroutes
import horseman.meta
import horseman.response
import horseman.http
import horseman.util

from sample.request import Request
from omegaconf.dictconfig import DictConfig


class Route(NamedTuple):
    path: str
    method: str
    endpoint: Callable
    params: dict
    extras: dict


def route_payload(view, methods: list=None):
    if inspect.isclass(view):
        inst = view()
        if isinstance(inst, horseman.meta.APIView):
            assert methods is None
            members = horseman.util.view_methods(inst)
            for name, func in members:
                yield name, func
        else:
            assert methods is not None
            for method in methods:
                yield method, inst.__call__
    else:
        if methods is None:
            methods = ['GET']
        for method in methods:
            yield method, view


@dataclass
class Application(horseman.meta.APINode):

    config: Mapping = field(default_factory=partial(DictConfig, {}))
    routes: autoroutes.Routes = field(default_factory=autoroutes.Routes)
    request_factory: Type[horseman.meta.Overhead] = Request

    def route(self, path: str, methods: list = None, **extras):
        def routing(view):
            for method, endpoint in route_payload(view, methods):
                self.routes.add(path, **{
                    method: endpoint,
                    'extras': extras
                })
            return view
        return routing

    def match(self, method: str, path_info: str) -> Route:
        methods, params = self.routes.match(path_info)
        if methods is None:
            return None
        endpoint = methods.get(method)
        if endpoint is None:
            raise HTTPError(HTTPStatus.METHOD_NOT_ALLOWED)
        return Route(
            path=path_info,
            method=method,
            endpoint=endpoint,
            params=params,
            extras=methods.get('extras', {})
        )

    def resolve(self, path: str, environ: dict):
        route = self.match(environ['REQUEST_METHOD'], path)
        if route is not None:
            environ['horseman.path.params'] = route.params
            request = self.request_factory(self, environ, route)
            return route.endpoint(request, **route.params)
        return None


app = Application()


@app.route('/')
def index(request: Request):
    return horseman.response.Response.create(200, body='Yeah')
