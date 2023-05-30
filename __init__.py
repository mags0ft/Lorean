from flask import Flask
from dotenv import load_dotenv
from os import getenv, mkdir, path
from uuid import uuid4

from .app.config import *
from .app.main import main

if not path.isfile(ENVFILE):
    with open(ENVFILE, "w") as f:
        f.write(
            f'SECRET_KEY="{str(uuid4())}-{str(uuid4())}"' +
            '\nFLASK_APP="__init__.py"'
        )

if not path.isdir(LOGDIR):
    mkdir(LOGDIR)

load_dotenv()

def create_app():
    app = Flask(
        __name__,

        template_folder = "app/templates",
        static_folder = "app/static"
    )

    app.register_blueprint(main)

    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.jinja_env.globals.update(round=round, len=len)

    return app