from flask import Flask
from dotenv import load_dotenv
from os import getenv, mkdir, path
from uuid import uuid4
import webbrowser

from .config import *
from .main import main

if not path.isfile(ENVFILE):
    with open(ENVFILE, "w") as f:
        f.write(
            f'SECRET_KEY="{str(uuid4())}-{str(uuid4())}"' +
            '\nFLASK_APP="__init__.py"'
        )

if not path.isdir(LOGDIR):
    mkdir(LOGDIR)

load_dotenv()

def create_app(standalone = False):
    app = Flask(
        __name__
    )

    app.register_blueprint(main)

    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.jinja_env.globals.update(round=round, len=len)

    if standalone:
        webbrowser.open("http://localhost:5000/")

    return app