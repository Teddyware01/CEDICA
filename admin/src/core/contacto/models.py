from datetime import datetime
from src.core.database import db
from enum import Enum

# Creo algunos estados. Despues armarlo bien.
class EstadoEnum(Enum):
    SIN_ATENDER = "Sin atender"
    EN_PROCESO = "En proceso"
    RESUELTO = "Resuelto"
    NINGUNO = "Ninguno"

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum(EstadoEnum), nullable=True, default="NINGUNO")
    comentario = db.Column(db.Text, nullable=True, default='')  
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    

    def __repr__(self):
        return f'<Contacto {self.nombre}>'
