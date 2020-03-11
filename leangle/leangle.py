from typing import Callable

from chalice.deploy.swagger import SwaggerGenerator

from .chalice_patches import generate_swagger, _generate_route_method


SwaggerGenerator.generate_swagger = generate_swagger
SwaggerGenerator._generate_route_method = _generate_route_method


def describe_response(status_code: str, **kwargs: str) -> Callable:
    """Decorator to describe a route's responses.

    Example:
        import leangle


        @app.route('/', methods=['POST'])
        @leangle.describe_response(201, description='Created')
        def index():
            return Response(status_code=201)

    """
    def annotate_function(func: Callable) -> Callable:
        # Ensure function has patched attribute
        func._leangle_responses = getattr(func, '_leangle_responses', {})
        func._leangle_responses[status_code] = kwargs

        if not kwargs.get('schema'):
            kwargs['schema'] = {'$ref': '#/definitions/Empty'}

        # Transform schema name into reference
        else:
            schema_name = kwargs['schema']
            kwargs['schema'] = {'$ref': f'#/definitions/{schema_name}'}

        return func

    return annotate_function


_leangle_schemas = {}


def add_schema(name):
    """Add a model to chalice from a schema.

    Example:
        import leangle


        @leangle.add_schema('PetSchema')
        PetSchema(Schema):
            name = fields.Str()

    """
    def wrapper(func):
        _leangle_schemas[name] = func
        return func

    return wrapper
