from chalice.deploy.swagger import SwaggerGenerator


_leangle_schemas = {}

# Patches
from .chalice_patches import patch_generate_route_method, patch_generate_swagger  # NOQA

SwaggerGenerator.generate_swagger = patch_generate_swagger()
SwaggerGenerator._generate_route_method = patch_generate_route_method()


def add_schema(name):
    """Add a model to chalice from a schema.

    Example:
        import leangle


        @leangle.add_schema('PetSchema')
        class PetSchema(Schema):
            name = fields.Str()

    """
    def wrapper(func):
        _leangle_schemas[name] = func
        return func

    return wrapper
