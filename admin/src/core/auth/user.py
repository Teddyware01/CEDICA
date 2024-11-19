from src.core.database import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    alias = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    system_admin = db.Column(db.Boolean, default=False, nullable=False) 
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    roles = db.relationship("Roles", secondary="usuario_rol", back_populates="users")
    is_google_auth = db.Column(db.Boolean, default=False, nullable=False) #Debe usarse para los editar usuario, ya que no se puede editar la contraseña (sera null) si este es TRUE.
    is_accept_pending = db.Column(db.Boolean, default=False) #Los usuarios dados de alta con google arrancan en estado: PENDIENTE de ACEPTACION

    issues = db.relationship("Issue", back_populates="user")
    
   # empleado_id = db.Column(db.Integer, db.ForeignKey("empleado.id"), nullable=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey("empleado.id", ondelete="SET NULL"), nullable=True)
   
    empleado_asignado = db.relationship("Empleado", back_populates="usuario_asignado")

    contenido = db.relationship("Contenido", back_populates="autor_user")

    def __repr__(self):
        return f"<User #{self.id} email = {self.email}>"
