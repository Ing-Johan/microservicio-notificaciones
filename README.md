# Microservicio de Notificaciones (`microservicio-notificaciones`)

## 📋 Descripción
`microservicio-notificaciones` es un microservicio backend independiente desarrollado en Python con Flask y SQLAlchemy, diseñado para simular el envío de comunicaciones (correo electrónico y SMS) a los usuarios y mantener un registro de auditoría persistente.

## 🎯 Objetivo del Microservicio
Proporcionar una API REST desacoplada que gestione el ciclo de vida de las notificaciones del sistema, garantizando la validación estricta de datos, la auditoría automática y la persistencia en una base de datos SQLite propia e independiente.

## 🏛️ Arquitectura
El microservicio implementa una arquitectura modular en capas basada en los patrones **Application Factory** y **Blueprints** de Flask:

- **Capa de Transporte (Routes)**: Expone los endpoints REST.
- **Capa de Negocio (Services & Utils)**: Procesa las reglas de negocio, simulación de envíos y validaciones.
- **Capa de Acceso a Datos (Models)**: Mapea la entidad mediante el ORM SQLAlchemy.
- **Capa de Persistencia**: Almacena los registros en una base de datos SQLite propia.

![Diagrama de Arquitectura](diagrams/arquitectura.png)

## 🛠️ Tecnologías Utilizadas
- **Lenguaje**: Python 3.x
- **Framework Web**: Flask
- **ORM**: Flask-SQLAlchemy / SQLAlchemy
- **Base de Datos**: SQLite 3

## 📁 Estructura del Proyecto
```text
microservicio-notificaciones/
│
├── app/
│   ├── __init__.py           # Aplicación Flask (Application Factory) y configuración SQLAlchemy
│   ├── config.py             # Configuración base del microservicio y URI de SQLite
│   ├── models/
│   │   ├── __init__.py
│   │   └── notificacion.py   # Modelo ORM Notificacion
│   ├── routes/
│   │   ├── __init__.py
│   │   └── notificaciones.py # Blueprint y controladores HTTP
│   ├── services/
│   │   ├── __init__.py
│   │   └── notificacion_service.py # Lógica de negocio y simulación de envío
│   └── utils/
│       ├── __init__.py
│       └── validators.py     # Validaciones de carga útil y tipos
│
├── diagrams/
│   └── arquitectura.png      # Diagrama de arquitectura del microservicio
├── .gitignore                # Archivos excluidos en control de versiones
├── app.py                    # Punto de entrada para ejecutar el microservicio
└── requirements.txt          # Dependencias de Python
```

## ⚙️ Requisitos Previos
- Python 3.9 o superior instalado.
- Gestor de paquetes `pip`.

## 📦 Instalación

1. **Clonar o descargar el repositorio del microservicio.**
2. **Crear y activar un entorno virtual:**
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Configuración
La configuración se administra en `app/config.py`. Por defecto, el microservicio utiliza la base de datos local SQLite `notificaciones.db` ubicada en la raíz del proyecto.
Se puede personalizar mediante variables de entorno:
- `DATABASE_URL`: URI de conexión a la base de datos.
- `SECRET_KEY`: Clave secreta de la aplicación.

## 🚀 Ejecución Local
Para iniciar el servidor de desarrollo en `http://localhost:5000`:
```bash
python app.py
```

---

## 📡 Documentación de Endpoints

### 1. Crear Notificación (`POST /notificaciones`)
Recibe los datos de la comunicación, valida las restricciones, simula el envío y registra la notificación.

- **Método**: `POST`
- **URL**: `/notificaciones`
- **Headers**: `Content-Type: application/json`
- **Body Request**:
  ```json
  {
    "destinatario": "usuario@ejemplo.com",
    "tipo": "email",
    "asunto": "Bienvenida al Sistema",
    "mensaje": "Hola, tu cuenta ha sido creada exitosamente."
  }
  ```
