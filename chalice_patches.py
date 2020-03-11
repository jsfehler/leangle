import inspect
from typing import Any, Dict

from chalice.app import RouteEntry  # noqa


def _generate_route_method(self, view: RouteEntry) -> Dict[str, Any]:
    """Monkey Patch SwaggerGenerator._generate_route_method"""

    responses = getattr(
        view.view_function,
        '_leangle_responses',
        self._generate_precanned_responses(),
    )

    current = {
        'consumes': view.content_types,
        'produces': ['application/json'],
        'responses': responses,
        'x-amazon-apigateway-integration': self._generate_apig_integ(
            view),
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
