from src.core.database import db



usuario_rol = db.Table(
    "usuario_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    users = db.relationship("Users", secondary="usuario_rol", back_populates="roles")
    permisos = db.relationship("Permisos", secondary="permisos_rol", back_populates="roles")
    def __repr__(self):
        return f"<Rol #{self.id} nombre = {self.nombre}>"



