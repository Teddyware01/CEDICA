from src.core.database import db
from datetime import datetime

class RegistroCobro(db.Model):
    __tablename__ = 'registro_cobros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    medio_pago = db.Column(db.String(50), nullable=False)  
    monto = db.Column(db.Float, nullable=False)
    recibido_por = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)  
    observaciones = db.Column(db.Text, nullable=True)
    estado_pago = db.Column(db.String(50), nullable=False, default="Al día")

    # Relaciones del modulo con jinetes y amazonas
    jinete = db.relationship('Jinete', backref='cobros')
    empleado = db.relationship('Empleado', backref='cobros_recibidos')

    def __repr__(self):
        return f'<RegistroCobro ID: {self.id}, Jinete: {self.jinete_id}, Monto: {self.monto}>'
