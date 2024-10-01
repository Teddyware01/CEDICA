from src.core.database import db


permisos_rol = db.Table(
    "permisos_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permisos_id", db.Integer, db.ForeignKey("permisos.id"), primary_key=True),
)

class Permisos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    roles = db.relationship("Roles", secondary="permisos_rol", back_populates="permisos")