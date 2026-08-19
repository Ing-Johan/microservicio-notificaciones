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


@notificaciones_bp.route('', methods=['GET'], strict_slashes=False)
def listar_notificaciones():
    """
    Endpoint: GET /notificaciones?destinatario=X
    Obtiene las notificaciones filtradas por el parámetro de consulta 'destinatario'.
    Si no existen resultados o no se provee el parámetro, retorna [] con HTTP 200.
    """
    destinatario = request.args.get('destinatario', default='', type=str)
    notificaciones = NotificacionService.obtener_por_destinatario(destinatario)
    
    return jsonify([n.to_dict() for n in notificaciones]), 200


@notificaciones_bp.route('/<int:notificacion_id>', methods=['GET'])
def obtener_notificacion_por_id(notificacion_id):
    """
    Endpoint: GET /notificaciones/<id>
    Obtiene la notificación correspondiente al ID proporcionado.
    Retorna HTTP 200 con la notificación en JSON o HTTP 404 si no existe.
    """
    notificacion = NotificacionService.obtener_por_id(notificacion_id)
    if notificacion is None:
        return jsonify({'error': f'La notificación con el ID {notificacion_id} no fue encontrada.'}), 404

    return jsonify(notificacion.to_dict()), 200
