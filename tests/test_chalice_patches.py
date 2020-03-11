import leangle
from leangle.chalice_patches import _add_leangle_schemas

from marshmallow import Schema, fields

from marshmallow_jsonschema import JSONSchema


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
            'BaseSchema': JSONSchema().dump(BaseSchema())['definitions'],
        },
    }

    assert result == expected
