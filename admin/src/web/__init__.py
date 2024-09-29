from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.controllers.usuarios import bp as usuarios_bp


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(issues_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/sobre_nosotros")
    def sobre_nosotros():
        return render_template("sobre_nosotros.html")
    
    
    @app.route("/add_client")
    def add_client():
        return render_template("add_client.html")
    
    
    @app.route("/edit_client")
    def edit_client():
        return render_template("listado.html")

    @app.route("/delete_client")
    def delete_client():
        return render_template("listado.html")
    

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(500, error.error_internal_server_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
