from flask import Blueprint, request, jsonify
from app.services.notificacion_service import NotificacionService

notificaciones_bp = Blueprint('notificaciones', __name__, url_prefix='/notificaciones')

@notificaciones_bp.route('', methods=['POST'], strict_slashes=False)
def crear_notificacion():
    """
    Endpoint: POST /notificaciones
    Recibe un JSON con destinatario, tipo (email/sms), asunto y mensaje.
    Valida, simula el envío y guarda el registro en SQLite.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}), 400

    try:
        nueva_notificacion = NotificacionService.crear_notificacion(data)
        return jsonify(nueva_notificacion.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error interno al procesar la notificación.'}), 500
