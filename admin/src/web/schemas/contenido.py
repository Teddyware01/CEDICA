from marshmallow import Schema, fields, post_load, validates_schema, ValidationError, post_dump
from marshmallow.validate import Length, OneOf
from src.core.contenido.contenido import Contenido, TipoContenidoEnum, EstadoContenidoEnum
from src.core.auth import get_alias_por_id

# Constantes para validar estados y tipos
TIPOS_CONTENIDO = [e.value for e in TipoContenidoEnum]
ESTADOS_CONTENIDO = [e.value for e in EstadoContenidoEnum]

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
    
    published_at = fields.DateTime(allow_none=True)
    inserted_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    estado = fields.Str(
        validate=OneOf([e.value for e in EstadoContenidoEnum]), required=False
    )
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )

    autor_user_id = fields.Int()



    @post_dump
    def translate_enum(self, data, **kwargs):
        tipo_value = data.get('tipo').split('.')[-1] #Sino entraba todo entero y falla como key ( entraba como TipoContenidoEnum.ARTICULO_INFO)
        data['tipo'] = TipoContenidoEnum[tipo_value].value if data['tipo'] else None
        estado_value = data.get('estado').split('.')[-1] 
        data['estado'] = EstadoContenidoEnum[estado_value].value if data['estado'] else None
        return data
    
    @post_dump
    def translate_autor(self, data, **kwargs):
        data['autor'] = get_alias_por_id(data['autor_user_id']) if data['autor_user_id'] else "Desconocido."
        return data


    @post_dump
    def translate_enum(self, data, **kwargs):
        tipo_value = data.get('tipo').split('.')[-1] #Sino entraba todo entero y falla como key ( entraba como TipoContenidoEnum.ARTICULO_INFO)
        data['tipo'] = TipoContenidoEnum[tipo_value].value if data['tipo'] else None
        estado_value = data.get('estado').split('.')[-1] 
        data['estado'] = EstadoContenidoEnum[estado_value].value if data['estado'] else None
        return data
    
    @post_dump
    def translate_autor(self, data, **kwargs):
        data['autor'] = get_alias_por_id(data['autor_user_id']) if data['autor_user_id'] else "Desconocido."
        return data

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
        required=False, 
        validate=Length(max=500, error="El copete no puede tener más de 500 caracteres.")
    )
    contenido = fields.Str(required=False)
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )
    autor_user_id = fields.Int(required=True)

class PublicateContenidoSchema(Schema):
    titulo = fields.Str(
        required=True,
        validate=Length(max=255, error="El título no puede tener más de 255 caracteres y es obligatorio.")
    )
    copete = fields.Str(
        required=True,
        validate=[
            Length(min=1, max=500, error="El copete no puede estar vacío y debe tener máximo 500 caracteres."),
        ]
    )
    contenido = fields.Str(
        required=True,
        validate=Length(min=1, error="El contenido no puede estar vacío.")
    )
    tipo = fields.Str(
        validate=OneOf(TIPOS_CONTENIDO, error="Tipo de contenido no válido."),
        required=True
    )
    fecha_publicacion = fields.DateTime(required=True)
    autor_user_id = fields.Int(required=True)


# Instancias de los esquemas
contenido_schema = ContenidoSchema()
contenidos_schema = ContenidoSchema(many=True)
simple_contenido_schema = SimpleContenidoSchema()
create_contenido_schema = CreateContenidoSchema()
publicate_contenido_schema = PublicateContenidoSchema()
