import leangle


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
