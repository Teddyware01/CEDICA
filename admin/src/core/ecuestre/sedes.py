from src.core.database import db
from datetime import datetime



class Sedes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ecuestre = db.relationship("Ecuestre", back_populates="sede_asignada")


    def __repr__(self):
        return f"pepe"