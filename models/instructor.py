from flask_mongoengine import MongoEngine
from datetime import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField

class Instructor(Document):
    nombre_completo = StringField(required=True)
    correo = EmailField(required=True, unique=True)
    regional = StringField(required=True)
    usuario = StringField(required=True, unique=True)
    clave = StringField(required=True)
    fecha_registro = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.nombre_completo
