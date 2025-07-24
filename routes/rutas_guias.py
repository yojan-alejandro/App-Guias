from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory
from models.guia import Guia
from models.instructor import Instructor
import os
from werkzeug.utils import secure_filename
from datetime import datetime

guia_bp = Blueprint("guia_bp", __name__)

PROGRAMAS = [
    "Desarrollo de Software", "Multimedia", "Inteligencia Artificial",
    "Analítica de Datos", "Construcción", "Contabilidad"
]

def login_requerido(func):
    from functools import wraps
    @wraps(func)
    def wrapped(*args, **kwargs):
        if "instructor_id" not in session:
            flash("Debes iniciar sesión para continuar", "warning")
            return redirect(url_for("auth_bp.login"))
        return func(*args, **kwargs)
    return wrapped

@guia_bp.route("/subir_guia", methods=["GET", "POST"])
@login_requerido
def subir_guia():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        programa = request.form["programa_formacion"]
        archivo = request.files["archivo_pdf"]

        if archivo and archivo.filename.endswith(".pdf"):
            filename = secure_filename(f"{datetime.utcnow().timestamp()}_{archivo.filename}")
            ruta = os.path.join("uploads", filename)
            archivo.save(ruta)

            instructor = Instructor.objects.get(id=session["instructor_id"])

            guia = Guia(
                nombre=nombre,
                descripcion=descripcion,
                programa_formacion=programa,
                archivo_pdf=filename,
                instructor=instructor
            )
            guia.save()

            flash("Guía subida exitosamente", "success")
            return redirect(url_for("guia_bp.listar_guias"))
        else:
            flash("Debe subir un archivo en formato PDF", "danger")
            return redirect(url_for("guia_bp.subir_guia"))

    return render_template("subir_guia.html", programas=PROGRAMAS)

@guia_bp.route("/listar_guias")
@login_requerido
def listar_guias():
    guias = Guia.objects().order_by("-fecha_publicacion")
    return render_template("listar_guias.html", guias=guias)

@guia_bp.route("/ver_pdf/<nombre_archivo>")
@login_requerido
def ver_pdf(nombre_archivo):
    return send_from_directory("uploads", nombre_archivo)
