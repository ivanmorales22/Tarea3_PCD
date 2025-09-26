# Tarea3_PCD
Repositorio creado para realizar la Tarea 3 correspondiende a la creacion de una API REST de FastAPI

FastAPI User CRUD API
Este proyecto es una API RESTful simple para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos de usuarios. Está construida con FastAPI para el servidor web, Pydantic para la validación de datos y SQLAlchemy para la interacción con la base de datos.

La API está protegida y requiere una clave (API Key) para acceder a los endpoints.

✨ Características
Operaciones CRUD completas: Funcionalidad para crear, leer, actualizar y eliminar usuarios.

Validación de Datos: Utiliza modelos Pydantic para garantizar que los datos de entrada sean válidos.

Seguridad: Endpoints protegidos mediante una API Key que debe ser enviada en el header X-API-Key.

Base de Datos: Integración con SQLAlchemy para persistencia de datos y creación automática de tablas.

Documentación Interactiva: Generación automática de documentación interactiva (Swagger UI y ReDoc) gracias a FastAPI.

🚀 Instalación y Puesta en Marcha
Sigue estos pasos para poner en funcionamiento el proyecto en tu entorno local.

Prerrequisitos
Python 3.8+

Un gestor de paquetes como pip

Pasos
Clona el repositorio (si aplica)

Bash

git clone <url-del-repositorio>
cd <nombre-del-directorio>
Crea un entorno virtual y actívalo

Bash

# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
Instala las dependencias
Crea un archivo requirements.txt con el siguiente contenido:

fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-dotenv
Luego, instálalo:

Bash

pip install -r requirements.txt
Configura las variables de entorno
Crea un archivo llamado .env en la raíz del proyecto y añade tu clave de API:

Fragmento de código

API_KEY="TU_CLAVE_SECRETA_AQUI"
Reemplaza "TU_CLAVE_SECRETA_AQUI" con una clave segura de tu elección.

Ejecuta la aplicación
Usa uvicorn para iniciar el servidor:

Bash

uvicorn main:app --reload
El flag --reload reiniciará el servidor automáticamente cada vez que hagas cambios en el código.

Accede a la API

La API estará disponible en: http://127.0.0.1:8000

La documentación interactiva (Swagger UI) estará en: http://127.0.0.1:8000/docs

📖 Uso de la API
Para interactuar con los endpoints, debes incluir tu clave de API en el header X-API-Key.

Endpoints Disponibles
Método	Endpoint	Descripción
POST	/api/v1/users/	Crea un nuevo usuario.
GET	/api/v1/users/{user_id}	Lista todos los usuarios de la base de datos.
PUT	/api/v1/users/{user_id}	Actualiza un usuario existente por su ID.
DELETE	/api/v1/users/{user_id}	Elimina un usuario por su ID.
GET	/api/v1/secure-data/	Endpoint de prueba para validar la API Key.

Exportar a Hojas de cálculo
Ejemplo de Petición (usando cURL)
Aquí tienes un ejemplo de cómo crear un nuevo usuario usando cURL desde la terminal.

Bash

curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: TU_CLAVE_SECRETA_AQUI' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "John Doe",
  "user_id": 101,
  "user_email": "john.doe@example.com",
  "age": 30,
  "recommendations": [
    "product_a",
    "product_b"
  ],
  "zip": 12345
}'
⚠️ Puntos a Mejorar en el Código
El código proporcionado es funcional, pero se han identificado algunas áreas de mejora para hacerlo más robusto y correcto:

Endpoint GET /api/v1/users/{user_id}:

Problema: Actualmente, este endpoint no usa el user_id de la URL y devuelve una lista de todos los usuarios.

Solución: Debería modificarse para aceptar user_id como parámetro y filtrar por ese ID para devolver un único usuario.

Filtrado en PUT y DELETE:

Problema: En las funciones update_user y delete_user, el filtro models.User.user == user_id parece incorrecto. El modelo User probablemente no tiene un campo llamado user.

Solución: Debería ser models.User.user_id == user_id (o el nombre del campo que corresponda a la clave primaria en tu modelo de SQLAlchemy).

Actualización de recommendations en PUT:

Problema: En update_user, la línea db_user.recommendations = users.recommendations asigna una lista de Python a un campo que probablemente es de tipo String en la base de datos. Esto causará un error.

Solución: Debería convertirse la lista a una cadena, igual que en la función create_user: db_user.recommendations = ",".join(users.recommendations).