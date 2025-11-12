from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Crear la app Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Inicializar extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ======= MODELOS =======

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="usuario")  # 'usuario' o 'admin'
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
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "completada": self.completada,
            "usuario_id": self.usuario_id
        }

# ======= RUTA DE PRUEBA =======
@app.route("/api")
def index():
    return jsonify({"mensaje": "API del Gestor de Tareas funcionando correctamente."})

# ======= EJECUTAR SERVIDOR =======
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
    app.run(debug=True)
