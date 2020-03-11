import inspect
from typing import Any, Dict, Optional

from chalice.app import Chalice, RouteEntry  # noqa
from chalice.deploy.swagger import SwaggerGenerator
from chalice.deploy.models import RestAPI  # noqa

from leangle.leangle import _leangle_schemas

from marshmallow_jsonschema import JSONSchema


original_generate_swagger = SwaggerGenerator.generate_swagger


def patch_generate_swagger():
    """Monkey Patch SwaggerGenerator.generate_swagger."""
    def generate_swagger(self,
                         app: Chalice,
                         rest_api: Optional[RestAPI] = None) -> Dict[str, Any]:
        api: Dict[str, Any] = original_generate_swagger(app, rest_api)
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

    current: Dict[str, Any] = {
        'consumes': view.content_types,
        'produces': ['application/json'],
        'responses': responses,
        'x-amazon-apigateway-integration': self._generate_apig_integ(view),
    }
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
