from flask import Blueprint

# Blueprint para encapsular las rutas de notificaciones
notificaciones_bp = Blueprint('notificaciones', __name__, url_prefix='/notificaciones')

# Los endpoints (POST /, GET /, GET /<id>) se implementarán en la siguiente etapa.
