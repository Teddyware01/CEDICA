from flask import Flask
from flask import render_template, redirect
from src.web.handlers import error
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.controllers.equipo import bp as equipo_blueprint
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.usuarios import bp as usuarios_bp
from src.web.controllers.pagos import pagos_bp


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(issues_bp)      
    app.register_blueprint(pagos_bp)


    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/sobre_nosotros")
    def sobre_nosotros():
        return render_template("sobre_nosotros.html")

    @app.route("/ecuestre")
    def ecuestre():
        return render_template("ecuestre.html")

    @app.route("/jya")
    def jya():
        return render_template("jya.html")

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(500, error.error_internal_server_error)
    app.register_blueprint(equipo_blueprint)
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app