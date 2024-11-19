#import logging
from flask import Flask
from flask import render_template, redirect,url_for
from src.web.handlers import error
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.storage import storage
from src.web import helpers 
from src.web.controllers.equipo import bp as equipo_blueprint
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.usuarios import bp as usuarios_bp
from src.web.controllers.pagos import pagos_bp
from src.web.controllers.cobros import cobros_bp
from src.web.controllers.ecuestre import bp as ecuestre_bp
from src.web.controllers.auth import bp as auth_blueprint
from flask_session import Session
from src.web.handlers.auth import is_authenticated, check_permission
from src.web.controllers.jya import bp as jya_bp
from src.web.api.issues import bp as issues_api_bp
from src.web.api.contenido import bp as contenido_api_bp
from flask_cors import CORS

session= Session()

#logging.basicConfig()
#logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    session.init_app(app)

    app.register_blueprint(pagos_bp, url_prefix="/pagos")
    app.register_blueprint(cobros_bp, url_prefix="/cobros")
    app.register_blueprint(usuarios_bp)     
    app.register_blueprint(issues_bp)
    app.register_blueprint(ecuestre_bp)
    app.register_blueprint(equipo_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(jya_bp)
    
    app.register_blueprint(issues_api_bp)
    app.register_blueprint(contenido_api_bp)
    
    
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.route("/sobre_nosotros")
    def sobre_nosotros():
        return render_template("sobre_nosotros.html")
    
    # Register object storage
    storage.init_app(app)

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(500, error.error_internal_server_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(413, error.forbidden)
    app.register_error_handler(413, error.payload)

    #registrar functions en jinja
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)



    app.jinja_env.globals.update(avatar_url=helpers.avatar_url)
    

    #ENABLE CORS
    CORS(app)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()
    
    # Reset y seeds automáticos al iniciar la app
    # Deberia sacarse la eliminacion de la base de datos a la hora de usarse en deploy.
    #Lo comento porque me molesta a la hora de trabajar.
    with app.app_context():
        database.reset()  # Restablece la base de datos
        seeds.run()       # Ejecuta los seeds de la base de datos

    return app
