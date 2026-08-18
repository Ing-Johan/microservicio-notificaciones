from app import db
from app.models.notificacion import Notificacion
from app.utils.validators import validar_datos_notificacion

class NotificacionService:
    """
    Capa de servicio que gestiona la lógica de negocio del microservicio de notificaciones.
    """

    @staticmethod
    def simular_envio(tipo, destinatario, asunto, mensaje):
        """
        Simula el envío de una comunicación por email o SMS.
        En una implementación real aquí se llamaría a un proveedor de correo/SMS.
        """
        # Simulación exitosa del envío
        return "ENVIADO"

    @classmethod
    def crear_notificacion(cls, data):
        """
        Valida, simula el envío y persiste el registro de la notificación.
        """
        # 1. Validar los datos de entrada
        datos_validados = validar_datos_notificacion(data)

        # 2. Simular el envío
        estado = cls.simular_envio(
            tipo=datos_validados['tipo'],
            destinatario=datos_validados['destinatario'],
            asunto=datos_validados['asunto'],
            mensaje=datos_validados['mensaje']
        )

        # 3. Instanciar y persistir en la base de datos mediante SQLAlchemy
        nueva_notificacion = Notificacion(
            destinatario=datos_validados['destinatario'],
            tipo=datos_validados['tipo'],
            asunto=datos_validados['asunto'],
            mensaje=datos_validados['mensaje'],
            estado_envio=estado
        )

        db.session.add(nueva_notificacion)
        db.session.commit()

        return nueva_notificacion

    @staticmethod
    def obtener_por_destinatario(destinatario):
        """
        Consulta y retorna las notificaciones asociadas a un destinatario.
        """
        if not destinatario or not str(destinatario).strip():
            return []
        
        return Notificacion.query.filter_by(destinatario=str(destinatario).strip()).all()

    @staticmethod
    def obtener_por_id(notificacion_id):
        """
        Consulta y retorna una notificación específica por su ID.
        """
        return db.session.get(Notificacion, notificacion_id)
