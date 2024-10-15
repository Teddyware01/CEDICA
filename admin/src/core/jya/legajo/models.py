from src.core.database import db
from datetime import datetime
from enum import Enum

class TipoDocumentoEnum(Enum):
    entrevista="entrevista"
    evaluacion="evaluacion"
    planificaciones="planificaciones"
    evolucion="evolución"
    cronicas="crónicas"
    documental="documental"
    
class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.Enum(TipoDocumentoEnum), nullable=False)
    
    jinete_id = db.Column(db.Integer, db.ForeignKey("jinete.id"), nullable=False)
    jinete = db.relationship("Jinete", back_populates="documentos")