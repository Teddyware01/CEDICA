from flask import Blueprint, render_template, request, jsonify, current_app
from src.core import contacto
from src.core.contacto.models import Contacto
from src.core.database import db

bp = Blueprint("contacto", __name__, url_prefix="/contacto")


@bp.get("/")
def listar_consultas():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    consultas = contacto.list_consultas(sort_by=sort_by, search=search, page=page)
    return render_template("contacto/listar_consultas.html", consultas=consultas)
    

@bp.post("/verify-captcha")
def verify_captcha():
    secret_key = "6LcD3n4qAAAAAI1RssEtVWIAtuaBn25ebGctDRr5"
    captcha_response = request.json.get("captchaResponse")

    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": captcha_response}
    response = request.post(verification_url, data=payload)
    result = response.json()

    if result.get("success"):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": result.get("error-codes")})


@bp.post('/submit_form')
def submit_form():
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400

    try:
        nombre = request.json.get('nombre')
        email = request.json.get('email')
        mensaje = request.json.get('mensaje')

        nuevo_mensaje = Contacto(nombre=nombre, email=email, mensaje=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return jsonify({'mensaje': 'Mensaje enviado con éxito!'}), 200
    except Exception as e:
        current_app.logger.error(f'Failed to insert message: {e}')
        return jsonify({'error': 'Internal server error'}), 500