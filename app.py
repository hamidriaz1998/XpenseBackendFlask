from flask import Flask
from extensions import db, migrate, bcrypt, jwt
from config import Config
import importlib
import Controllers
import os
from dotenv import load_dotenv


def register_blueprints(app):
    for module_name in Controllers.__all__:
        module = importlib.import_module(f"Controllers.{module_name}")
        if hasattr(module, "bp"):
            app.register_blueprint(module.bp, url_prefix="/api")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # setup extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    # setup jwt key
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    # register blueprints
    register_blueprints(app)

    return app


if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        load_dotenv()
    app = create_app()
    app.run(debug=True)
