import leangle

from marshmallow import Schema, fields


def test_describe_response():

    @leangle.describe_response('201', description="Yep, it's wood")
    def test_func():
        pass

    assert test_func._leangle_responses == {
        '201': {
            'description': "Yep, it's wood",
            'schema': {'$ref': '#/definitions/Empty'},
        },
    }


def test_describe_response_has_schema():

    @leangle.describe_response(
        '201', description="Yep, it's wood", schema='PetStore',
    )
    def test_func():
        pass

    assert test_func._leangle_responses == {
        '201': {
            'description': "Yep, it's wood",
            'schema': {'$ref': '#/definitions/PetStore'},
        },
    }


def test_add_schema():

    @leangle.add_schema('PetSchema')
    class PetSchema(Schema):
        name = fields.Str()

    assert leangle.leangle._leangle_schemas == {'PetSchema': PetSchema}
