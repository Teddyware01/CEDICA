#  src/equipo/extra_models.py
from src.core.database import db


class ContactoEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(15), nullable=False, unique=True)


class Domicilio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False, unique=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    departamento = db.Column(db.Integer, nullable=False, unique=True)
    localidad = db.relationship(
        "Localidad", secondary="domicilio_localidad", back_populates="domicilio"
    )
    provincia = db.relationship(
        "Provincia", secondary="domicilio_provincia", back_populates="provincia"
    )


class ObraSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, unique=True)


class Localidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)


class Provincia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
