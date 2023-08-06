import flask
import json

from infosystem.common.subsystem import controller
from infosystem.common import exception


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    def restore(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            self.manager.restore(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")

    def reset(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            self.manager.reset(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")

    def routes(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        token = self.manager.api.tokens.get(
            id=flask.request.headers.get('token'))
        try:
            routes = self.manager.routes(user_id=token.user_id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {"routes": [route.to_dict() for route in routes]}

        return flask.Response(response=json.dumps(response, default=str),
                              status=200,
                              mimetype="application/json")
