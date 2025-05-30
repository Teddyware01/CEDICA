#  src/equipo/models.py
from src.core.database import db
from datetime import datetime
from enum import Enum


class CondicionEnum(Enum):
    VOLUNTARIO = "Voluntario"
    PERSONAL_RENTADO = "Personal Rentado"



class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=False)
    apellido = db.Column(db.String(100), nullable=False, unique=False)
    dni = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False, unique=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    condicion = db.Column(db.Enum(CondicionEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    obra_social = db.Column(db.String(25), nullable=False, unique=False)
    nro_afiliado = db.Column(db.String(25), nullable=False, unique=False)
    esta_borrado = db.Column(db.Boolean, default=False)

    # campos id
    profesion_id = db.Column(db.Integer, db.ForeignKey("profesion.id"), nullable=False)
    puesto_laboral_id = db.Column(
        db.Integer, db.ForeignKey("puesto_laboral.id"), nullable=False
    )
    domicilio_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=False)
    contacto_emergencia_id = db.Column(
        db.Integer, db.ForeignKey("contacto_emergencia.id"), nullable=False
    )

    # relaciones
    usuario_asignado = db.relationship("Users", back_populates="empleado_asignado")
    profesion = db.relationship("Profesion", back_populates="empleado")
    puesto_laboral = db.relationship("PuestoLaboral", back_populates="empleado")
    domicilio = db.relationship("Domicilio", back_populates="empleado")
    ecuestre = db.relationship("Ecuestre", secondary="empleado_ecuestre", back_populates="empleado")
    contacto_emergencia = db.relationship(
        "ContactoEmergencia",
        back_populates="empleado",
    )

    documentos = db.relationship("Empleado_docs", back_populates="empleado", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Empleado #{self.id}. AyN = {self.apellido}, {self.nombre}. Email = {self.email}. DNI = {self.dni}>"


class Profesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    empleado = db.relationship("Empleado", back_populates="profesion")


class PuestoLaboral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    empleado = db.relationship("Empleado", back_populates="puesto_laboral")





class TiposDocumentosEnum(Enum):
    TITULO = "Titulo"
    COPIA_DNI = "Copia DNI"
    CV_ACTUALIZADO = "CV actualizado"



class Empleado_docs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_asignado = db.Column(db.String(100), nullable=False) # esto escrito a mano
    titulo = db.Column(db.String(100), nullable=True) #este va en minio
    fecha_subida = db.Column(db.DateTime, default=datetime.now)
    tipo_documento = db.Column(db.Enum(TiposDocumentosEnum), nullable=True)
    is_enlace =  db.Column(db.Boolean, default=False, nullable=False)
    url_enlace = db.Column(db.String(255), nullable=True)

    empleado_id = db.Column(db.Integer, db.ForeignKey("empleado.id"), nullable=False)
    empleado = db.relationship("Empleado", back_populates="documentos")
