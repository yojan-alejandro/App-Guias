from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.instructor import Instructor
from utils.enviar_correo import enviar_correo
import random
import string

auth_bp = Blueprint("auth_bp", __name__)

def generar_credenciales(nombre):
    usuario = ''.join(nombre.lower().split()) + str(random.randint(100, 999))
    clave = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return usuario, clave

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        regional = request.form["regional"]

        existente = Instructor.objects(correo=correo).first()
        if existente:
            flash("Este correo ya está registrado.", "danger")
            return redirect(url_for("auth_bp.registro"))

        usuario, clave = generar_credenciales(nombre)
        nuevo = Instructor(
            nombre_completo=nombre,
            correo=correo,
            regional=regional,
            usuario=usuario,
            clave=clave
        )
        nuevo.save()

        exito = enviar_correo(correo, usuario, clave)

        if exito:
            flash(f"Registro exitoso. Se enviaron las credenciales al correo {correo}", "success")
        else:
            flash(f"Registro exitoso, pero ocurrió un error al enviar el correo.", "warning")

        return redirect(url_for("auth_bp.login"))

    return render_template("registro.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        instructor = Instructor.objects(usuario=usuario, clave=clave).first()
        if instructor:
            session["instructor_id"] = str(instructor.id)
            session["nombre"] = instructor.nombre_completo
            session["regional"] = instructor.regional
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("guia_bp.subir_guia"))
        else:
            flash("Credenciales inválidas", "danger")
            return redirect(url_for("auth_bp.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente", "info")
    return redirect(url_for("auth_bp.login"))
