#  src/equipo/extra_models.py
from src.core.database import db


class ContactoEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(15), nullable=False, unique=True)

    empleados = db.relationship(
        "Empleado",
        secondary="empleado_contacto_emergencia",
        back_populates="contacto_emergencia",
    )


from src.core.database import db


class Domicilio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False, unique=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    departamento = db.Column(db.Integer, nullable=False, unique=True)
    piso = db.Column(db.Integer, nullable=False, unique=True)
    localidad_id = db.Column(db.Integer, db.ForeignKey("localidad.id"), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), nullable=False)

    localidad = db.relationship("Localidad", backref="domicilios")
    provincia = db.relationship("Provincia", backref="domicilios")

    empleado = db.relationship("Empleado", back_populates="domicilio")


class Localidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)


class Provincia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
