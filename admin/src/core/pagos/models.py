from src.core.database import db
from datetime import datetime


class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    beneficiario = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime)
    tipo_pago = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Pago {self.beneficiario} - {self.monto}>'
