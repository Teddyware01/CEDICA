from flask import Flask
from flask import render_template
from src.web.handlers import error

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    
    @app.route('/')
    def home():
        return render_template("home.html")
    
    @app.route('/sobre_nosotros')
    def sobre_nosotros():
        return render_template("sobre_nosotros.html")
    
    



    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(500, error.error_internal_server_error)

    return app

