from marshmallow import Schema, fields, post_load, post_dump
from marshmallow.validate import OneOf
from src.core.contenido.contenido import Contenido, TipoContenidoEnum, EstadoContenidoEnum
from src.core.auth import get_alias_por_id

class ContenidoSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    contenido = fields.Str(required=True)
    published_at = fields.DateTime(allow_none=True)
    inserted_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    tipo = fields.Str(
        validate=OneOf([e.value for e in TipoContenidoEnum]), required=True
    )
    estado = fields.Str(
        validate=OneOf([e.value for e in EstadoContenidoEnum]), required=True
    )

    autor_user_id = fields.Int(required=True)


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
    titulo = fields.Str(required=True)
    tipo = fields.Str(dump_only=True)
    estado = fields.Str(dump_only=True)

class CreateContenidoSchema(Schema):
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    contenido = fields.Str(required=True)
    tipo = fields.Str(
        validate=OneOf([e.value for e in TipoContenidoEnum]), required=True
    )
    autor_user_id = fields.Int(required=True)

# Instancias de los esquemas
contenido_schema = ContenidoSchema()
contenidos_schema = ContenidoSchema(many=True)
simple_contenido_schema = SimpleContenidoSchema()
create_contenido_schema = CreateContenidoSchema()
