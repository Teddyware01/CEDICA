from src.core.database import db

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)