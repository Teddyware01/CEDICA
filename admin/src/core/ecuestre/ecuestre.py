from src.core.database import db
from datetime import datetime


empleado_ecuestre = db.Table(
    "empleado_ecuestre",
    db.Column("ecuestre_id", db.Integer, db.ForeignKey("ecuestre.id"), primary_key=True),
    db.Column("empleado_id", db.Integer, db.ForeignKey("empleado.id"), primary_key=True),
)



class Ecuestre (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.Boolean, nullable=False)    #true macho false hembra
    raza = db.Column(db.String(255), nullable=False)
    pelaje = db.Column(db.String(255), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    sede_asignada = db.relationship("Sedes", back_populates="ecuestre")
    empleado = db.relationship("Empleado", secondary="empleado_ecuestre", back_populates="ecuestre")

    def __repr__(self):
        return f"{self.id} nombre: {self.nombre}"

    
   