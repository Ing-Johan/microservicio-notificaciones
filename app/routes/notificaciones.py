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
    except Exception:
        return jsonify({'error': 'Ocurrió un error interno al procesar la notificación.'}), 500


@notificaciones_bp.route('', methods=['GET'], strict_slashes=False)
def listar_notificaciones():
    """
    Endpoint: GET /notificaciones
    - Sin parámetros: Devuelve la lista completa de todas las notificaciones registradas.
    - Con parámetro ?destinatario=X: Devuelve las notificaciones filtradas por ese destinatario.
    """
    try:
        destinatario = request.args.get('destinatario')
        
        if destinatario is not None:
            notificaciones = NotificacionService.obtener_por_destinatario(destinatario)
        else:
            notificaciones = NotificacionService.obtener_todas()
            
        return jsonify([n.to_dict() for n in notificaciones]), 200
    except Exception:
        return jsonify({'error': 'Ocurrió un error interno al consultar las notificaciones.'}), 500


@notificaciones_bp.route('/<int:notificacion_id>', methods=['GET'])
def obtener_notificacion_por_id(notificacion_id):
    """
    Endpoint: GET /notificaciones/<id>
    Obtiene la notificación correspondiente al ID proporcionado.
    Retorna HTTP 200 con la notificación en JSON o HTTP 404 si no existe.
    """
    try:
        notificacion = NotificacionService.obtener_por_id(notificacion_id)
        if notificacion is None:
            return jsonify({'error': f'La notificación con el ID {notificacion_id} no fue encontrada.'}), 404

        return jsonify(notificacion.to_dict()), 200
    except Exception:
        return jsonify({'error': 'Ocurrió un error interno al consultar la notificación.'}), 500


@notificaciones_bp.route('/<int:notificacion_id>', methods=['PUT'])
def actualizar_notificacion(notificacion_id):
    """
    Endpoint: PUT /notificaciones/<id>
    Actualiza los campos permitidos (destinatario, tipo, asunto, mensaje) de una notificación existente.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}), 400

    try:
        notificacion_actualizada = NotificacionService.actualizar_notificacion(notificacion_id, data)
        if notificacion_actualizada is None:
            return jsonify({'error': f'La notificación con el ID {notificacion_id} no fue encontrada.'}), 404

        return jsonify(notificacion_actualizada.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Ocurrió un error interno al actualizar la notificación.'}), 500


@notificaciones_bp.route('/<int:notificacion_id>', methods=['DELETE'])
def eliminar_notificacion(notificacion_id):
    """
    Endpoint: DELETE /notificaciones/<id>
    Elimina la notificación correspondiente al ID proporcionado.
    Retorna HTTP 200 con mensaje de éxito o HTTP 404 si no existe.
    """
    try:
        eliminado = NotificacionService.eliminar_notificacion(notificacion_id)
        if not eliminado:
            return jsonify({'error': f'La notificación con el ID {notificacion_id} no fue encontrada.'}), 404

        return jsonify({'mensaje': f'Notificación con ID {notificacion_id} eliminada exitosamente.'}), 200
    except Exception:
        return jsonify({'error': 'Ocurrió un error interno al eliminar la notificación.'}), 500
