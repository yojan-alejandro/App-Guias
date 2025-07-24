import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(destinatario, usuario, clave):
    emisor = os.getenv("CORREO_EMISOR")
    clave_emisor = os.getenv("CLAVE_CORREO")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Credenciales de acceso - App Guías SENA"
    mensaje["From"] = emisor
    mensaje["To"] = destinatario

    mensaje.set_content(f"""
    ¡Hola!

    Te has registrado exitosamente en la aplicación web de guías del SENA.

    Estas son tus credenciales de acceso:

    Usuario: {usuario}
    Contraseña: {clave}

    Puedes iniciar sesión en: http://localhost:5000/login

    Saludos,
    Equipo de Desarrollo SENA
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(emisor, clave_emisor)
            smtp.send_message(mensaje)
        return True
    except Exception as e:
        print("❌ Error al enviar correo:", e)
        return False
