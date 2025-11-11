from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend (Vue)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "¡Hola Miguel Ángel! Tu servidor Flask funciona correctamente."})

if __name__ == "__main__":
    app.run(debug=True)