- **Respuesta Exitosa (`HTTP 201 Created`)**:
  ```json
  {
    "id": 1,
    "destinatario": "usuario@ejemplo.com",
    "tipo": "email",
    "asunto": "Bienvenida al Sistema",
    "mensaje": "Hola, tu cuenta ha sido creada exitosamente.",
    "estado_envio": "ENVIADO",
    "fecha": "2026-08-19T00:00:00.000000"
  }
  ```

---

### 2. Consultar Notificaciones por Destinatario (`GET /notificaciones?destinatario=X`)
Retorna todas las notificaciones asociadas al destinatario indicado en el parámetro de consulta.

- **Método**: `GET`
- **URL**: `/notificaciones?destinatario=usuario@ejemplo.com`
- **Respuesta Exitosa (`HTTP 200 OK`)**:
  ```json
  [
    {
      "id": 1,
      "destinatario": "usuario@ejemplo.com",
      "tipo": "email",
      "asunto": "Bienvenida al Sistema",
      "mensaje": "Hola, tu cuenta ha sido creada exitosamente.",
      "estado_envio": "ENVIADO",
      "fecha": "2026-08-19T00:00:00.000000"
    }
  ]
  ```
- **Sin resultados (`HTTP 200 OK`)**: `[]`

---

### 3. Consultar Notificación por ID (`GET /notificaciones/{id}`)
Retorna los detalles de una notificación específica por su ID.

- **Método**: `GET`
- **URL**: `/notificaciones/1`
- **Respuesta Exitosa (`HTTP 200 OK`)**:
  ```json
  {
    "id": 1,
    "destinatario": "usuario@ejemplo.com",
    "tipo": "email",
    "asunto": "Bienvenida al Sistema",
    "mensaje": "Hola, tu cuenta ha sido creada exitosamente.",
    "estado_envio": "ENVIADO",
    "fecha": "2026-08-19T00:00:00.000000"
  }
  ```
- **Respuesta No Encontrado (`HTTP 404 Not Found`)**:
  ```json
  {
    "error": "La notificación con el ID 99999 no fue encontrada."
  }
  ```

---

## 🚦 Códigos HTTP Utilizados
- `200 OK`: Petición GET procesada correctamente.
- `201 Created`: Notificación creada y registrada exitosamente.
- `400 Bad Request`: Petición malformada, JSON ausente o fallo de validación en campos.
- `404 Not Found`: Notificación solicitada por ID no existe en la base de datos.
- `500 Internal Server Error`: Error interno inesperado en el servidor o base de datos.

## 🛡️ Validaciones Implementadas
- **Campos Requeridos**: `destinatario`, `tipo`, `asunto` y `mensaje` no pueden estar vacíos.
- **Restricción de Tipo**: El campo `tipo` acepta únicamente los valores `"email"` o `"sms"`.
- **Formato del Destinatario**: Validaciones específicas de formato para correo electrónico (`user@domain.com`) y número de teléfono para SMS.

## ⚠️ Manejo de Errores
Todas las respuestas de error retornan una estructura JSON uniforme:
```json
{
  "error": "Descripción del error."
}
```

## 🗄️ Base de Datos
El microservicio gestiona su propia base de datos SQLite denominada `notificaciones.db`.
- **Tabla**: `notificaciones`
- **Creación de Tabla**: Automática mediante `db.create_all()` en el arranque del servicio.
- **Campos Mapeados**: `id`, `destinatario`, `tipo`, `asunto`, `mensaje`, `estado_envio`, `fecha`.

## 🧪 Cómo Ejecutar las Pruebas
Para validar el funcionamiento completo de la API mediante el cliente de pruebas de Flask:
```bash
python -c "from app import create_app; app = create_app(); client = app.test_client(); print('POST status:', client.post('/notificaciones', json={'destinatario': 'test@test.com', 'tipo': 'email', 'asunto': 'A', 'mensaje': 'M'}).status_code)"
```
