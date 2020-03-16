from typing import Callable


_leangle_schemas = []

# Patches
# On AWS, chalice does not include deploy, so ignore patching it.
try:
    from .chalice_patches import patch_generate_route_method, patch_generate_swagger  # NOQA
    from chalice.deploy.swagger import SwaggerGenerator # NOQA

    SwaggerGenerator.generate_swagger = patch_generate_swagger()
    SwaggerGenerator._generate_route_method = patch_generate_route_method()

except ImportError:
    pass


def add_schema() -> Callable:
    """Add a model to chalice from a schema.

    Example:
        import leangle


        @leangle.add_schema()
        class PetSchema(Schema):
            name = fields.Str()

    """
    def wrapper(cls: Callable) -> Callable:
        _leangle_schemas.append(cls)
        return cls

    return wrapper
