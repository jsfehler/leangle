leangle
=======

.. image:: https://img.shields.io/github/license/jsfehler/leangle.svg
    :alt: GitHub
    :target: https://github.com/jsfehler/leangle/blob/master/LICENSE


An add-on for `chalice <https://github.com/aws/chalice>`_ to improve documentation of an API Gateway.


Describe API Responses
------------------------

API Responses can be described with the `describe_response` decorator.
They will be added as documentation to the API Gateway.
They should go after the route decorator, and can be stacked.

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe_response(201, description='Created')
    @leangle.describe_response(422, description='Missing Parameter')
    def index():
        return Response(status_code=201)


Add schemas
~~~~~~~~~~~

Schema objects can be defined using `marshmallow <https://github.com/marshmallow-code/marshmallow>`_

When decorated with the `add_schema` decorator, they will be added as models to the API Gateway.

.. code-block:: python

  import leangle
  from marshmallow import Schema, fields


  @leangle.add_schema('BaseSchema')
  class BaseSchema(Schema):
      name = fields.Str()


  @app.route('/', methods=['POST'])
  @leangle.describe_response(201, description='Created', schema='BaseSchema')
  def index():
      return Response(status_code=201)
