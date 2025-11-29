from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ========================
# MODELOS
# ========================

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="usuario")
    tareas = db.relationship("Tarea", backref="usuario", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol
        }


class Tarea(db.Model):
    __tablename__ = "tareas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    completada = db.Column(db.Boolean, default=False)
    prioridad = db.Column(db.String(10), default="media")
    fecha_limite = db.Column(db.String(20), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "completada": self.completada,
            "prioridad": self.prioridad,
            "fecha_limite": self.fecha_limite,
            "usuario_id": self.usuario_id
        }


# ========================
# RUTAS API
# ========================

@app.route("/api")
def index():
    return jsonify({"mensaje": "API funcionando correctamente"})


# ----------- REGISTRO -----------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    if not nombre or not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201


# ----------- LOGIN -----------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not bcrypt.check_password_hash(usuario.password, password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = create_access_token(identity=usuario.id)

    return jsonify({
        "mensaje": "Inicio de sesión correcto",
        "token": token,
        "usuario": usuario.to_dict()
    }), 200


# ================================
#   CRUD DE TAREAS SIN JWT
#   (totalmente desbloqueado por ahora)
# ================================

# ----- OBTENER TAREAS -----
@app.route("/api/tareas", methods=["GET"])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([t.to_dict() for t in tareas]), 200


# ----- CREAR TAREA -----
@app.route("/api/tareas", methods=["POST"])
def crear_tarea():
    data = request.get_json()

    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    prioridad = data.get("prioridad")
    fecha_limite = data.get("fecha_limite")
    usuario_id = data.get("usuario_id", 1)  # Temporal: usuario #1

    if not titulo:
        return jsonify({"error": "El título es obligatorio"}), 400

    nueva_tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        prioridad=prioridad,
        fecha_limite=fecha_limite,
        usuario_id=usuario_id
    )

    db.session.add(nueva_tarea)
    db.session.commit()

    return jsonify({"mensaje": "Tarea creada correctamente"}), 201


# ----- ACTUALIZAR TAREA -----
@app.route("/api/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    tarea = Tarea.query.filter_by(id=tarea_id).first()

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.get_json()

    tarea.titulo = data.get("titulo", tarea.titulo)
    tarea.descripcion = data.get("descripcion", tarea.descripcion)
    tarea.completada = data.get("completada", tarea.completada)
    tarea.prioridad = data.get("prioridad", tarea.prioridad)
    tarea.fecha_limite = data.get("fecha_limite", tarea.fecha_limite)

    db.session.commit()
    return jsonify({"mensaje": "Tarea actualizada correctamente"}), 200


# ----- ELIMINAR TAREA -----
@app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.filter_by(id=tarea_id).first()

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(tarea)
    db.session.commit()

    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200

# ======= TAREAS POR FECHA (para el Calendario) =======
@app.route("/api/tareas_por_fecha", methods=["GET"])
def tareas_por_fecha():
    fecha = request.args.get("fecha")  # formato YYYY-MM-DD

    if not fecha:
        return jsonify({"error": "Falta la fecha"}), 400

    # Buscar tareas cuya fecha limite coincida con el día seleccionado
    tareas = Tarea.query.filter_by(fecha_limite=fecha).all()

    return jsonify([t.to_dict() for t in tareas]), 200

# ========================
# EJECUCIÓN
# ========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
