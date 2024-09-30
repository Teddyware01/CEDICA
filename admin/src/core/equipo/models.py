#  src/equipo/models.py
from src.core.database import db
from datetime import datetime
from enum import Enum


class CondicionEnum(Enum):
    VOLUNTARIO = "Voluntario"
    PERSONAL_RENTADO = "Personal Rentado"


class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    apellido = db.Column(db.String(100), nullable=False, unique=True)
    dni = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    condicion = db.Column(db.Enum(CondicionEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    obra_social = db.Column(db.String(25), nullable=False, unique=False)
    nro_afiliado = db.Column(db.Integer, nullable=False)
    profesion_id = db.Column(db.Integer, db.ForeignKey("profesion.id"), nullable=False)
    puesto_laboral_id = db.Column(
        db.Integer, db.ForeignKey("puesto_laboral.id"), nullable=False
    )
    domicilio_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=False)

    contacto_emergencia_id = db.Column(
        db.Integer, db.ForeignKey("contacto_emergencia.id"), nullable=False
    )
    obra_social_id = db.Column(
        db.Integer, db.ForeignKey("obra_social_id.id"), nullable=False
    )

    profesion = db.relationship("Profesion", back_populates="empleado")
    puesto_laboral = db.relationship("PuestoLaboral", back_populates="empleado")
    domicilio = db.relationship(
        "Domicilio", secondary="empleado_domicilio", back_populates="empleado"
    )

    contacto_emergencia = db.relationship(
        "ContactoEmergencia",
        secondary="empleado_contacto_emergencia",
        back_populates="empleados",
    )

    def __repr__(self):
        return f"<Empleado #{self.id}. AyN = {self.apellido}, {self.nombre}. Email = {self.email}>"


empleado_domicilio = db.Table(
    "empleado_domicilio",
    db.Column("empleado_id", db.Integer, db.ForeignKey("empleado.id")),
    db.Column("domicilio_id", db.Integer, db.ForeignKey("domicilio.id")),
)

# Tabla intermedia para la relación muchos a muchos entre Empleado y ContactoEmergencia
empleado_contacto_emergencia = db.Table(
    "empleado_contacto_emergencia",
    db.Column(
        "empleado_id", db.Integer, db.ForeignKey("empleado.id"), primary_key=True
    ),
    db.Column(
        "contacto_emergencia_id",
        db.Integer,
        db.ForeignKey("contacto_emergencia.id"),
        primary_key=True,
    ),
)


class Profesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    empleado = db.relationship("Empleado", back_populates="profesion")


class PuestoLaboral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    empleado = db.relationship("Empleado", back_populates="puesto_laboral")
