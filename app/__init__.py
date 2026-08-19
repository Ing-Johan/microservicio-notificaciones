from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Fábrica de aplicaciones (Application Factory Pattern) de Flask.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar Blueprints (rutas API y Frontend)
    from app.routes.notificaciones import notificaciones_bp
    from app.routes.frontend import frontend_bp

    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(frontend_bp)

    # Cargar modelos e inicializar las tablas automáticamente en SQLite
    from app.models import Notificacion
    with app.app_context():
        db.create_all()

    return app
