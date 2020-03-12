from chalice import Chalice
from chalice.deploy.swagger import SwaggerGenerator

import leangle
from leangle.chalice_patches import _add_leangle_schemas

from marshmallow import Schema, fields


def test_chalice_swagger_generator_parameters():
    app = Chalice(app_name="leangle_tests")

    @app.route('/the_works')
    @leangle.describe.parameter(
        name='body',
        _in='body',
        description='Gimme all you got.',
        schema='TheWorksSchema',
    )
    @leangle.describe.response('201', description="All-dressed, baby.")
    def the_works():
        """Just do it."""
        return {"hello": "world"}

    swagger_gen = SwaggerGenerator(
        region='unit_test',
        deployed_resources={'api_handler_arn': '123456'},
    )
    swagger = swagger_gen.generate_swagger(app)

    expected = {
        'name': 'body',
        'description': 'Gimme all you got.',
        'schema': {
            '$ref': '#/definitions/TheWorksSchema',
        },
        'in': 'body',
    }

    assert swagger['paths']['/the_works']['get']['parameters'][0] == expected


def test_chalice_swagger_generator_response():
    app = Chalice(app_name="leangle_tests")

    @app.route('/the_works')
    @leangle.describe.parameter(
        name='body',
        _in='body',
        description='Gimme all you got.',
        schema='TheWorksSchema',
    )
    @leangle.describe.response('201', description="All-dressed, baby.")
    def the_works():
        """Just do it."""
        return {"hello": "world"}

    swagger_gen = SwaggerGenerator(
        region='unit_test',
        deployed_resources={'api_handler_arn': '123456'},
    )
    swagger = swagger_gen.generate_swagger(app)

    expected = {
        '201': {
            'description': 'All-dressed, baby.',
        },
    }

    assert swagger['paths']['/the_works']['get']['responses'] == expected


def test_add_leangle_schemas(request):

    def fin():
        leangle.leangle._leangle_schemas = {}

    request.addfinalizer(fin)

    @leangle.add_schema('BaseSchema')
    class BaseSchema(Schema):
        name = fields.Str()

    mock_api = {
        'definitions': {},
    }
    result = _add_leangle_schemas(mock_api)

    expected = {
        'definitions': {
            'BaseSchema': {
                'additionalProperties': False,
                'properties': {
                    'name': {
                        'title': 'name',
                        'type': 'string',
                    },
                },
                'type': 'object',
            },
        },
    }

    assert result == expected
