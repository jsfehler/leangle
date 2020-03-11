from typing import Callable

from chalice.deploy.swagger import SwaggerGenerator

from .chalice_patches import _generate_route_method


SwaggerGenerator._generate_route_method = _generate_route_method


def describe_response(status_code: str, **kwargs: str) -> Callable:
    """Decorator to describe a route's responses.

    Example:
        from leangle import describe_response

        @app.route('/', methods=['POST'])
        @describe_response(201, description='Created')
        def index():
            return Response(status_code=201)

    """
    def annotate_function(func: Callable) -> Callable:
        # Ensure function has patched attribute
        func._leangle_responses = getattr(func, '_leangle_responses', {})
        func._leangle_responses[status_code] = kwargs

        return func

    return annotate_function
