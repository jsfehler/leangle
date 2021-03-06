leangle
=======

.. image:: https://img.shields.io/pypi/v/leangle.svg
    :target: https://pypi.org/project/leangle
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/leangle.svg
    :alt: PyPI - Python Version
    :target: https://github.com/jsfehler/leangle

.. image:: https://img.shields.io/github/license/jsfehler/leangle.svg
    :alt: GitHub
    :target: https://github.com/jsfehler/leangle/blob/master/LICENSE

.. image:: https://travis-ci.org/jsfehler/leangle.svg?branch=master
    :target: https://travis-ci.org/jsfehler/leangle

.. image:: https://coveralls.io/repos/github/jsfehler/leangle/badge.svg?branch=master
    :target: https://coveralls.io/github/jsfehler/leangle?branch=master

An add-on for `chalice <https://github.com/aws/chalice>`_ to improve documentation of an API Gateway.

As of version 1.13.0, chalice does not support models for the request or response.
This means any documentation generated for an API Gateway is going to be much less useful.

leangle improves this with a collection of decorators for chalice route functions, and
built-in support for marshmallow schemas.

Installation
------------

Via pip:

.. code-block:: bash

  pip install leangle


Chalice itself is an optional dependency. This can be useful for testing and validation,
but should not be used for the version of chalice deployed to AWS.

.. code-block:: bash

  pip install leangle[chalice]


Describe API Parameters
------------------------

API Responses can be described with the *describe.parameter* decorator.
They will be added as documentation to the API Gateway.
They should go after the route decorator, and can be stacked.

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe.parameter(name='body', _in='body', description='Create a new widget', schema='WidgetSchema')
    def index():
        return Response(status_code=201)


Describing the 'in' field of a parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*_in* is used, as *in* is a reserved word in Python.


Describe API Responses
------------------------

API Responses can be described with the *describe.response* decorator.
They will be added as documentation to the API Gateway.
They should go after the route decorator, and can be stacked.

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe.response(201, description='Created')
    @leangle.describe.response(422, description='Missing Parameter')
    def index():
        return Response(status_code=201)


Describe Method Tags
--------------------

.. code-block:: python

    import leangle


    @app.route('/', methods=['POST'])
    @leangle.describe.tags(["x-large"])
    def index():
        return Response(status_code=201)


Add schemas
~~~~~~~~~~~

Schema objects can be defined using `marshmallow <https://github.com/marshmallow-code/marshmallow>`_

When decorated with the *add_schema* decorator, they will be added as models to the API Gateway.

The name of these Schema classes can be used in the describe decorators.

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
