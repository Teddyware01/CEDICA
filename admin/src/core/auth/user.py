from src.core.database import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    alias = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    system_admin = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    roles = db.relationship("Roles", secondary="usuario_rol", back_populates="users")

    issues = db.relationship("Issue", back_populates="user")
    
    empleado_id = db.Column(db.Integer, db.ForeignKey("empleado.id"), nullable=True)
    empleado_asignado = db.relationship("Empleado", back_populates="usuario_asignado")

    def __repr__(self):
        return f"<User #{self.id} email = {self.email}>"
