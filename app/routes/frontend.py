from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    """
    Ruta raíz para servir la interfaz web (Frontend) del microservicio.
    """
    return render_template('index.html')
