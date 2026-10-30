# Escáner de matrículas

Aplicación Flask para escanear códigos QR y de barras con la cámara del navegador y consultar los datos del alumno en SQLite.

## Requisitos y ejecución

Necesitas Python 3.10 o posterior. Instala Flask e inicia la aplicación:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Abre <http://127.0.0.1:5000>. La cámara requiere permiso del navegador y un contexto seguro: `localhost` funciona localmente; para acceder desde otro dispositivo, sirve la aplicación mediante HTTPS. La biblioteca de lectura de códigos se carga desde un CDN, por lo que el navegador necesita conexión a internet.

La aplicación crea `alumnos.sqlite3` junto a `main.py` y la tabla `alumnos` si aún no existen. Puedes elegir otro archivo con la variable de entorno `DATABASE_PATH`.

## Datos de alumnos

La tabla esperada tiene estas columnas:

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `matricula` | TEXT, clave primaria | Valor contenido en el código |
| `nombre` | TEXT | Nombre del alumno |
| `carrera` | TEXT | Carrera |
| `estatus` | TEXT | Estatus actual en la escuela |

Ejemplo para agregar un alumno:

```bash
sqlite3 alumnos.sqlite3 "INSERT INTO alumnos (matricula, nombre, carrera, estatus) VALUES ('123456', 'Nombre Apellido', 'Ingeniería', 'Activo');"
```

La ruta `POST /api/alumnos/consultar` recibe `{"matricula": "123456"}`. Devuelve los datos cuando existe; si no existe, responde con HTTP 404. La aplicación inicia ligada a `127.0.0.1`; no la expongas a una red pública sin añadir autenticación y controles de acceso.
