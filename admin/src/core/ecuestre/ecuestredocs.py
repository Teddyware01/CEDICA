from src.core.database import db
from datetime import datetime
from enum import Enum



    
    
class Ecuestre_docs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=True) #esto usa minio
    fecha_subida = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.String(100), nullable=True)
    is_enlace =  db.Column(db.Boolean, default=False, nullable=False)
    url_enlace = db.Column(db.String(255), nullable=True)
    nombre_asignado = db.Column(db.String(100), nullable=False) # esto escrito a mano

    ecuestre_id = db.Column(db.Integer, db.ForeignKey("ecuestre.id"), nullable=False)
    ecuestre = db.relationship("Ecuestre", back_populates="documentos")
