from flask import Blueprint, request, jsonify
from src.core import contenido
from datetime import datetime
from src.core.contenido import list_contenido,list_contenido_published,get_contenido_id, create_contenido, update_contenido, delete_contenido, obtener_usuario_por_id
from src.web.schemas.contenido import contenidos_schema, create_contenido_schema, contenido_schema
from src.core.contenido.contenido import EstadoContenidoEnum


bp = Blueprint("contenido_api", __name__, url_prefix="/api/contenido")

@bp.get("/")
def index():
    print("ENTRE")
    contenidos = list_contenido_published()
    data = contenidos_schema.dump(contenidos)

    print("TODOS:")
    print(data)  

    return jsonify(data), 200


@bp.get("/id/<int:contenido_id>")
def traer_contenido_por_id(contenido_id):
    contenido = get_contenido_id(contenido_id)
    if not contenido:
        print("contenido is null")
        return jsonify({"error": "Contenido no encontrado"}), 404
    
    data = contenido_schema.dump(contenido)

    print("devolviendo")
    print( jsonify(data))
    return jsonify(data), 200


@bp.post("/")
def create():
    attrs = request.get_json()
    
    # Valida datos usando el esquema de creacion
    errors = create_contenido_schema.validate(attrs)
    if errors:
        return jsonify(errors), 400

    # carga y crea  "contenido"
    content_data = create_contenido_schema.load(attrs)
    content_data["fecha_publicacion"] = datetime.now()
    content_data["estado"] = EstadoContenidoEnum.PUBLICADO.value
    autor = obtener_usuario_por_id(content_data["autor_user_id"])
    if not autor:
        return jsonify({"autor_user_id": "El autor no existe"}), 404
    new_content = create_contenido(**content_data)
    new_content.autor = autor
    

    # Serializar el nuevo contenido para la respuesta
    data = contenido_schema.dump(new_content)
    
 

    return jsonify(data), 201


#hacer la que trae el contenido en epseciipcio
@bp.post("/{contenido_id}")
def create_porid():
    
    attrs = request.get_json()

    # Valida datos usando el esquema de creacion
    errors = create_contenido_schema.validate(attrs)
    if errors:
        return jsonify(errors), 400

    # carga y crea  "contenido"
    content_data = create_contenido_schema.load(attrs)
    new_content = create_contenido(**content_data)

    # Serializar el nuevo contenido para la respuesta
    data = contenido_schema.dump(new_content)

    return jsonify(data), 201


@bp.get("/<int:contenido_id>")
def update(contenido_id):
    attrs = request.get_json()

    errors = contenido_schema.validate(attrs)
    if errors:
        return jsonify(errors), 400

   
    updated_contenido = update_contenido(contenido_id, **attrs)

    if isinstance(updated_contenido, dict) and "error" in updated_contenido:
        return jsonify(updated_contenido), 404

    data = contenido_schema.dump(updated_contenido)
    return jsonify(data), 200

@bp.post("/ulr para eliminar")
def delete(contenido_id):

    response = delete_contenido(contenido_id)

    if isinstance(response, dict) and "error" in response:
        return jsonify(response), 404

    return jsonify(response), 200

