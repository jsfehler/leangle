from typing import Callable, List


def parameter(**kwargs: str) -> Callable:
    """Decorator to describe a route's parameters.

    Example:
        import leangle


        @app.route('/', methods=['POST'])
        @leangle.describe.parameter(name='body',
                                    description='Create a new object',
                                    required=True)
        def index():
            return Response(status_code=201)

    """
    def annotate_function(func: Callable) -> Callable:
        # Ensure function has patched attribute
        func._leangle_parameters = getattr(func, '_leangle_parameters', [])
        func._leangle_parameters.append(kwargs)

        if kwargs.get('_in'):
            kwargs['in'] = kwargs.get('_in')
            kwargs.pop('_in')

        # Transform schema name into reference
        if kwargs.get('schema'):
            schema_name = kwargs['schema']
            kwargs['schema'] = {'$ref': f'#/definitions/{schema_name}'}

        return func

    return annotate_function


def response(status_code: str, **kwargs: str) -> Callable:
    """Decorator to describe a route's responses.

    Example:
        import leangle


        @app.route('/', methods=['POST'])
        @leangle.describe.response(201, description='Created')
        def index():
            return Response(status_code=201)

    """
    def annotate_function(func: Callable) -> Callable:
        # Ensure function has patched attribute
        func._leangle_responses = getattr(func, '_leangle_responses', {})
        func._leangle_responses[status_code] = kwargs

        # Transform schema name into reference
        if kwargs.get('schema'):
            schema_name = kwargs['schema']
            kwargs['schema'] = {'$ref': f'#/definitions/{schema_name}'}

        return func

    return annotate_function


def tags(tag_list: List[str]) -> Callable:
    def annotate_function(func: Callable) -> Callable:
        func._leangle_tags = tag_list

        return func

    return annotate_function
