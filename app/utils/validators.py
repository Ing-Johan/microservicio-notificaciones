import re

def validar_datos_notificacion(data):
    """
    Valida la estructura y los datos requeridos para crear una notificación.
    Retorna un diccionario con los datos limpios o lanza ValueError si no cumple.
    """
    if not isinstance(data, dict):
        raise ValueError("El cuerpo de la petición debe ser un objeto JSON.")

    campos_requeridos = ['destinatario', 'tipo', 'asunto', 'mensaje']
    for campo in campos_requeridos:
        valor = data.get(campo)
        if valor is None or (isinstance(valor, str) and not valor.strip()) or not isinstance(valor, (str, int, float)):
            raise ValueError(f"El campo '{campo}' es obligatorio y debe ser un valor de texto válido.")

    tipo = str(data['tipo']).strip().lower()
    if tipo not in ['email', 'sms']:
        raise ValueError("El campo 'tipo' únicamente permite los valores 'email' o 'sms'.")

    destinatario = str(data['destinatario']).strip()
    if tipo == 'email':
        patron_email = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(patron_email, destinatario):
            raise ValueError("El campo 'destinatario' no contiene un formato de correo electrónico válido.")
    elif tipo == 'sms':
        patron_sms = r'^\+?[0-9\s\-]{7,15}$'
        if not re.match(patron_sms, destinatario):
            raise ValueError("El campo 'destinatario' no contiene un número de teléfono válido para SMS.")

    return {
        'destinatario': destinatario,
        'tipo': tipo,
        'asunto': str(data['asunto']).strip(),
        'mensaje': str(data['mensaje']).strip()
    }
