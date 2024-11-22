from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from marshmallow.validate import Length, OneOf
from src.core.contenido.contenido import Contenido, TipoContenidoEnum, EstadoContenidoEnum

# Constantes para validar estados y tipos
TIPOS_CONTENIDO = [e.value for e in TipoContenidoEnum]
ESTADOS_CONTENIDO = [e.value for e in EstadoContenidoEnum]

class AutorSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)

class ContenidoSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(
        required=True, 
        validate=Length(max=255, error="El título no puede tener más de 255 caracteres.")
    )
    copete = fields.Str(
        required=True, 
        validate=Length(max=500, error="El copete no puede tener más de 500 caracteres.")
    )
    contenido = fields.Str(required=True)
    fecha_publicacion = fields.DateTime(allow_none=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_actualizacion = fields.DateTime(dump_only=True)
    
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )
    
    autor = fields.Nested(AutorSchema, dump_only=True)

    @post_load
    def make_contenido(self, data, **kwargs):
        return Contenido(**data)

class SimpleContenidoSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(
        required=True, 
        validate=Length(max=255, error="El título no puede tener más de 255 caracteres.")
    )
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )
    estado = fields.Str(
        validate=OneOf(ESTADOS_CONTENIDO, error="Estado de contenido no válido."),
        required=True
    )


class CreateContenidoSchema(Schema):
    titulo = fields.Str(
        required=True, 
        validate=Length(max=255, error="El título no puede tener más de 255 caracteres.")
    )
    copete = fields.Str(
        required=True, 
        validate=Length(max=500, error="El copete no puede tener más de 500 caracteres.")
    )
    contenido = fields.Str(required=True)
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )
    autor_user_id = fields.Int(required=True)

# Instancias de los esquemas
contenido_schema = ContenidoSchema()
contenidos_schema = ContenidoSchema(many=True)
simple_contenido_schema = SimpleContenidoSchema()
create_contenido_schema = CreateContenidoSchema()
