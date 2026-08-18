import os

class Config:
    """
    Configuración base de la aplicación.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-notificaciones')
    
    # Configuración de SQLite propia para el microservicio
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f'sqlite:///{os.path.join(BASE_DIR, "notificaciones.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
