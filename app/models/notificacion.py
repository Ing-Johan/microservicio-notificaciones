from datetime import datetime, timezone
from app import db

class Notificacion(db.Model):
    """
    Modelo ORM para la tabla 'notificaciones'.
    Almacena cada comunicación enviada y su registro de auditoría.
    """
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    destinatario = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado_envio = db.Column(db.String(30), nullable=False, default='PENDIENTE')
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Restricción para garantizar que el tipo solo sea 'email' o 'sms'
    __table_args__ = (
        db.CheckConstraint("tipo IN ('email', 'sms')", name='check_tipo_notificacion'),
    )

    def to_dict(self):
        """
        Convierte la instancia del modelo a un diccionario serializable en JSON.
        """
        return {
            'id': self.id,
            'destinatario': self.destinatario,
            'tipo': self.tipo,
            'asunto': self.asunto,
            'mensaje': self.mensaje,
            'estado_envio': self.estado_envio,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
