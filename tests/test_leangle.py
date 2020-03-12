import leangle

from marshmallow import Schema, fields


def test_describe_parameter():

    @leangle.describe.parameter('body', description="Is it wood?")
    def test_func():
        pass

    assert test_func._leangle_parameters == {
        'body': {
            'description': "Is it wood?",
        },
    }


def test_describe_parmeter_has_schema():

    @leangle.describe.response(
        'body', description="Is it wood?", schema='WoodRequest',
    )
    def test_func():
        pass

    assert test_func._leangle_responses == {
        'body': {
            'description': "Is it wood?",
            'schema': {'$ref': '#/definitions/WoodRequest'},
        },
    }


def test_describe_response():

    @leangle.describe.response('201', description="Yep, it's wood")
    def test_func():
        pass

    assert test_func._leangle_responses == {
        '201': {
            'description': "Yep, it's wood",
        },
    }


def test_describe_response_has_schema():

    @leangle.describe.response(
        '201', description="Yep, it's wood", schema='WoodResponse',
    )
    def test_func():
        pass

    assert test_func._leangle_responses == {
        '201': {
            'description': "Yep, it's wood",
            'schema': {'$ref': '#/definitions/WoodResponse'},
        },
    }


def test_add_schema(request):

    def fin():
        leangle.leangle._leangle_schemas = {}

    request.addfinalizer(fin)

    @leangle.add_schema('PetSchema')
    class PetSchema(Schema):
        name = fields.Str()

    assert leangle.leangle._leangle_schemas == {'PetSchema': PetSchema}
