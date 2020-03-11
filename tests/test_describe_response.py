from describe_response import describe_response


def test_describe_response():

    @describe_response('201', description="Yep, it's wood")
    def test_func():
        pass

    assert test_func._leangle_responses == {
        '201': "Yep, it's wood",
    }
