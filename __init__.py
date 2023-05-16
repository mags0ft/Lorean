from flask import Flask
from .app.config import *

from .app.main import main

def create_app():
    app = Flask(
        __name__,

        template_folder = "app/templates",
        static_folder = "app/static"
    )

    app.register_blueprint(main)
    
    return app