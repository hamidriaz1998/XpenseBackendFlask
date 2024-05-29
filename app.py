from flask import Flask
from extensions import db, migrate
from config import Config
import importlib
import Controllers

def register_blueprints(app):
    for module_name in Controllers.__all__:
        module = importlib.import_module(f'Controllers.{module_name}')
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp, url_prefix='/api')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)