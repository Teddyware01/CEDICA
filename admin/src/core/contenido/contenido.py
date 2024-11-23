from datetime import datetime
from src.core.database import db
from enum import Enum


# Pueden haber mas o ser cambiados...
class TipoContenidoEnum(Enum):
    ARTICULO_INFO='Articulo informativo'
    PUBLICACION='Publicicacion'
    AVISO_EVENTO='Notificacion de evento'
    
class EstadoContenidoEnum(Enum):
    BORRADOR = 'Borrador'
    PUBLICADO = 'Publicado'
    ARCHIVADO = 'Archivado'

class Contenido(db.Model):
    __tablename__ = 'contenido'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(256), nullable=False, index=True)
    copete = db.Column(db.String(600), nullable=True)
    contenido = db.Column(db.Text, nullable=True)
    
    published_at = db.Column(db.DateTime, default=datetime.now, nullable=True) # Fecha en la que se publica, (imaginamos puede estar no publicado )
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
        
    tipo = db.Column(db.Enum(TipoContenidoEnum), default=TipoContenidoEnum.PUBLICACION)
    estado = db.Column(db.Enum(EstadoContenidoEnum), default=EstadoContenidoEnum.BORRADOR)
    
    autor_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    autor_user = db.relationship("Users", back_populates="contenido")

    def __repr__(self):
        return f"<Contenido #{self.id}, estado={self.estado.value}, titulo={self.titulo}>"

