#  src/equipo/extra_models.py
from src.core.database import db


class ContactoEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(15), nullable=False, unique=False)

    empleado = db.relationship("Empleado", back_populates="contacto_emergencia")
    jinete = db.relationship("Jinete", back_populates="contacto_emergencia")


class Domicilio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False, unique=False)
    numero = db.Column(db.Integer, nullable=False, unique=False)
    departamento = db.Column(db.String(10), nullable=True, unique=False) # !!!!! cambie a string
    piso = db.Column(db.Integer, nullable=True, unique=False)
    localidad_id = db.Column(db.Integer, db.ForeignKey("localidad.id"), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), nullable=False)
    provincia = db.relationship("Provincia", backref="domicilios")

    localidad = db.relationship("Localidad", backref="domicilios")

    empleado = db.relationship("Empleado", back_populates="domicilio")
    jinetes = db.relationship("Jinete", foreign_keys="Jinete.domicilio_id", back_populates="domicilio")
    

class Localidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), nullable=False)
    provincia = db.relationship("Provincia", backref="localidad")
    
    jinetes = db.relationship("Jinete", foreign_keys="Jinete.localidad_nacimiento_id", back_populates="localidad_nacimiento")
    familiares = db.relationship("Familiar", back_populates="localidad_familiar")

class Provincia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)

    jinetes = db.relationship("Jinete", foreign_keys="Jinete.provincia_nacimiento_id", back_populates="provincia_nacimiento")
    familiares = db.relationship("Familiar", back_populates="provincia_familiar")