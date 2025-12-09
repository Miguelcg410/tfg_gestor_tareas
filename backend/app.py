# app.py — Backend simple con Supabase REST API

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests
from urllib.parse import quote   # <<< NECESARIO PARA ENCODEAR EMAILS

# Configuración Supabase
from supabase_client import SUPABASE_URL, SUPABASE_HEADERS

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ================================================================
# FUNCIONES AUXILIARES
# ================================================================
def supabase_url(table, filters=None):
    base = f"{SUPABASE_URL}/rest/v1/{table}"
    if not filters:
        return base

    query = "&".join([f"{col}=eq.{val}" for col, val in filters.items()])
    return f"{base}?{query}"


# ================================================================
# RUTA TEST
# ================================================================
@app.route("/api")
def index():
    return jsonify({"mensaje": "API funcionando correctamente"}), 200


# ================================================================
# REGISTRO
# ================================================================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    if not nombre or not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # ENCODEAR EMAIL PARA CONSULTAR
    email_encoded = quote(email)

    # Verificar si ya existe
    url = f"{SUPABASE_URL}/rest/v1/usuarios?email=eq.{email_encoded}&select=*"
    print("URL CHECK REGISTER:", url)
    res = requests.get(url, headers=SUPABASE_HEADERS).json()

    if isinstance(res, list) and len(res) > 0 and res[0].get("email"):
        return jsonify({"error": "El correo ya está registrado"}), 400

    # Hashear contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Insertar usuario
    url = f"{SUPABASE_URL}/rest/v1/usuarios"
    nuevo = requests.post(url, headers=SUPABASE_HEADERS, json={
        "nombre": nombre,
        "email": email,
        "password": hashed_password,
        "rol": "usuario"
    }).json()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201


# ================================================================
# LOGIN
# ================================================================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # ENCODE EMAIL
    email_encoded = quote(email)

    # Buscar usuario
    url = f"{SUPABASE_URL}/rest/v1/usuarios?email=eq.{email_encoded}&select=*"

    print("LOGIN: URL ENVIADA:", url)
    res = requests.get(url, headers=SUPABASE_HEADERS).json()
    print("RESPUESTA SUPABASE:", res)

    if not isinstance(res, list) or len(res) == 0:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    usuario = res[0]

    # Verificar contraseña
    if not bcrypt.check_password_hash(usuario["password"], password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = create_access_token(identity=str(usuario["id"]))

    return jsonify({
        "mensaje": "Inicio de sesión correcto",
        "token": token,
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "rol": usuario["rol"]
        }
    }), 200


# ================================================================
# OBTENER TAREAS
# ================================================================
@app.route("/api/tareas", methods=["GET"])
@jwt_required()
def obtener_tareas():
    usuario_id = get_jwt_identity()

    url = supabase_url("tareas", {"usuario_id": usuario_id})
    res = requests.get(url, headers=SUPABASE_HEADERS).json()

    return jsonify(res), 200


# ================================================================
# CREAR TAREA
# ================================================================
@app.route("/api/tareas", methods=["POST"])
@jwt_required()
def crear_tarea():
    usuario_id = get_jwt_identity()
    data = request.json

    titulo = data.get("titulo")
    if not titulo:
        return jsonify({"error": "El título es obligatorio"}), 400

    url = f"{SUPABASE_URL}/rest/v1/tareas"
    nueva = requests.post(url, headers=SUPABASE_HEADERS, json={
        "titulo": titulo,
        "descripcion": data.get("descripcion"),
        "prioridad": data.get("prioridad", "media"),
        "fecha_limite": data.get("fecha_limite") or None,
        "usuario_id": usuario_id,
        "completada": False
    }).json()

    return jsonify(nueva), 201


# ================================================================
# ACTUALIZAR TAREA
# ================================================================
@app.route("/api/tareas/<int:tarea_id>", methods=["PUT"])
@jwt_required()
def actualizar_tarea(tarea_id):
    usuario_id = get_jwt_identity()
    data = request.json

    url = supabase_url("tareas", {"id": tarea_id, "usuario_id": usuario_id})
    existe = requests.get(url, headers=SUPABASE_HEADERS).json()

    if not existe:
        return jsonify({"error": "Tarea no encontrada o no autorizada"}), 404

    url = supabase_url("tareas", {"id": tarea_id})
    actualizado = requests.patch(url, headers=SUPABASE_HEADERS, json=data).json()

    return jsonify(actualizado), 200


# ================================================================
# ELIMINAR TAREA
# ================================================================
@app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
@jwt_required()
def eliminar_tarea(tarea_id):
    usuario_id = get_jwt_identity()

    url = supabase_url("tareas", {"id": tarea_id, "usuario_id": usuario_id})
    existe = requests.get(url, headers=SUPABASE_HEADERS).json()

    if not existe:
        return jsonify({"error": "Tarea no encontrada o no autorizada"}), 404

    url = supabase_url("tareas", {"id": tarea_id})
    requests.delete(url, headers=SUPABASE_HEADERS)

    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200


# ================================================================
# TAREAS POR FECHA
# ================================================================
@app.route("/api/tareas_por_fecha", methods=["GET"])
@jwt_required()
def tareas_por_fecha():
    usuario_id = get_jwt_identity()
    fecha = request.args.get("fecha")

    if not fecha:
        return jsonify({"error": "Falta la fecha"}), 400

    url = supabase_url("tareas", {
        "usuario_id": usuario_id,
        "fecha_limite": fecha
    })

    res = requests.get(url, headers=SUPABASE_HEADERS).json()

    return jsonify(res), 200


# ================================================================
# EJECUCIÓN
# ================================================================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
