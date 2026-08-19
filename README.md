# Microservicio de Notificaciones (`microservicio-notificaciones`)

## 📋 Descripción
`microservicio-notificaciones` es un microservicio backend independiente desarrollado en Python con Flask y SQLAlchemy. Incluye un **Frontend Web interactivo** y una **API REST independiente con CRUD completo** para gestionar y simular el envío de comunicaciones (email/SMS) con registro de auditoría en una base de datos SQLite persistente.

## 🎯 Objetivo del Microservicio
Proporcionar una solución desacoplada que administre el ciclo de vida completo (**Create, Read, Update, Delete**) de las notificaciones del sistema, garantizando la validación estricta de datos, la auditoría de envíos y una interfaz web para interactuar y realizar pruebas en vivo.

## 🏛️ Arquitectura
El microservicio implementa una arquitectura modular en capas basada en los patrones **Application Factory** y **Blueprints** de Flask:

- **Capa de Interfaz (Frontend Web)**: Dashboard interactivo Single-Page Application (HTML5, CSS3, JS Vanilla con `fetch API`).
- **Capa de Transporte (Routes/Controllers)**: API REST desacoplada que gestiona peticiones HTTP (`GET`, `POST`, `PUT`, `DELETE`).
- **Capa de Negocio (Services & Utils)**: Reglas de negocio, simulación de envíos, transacciones con rollback y validaciones.
- **Capa de Acceso a Datos (Models)**: Mapeo objeto-relacional mediante SQLAlchemy.
- **Capa de Persistencia**: Archivo de base de datos SQLite independiente (`notificaciones.db`).

![Diagrama de Arquitectura](diagrams/arquitectura.png)

## 🛠️ Tecnologías Utilizadas
- **Lenguaje**: Python 3.x
- **Framework Web**: Flask
- **ORM**: Flask-SQLAlchemy / SQLAlchemy
- **Base de Datos**: SQLite 3
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism Dark Mode), JavaScript Nativo (AJAX / Fetch API)

## 📁 Estructura del Proyecto
```text
microservicio-notificaciones/
│
├── app/
│   ├── __init__.py           # Inicialización de Flask, Blueprints y SQLAlchemy
│   ├── config.py             # Configuración base del microservicio y URI de SQLite
│   ├── models/
│   │   └── notificacion.py   # Modelo ORM Notificacion
│   ├── routes/
│   │   ├── frontend.py       # Blueprint para servir la interfaz Web UI (GET /)
│   │   └── notificaciones.py # Blueprint y controladores de la API REST CRUD
│   ├── services/
│   │   └── notificacion_service.py # Lógica de negocio (Crear, Listar, Actualizar, Eliminar)
│   ├── static/
│   │   ├── css/styles.css    # Estilos visuales del Frontend
│   │   └── js/main.js        # Lógica cliente y consumo asíncrono de la API REST
│   ├── templates/
│   │   └── index.html        # Plantilla del Dashboard interactivo
│   └── utils/
│       └── validators.py     # Validaciones de entrada y restricción de tipos
│
├── diagrams/
│   └── arquitectura.png      # Diagrama de arquitectura del microservicio
├── .gitignore                # Archivos excluidos en control de versiones
├── app.py                    # Punto de entrada para ejecutar el microservicio
└── requirements.txt          # Dependencias del proyecto
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

## 🚀 Ejecución Local

Para iniciar el servidor del microservicio en `http://localhost:5000`:
```bash
python app.py
```

- **Frontend Web (Dashboard de Pruebas)**: Abre en tu navegador `http://localhost:5000/`
- **API REST**: `http://localhost:5000/notificaciones`

---

## 📡 Documentación de Endpoints (API REST CRUD)

### 1. Crear Notificación (`POST /notificaciones`)
Valida, simula el envío y registra una nueva comunicación.
- **Body Request**:
  ```json
  {
    "destinatario": "usuario@ejemplo.com",
    "tipo": "email",
    "asunto": "Bienvenida",
    "mensaje": "Hola, bienvenido al sistema."
  }
  ```
- **Respuesta (`201 Created`)**: Objeto JSON con la notificación registrada (`id`, `estado_envio: "ENVIADO"`, `fecha`).

### 2. Listar Notificaciones (`GET /notificaciones`)
- `GET /notificaciones`: Devuelve el listado completo de notificaciones registradas (`200 OK`).
- `GET /notificaciones?destinatario=X`: Filtra las notificaciones por el destinatario especificado (`200 OK`).

### 3. Consultar por ID (`GET /notificaciones/{id}`)
Retorna los detalles de una notificación específica (`200 OK` o `404 Not Found`).

### 4. Actualizar Notificación (`PUT /notificaciones/{id}`)
Actualiza los campos `destinatario`, `tipo`, `asunto` y `mensaje` de una notificación existente.
- **Body Request**:
  ```json
  {
    "destinatario": "+573001234567",
    "tipo": "sms",
    "asunto": "Alerta Corregida",
    "mensaje": "Mensaje de texto actualizado."
  }
  ```
- **Respuesta (`200 OK`)**: Objeto JSON actualizado.

### 5. Eliminar Notificación (`DELETE /notificaciones/{id}`)
Elimina permanentemente el registro de auditoría de la base de datos SQLite.
- **Respuesta (`200 OK`)**: `{"mensaje": "Notificación con ID X eliminada exitosamente."}`
- **Respuesta (`404 Not Found`)**: `{"error": "La notificación con el ID X no fue encontrada."}`

---

## 🖥️ Interfaz Web (Frontend Integrado)
El microservicio incluye un **Dashboard Web** cargado al abrir `http://localhost:5000/` que permite:
1. **Formulario de Envío**: Probar la creación de notificaciones por Email y SMS en tiempo real (`POST`).
2. **Tabla de Auditoría**: Visualizar todas las notificaciones registradas en la base de datos SQLite (`GET`).
3. **Filtro Dinámico**: Buscar por destinatario en vivo.
4. **Edición Inline**: Modificar notificaciones existentes mediante un modal interactivo (`PUT`).
5. **Eliminación**: Remover registros directamente desde la interfaz con confirmación (`DELETE`).
6. **Métricas en Vivo**: Contadores automáticos de notificaciones totales, por Email y por SMS.

---

## 🚦 Códigos HTTP Utilizados
- `200 OK`: Petición procesada exitosamente (`GET`, `PUT`, `DELETE`).
- `201 Created`: Notificación creada y registrada exitosamente (`POST`).
- `400 Bad Request`: Petición malformada, JSON ausente o error de validación en campos.
- `404 Not Found`: Notificación solicitada por ID no existe en la base de datos.
- `500 Internal Server Error`: Error interno del servidor.

## 🗄️ Base de Datos Persistente
- **Archivo SQLite**: `notificaciones.db`
- **Tabla**: `notificaciones` (creada automáticamente mediante `db.create_all()`).
- **Persistencia**: Todos los cambios (creación, edición, eliminación) se conservan físicamente en el disco.
