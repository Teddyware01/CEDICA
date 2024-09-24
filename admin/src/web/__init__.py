from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.config import config
from src.core import database
from src.core import seeds


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
<<<<<<< HEAD
    app.config.from_object(config[env])
    database.init_app(app)
    
    @app.route('/')
=======

    @app.route("/")
>>>>>>> e27f665740dd64ab56d107a82b4c56a124d28d86
    def home():
        return render_template("home.html")

    @app.route("/sobre_nosotros")
    def sobre_nosotros():
        return render_template("sobre_nosotros.html")
<<<<<<< HEAD
    
    
    app.register_blueprint(issues_bp)
=======
>>>>>>> e27f665740dd64ab56d107a82b4c56a124d28d86

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(500, error.error_internal_server_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
