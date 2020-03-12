leangle
=======

.. image:: https://img.shields.io/github/license/jsfehler/leangle.svg
    :alt: GitHub
    :target: https://github.com/jsfehler/leangle/blob/master/LICENSE

.. image:: https://travis-ci.org/jsfehler/leangle.svg?branch=master
    :target: https://travis-ci.org/jsfehler/leangle

.. image:: https://coveralls.io/repos/github/jsfehler/leangle/badge.svg?branch=master
    :target: https://coveralls.io/github/jsfehler/leangle?branch=master

An add-on for `chalice <https://github.com/aws/chalice>`_ to improve documentation of an API Gateway.


Describe API Parameters
------------------------

API Responses can be described with the `describe.parameter` decorator.
They will be added as documentation to the API Gateway.
They should go after the route decorator, and can be stacked.

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe.parameter('body', description='Create a new widget', schema='WidgetSchema')
    def index():
        return Response(status_code=201)


Describe API Responses
------------------------

API Responses can be described with the `describe.response` decorator.
They will be added as documentation to the API Gateway.
They should go after the route decorator, and can be stacked.

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe.response(201, description='Created')
    @leangle.describe.response(422, description='Missing Parameter')
    def index():
        return Response(status_code=201)


Add schemas
~~~~~~~~~~~

Schema objects can be defined using `marshmallow <https://github.com/marshmallow-code/marshmallow>`_

When decorated with the `add_schema` decorator, they will be added as models to the API Gateway.

.. code-block:: python

  import leangle
  from marshmallow import Schema, fields


  @leangle.add_schema()
  class BaseSchema(Schema):
      name = fields.Str()


  @app.route('/', methods=['POST'])
  @leangle.describe.response(201, description='Created', schema='BaseSchema')
  def index():
      return Response(status_code=201)
