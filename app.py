from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secreto123")  

app.config["MONGODB_SETTINGS"] = {
    "db": "PythonWebFlask",  
    "host": os.environ.get("URI")
}
app.config["UPLOAD_FOLDER"] = "./uploads"

db = MongoEngine(app)

from routes.rutas_autenticacion import auth_bp
from routes.rutas_guias import guia_bp

app.register_blueprint(auth_bp)
app.register_blueprint(guia_bp)

@app.route("/")
def home():
    return render_template("inicio.html")  

if __name__ == "__main__":
    print("🚀 Servidor Flask cargado correctamente.")
    app.run(port=5000, host="0.0.0.0", debug=True)
