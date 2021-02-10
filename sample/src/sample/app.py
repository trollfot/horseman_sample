from dataclasses import dataclass, field
from functools import partial
from typing import Mapping, Type

import horseman.meta
import horseman.response
import horseman.http

from sample.request import Request
from omegaconf.dictconfig import DictConfig
from roughrider.routing.route import Routes
from roughrider.routing.components import RoutingNode


@dataclass
class Application(RoutingNode):

    config: Mapping = field(default_factory=partial(DictConfig, {}))
    routes: Routes = field(default_factory=Routes)
    request_factory: Type[horseman.meta.Overhead] = Request

    def resolve(self, path: str, environ: dict):
        route = self.routes.match_method(path, environ['REQUEST_METHOD'])
        if route is not None:
            environ['horseman.path.params'] = route.params
            request = self.request_factory(self, environ, route)
            return route.endpoint(request, **route.params)


app = Application()


@app.route('/')
def index(request: Request):
    return horseman.response.Response.create(200, body='Yeah')
