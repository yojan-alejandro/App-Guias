from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from models.instructor import Instructor

class Guia(Document):
    nombre = StringField(required=True)
    descripcion = StringField()
    programa_formacion = StringField(required=True)
    archivo_pdf = StringField(required=True)  
    fecha_publicacion = DateTimeField(default=datetime.utcnow)
    instructor = ReferenceField(Instructor, required=True)

    def __str__(self):
        return self.nombre
