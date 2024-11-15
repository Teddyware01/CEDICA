from flask import Blueprint, request, jsonify
from src.core import contenido
from src.core.contenido import list_contenido, create_contenido
from src.web.schemas.contenido import contenidos_schema, create_contenido_schema, contenido_schema


bp = Blueprint("contenido_api", __name__, url_prefix="/api/contenido")

@bp.get("/")
def index():
    print("ENTRE")
    contenidos = list_contenido()
    data = contenidos_schema.dump(contenidos)

    print("TODOS:")
    print(data)  

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
    new_content = create_contenido(**content_data)

    # Serializar el nuevo contenido para la respuesta
    data = contenido_schema.dump(new_content)

    return jsonify(data), 201


#hacer la que trae el contenido en epseciipcio
@bp.post("/{contenido_id}")
def create():
    
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
