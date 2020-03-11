import copy
import inspect
from typing import Any, Dict, Optional

from chalice.app import Chalice, RouteEntry  # noqa
from chalice.deploy.models import RestAPI  # noqa

from leangle.leangle import _leangle_schemas

from marshmallow_jsonschema import JSONSchema


def generate_swagger(self, app, rest_api=None):
    """Monkey Patch SwaggerGenerator.generate_swagger."""
    # type: (Chalice, Optional[RestAPI]) -> Dict[str, Any]
    api = copy.deepcopy(self._BASE_TEMPLATE)
    api['info']['title'] = app.app_name
    self._add_binary_types(api, app)
    self._add_route_paths(api, app)
    self._add_resource_policy(api, rest_api)
    self._add_validators(api, app)
    self._add_model_definitions(api, rest_api)
    _add_leangle_schemas(api)
    return api


def _add_leangle_schemas(api: Dict):
    """Add schema dumps to the API."""
    for name, schema in _leangle_schemas.items():
        api['definitions'][name] = JSONSchema().dump(schema)


def _generate_route_method(self, view: RouteEntry) -> Dict[str, Any]:
    """Monkey Patch SwaggerGenerator._generate_route_method."""
    responses = getattr(
        view.view_function,
        '_leangle_responses',
        self._generate_precanned_responses(),
    )

    current = {
        'consumes': view.content_types,
        'produces': ['application/json'],
        'responses': responses,
        'x-amazon-apigateway-integration': self._generate_apig_integ(view),
    }  # type: Dict[str, Any]
    docstring = inspect.getdoc(view.view_function)
    if docstring:
        doc_lines = docstring.splitlines()
        current['summary'] = doc_lines[0]
        if len(doc_lines) > 1:
            current['description'] = '\n'.join(doc_lines[1:]).strip('\n')
    if view.api_key_required:
        # When this happens we also have to add the relevant portions
        # to the security definitions.  We have to someone indicate
        # this because this neeeds to be added to the global config
        # file.
        current.setdefault('security', []).append({'api_key': []})
    if view.authorizer:
        current.setdefault('security', []).append(
            {view.authorizer.name: []})
    if view.view_args:
        self._add_view_args(current, view.view_args)
    return current
