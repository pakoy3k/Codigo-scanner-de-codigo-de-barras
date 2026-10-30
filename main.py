import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request


DEFAULT_DATABASE_PATH = Path(__file__).with_name("alumnos.sqlite3")


def create_app(database_path=None):
    app = Flask(__name__)
    app.config["DATABASE_PATH"] = str(
        database_path or os.environ.get("DATABASE_PATH", DEFAULT_DATABASE_PATH)
    )

    init_database(app.config["DATABASE_PATH"])

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/alumnos/consultar")
    def consultar_alumno():
        data = request.get_json(silent=True)
        matricula = data.get("matricula", "").strip() if isinstance(data, dict) else ""
        if not matricula:
            return jsonify(error="La matrícula es obligatoria."), 400

        try:
            with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
                connection.row_factory = sqlite3.Row
                alumno = connection.execute(
                    """
                    SELECT matricula, nombre, carrera, estatus
                    FROM alumnos
                    WHERE matricula = ?
                    """,
                    (matricula,),
                ).fetchone()
        except sqlite3.Error:
            app.logger.exception("No se pudo consultar la base de datos de alumnos.")
            return jsonify(error="No se pudo consultar la base de datos."), 500

        if alumno is None:
            return jsonify(existe=False, matricula=matricula), 404

        return jsonify(
            existe=True,
            alumno={
                "matricula": alumno["matricula"],
                "nombre": alumno["nombre"],
                "carrera": alumno["carrera"],
                "estatus": alumno["estatus"],
            },
        )

    return app


def init_database(database_path):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alumnos (
                matricula TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                carrera TEXT NOT NULL,
                estatus TEXT NOT NULL
            )
            """
        )


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
