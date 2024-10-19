from src.core.database import db

class RegistroCobro(db.Model):
    __tablename__ = 'registro_cobros'
    
    id = db.Column(db.Integer, primary_key=True)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    medio_pago = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    recibido_por = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    
    jinete = db.relationship("Jinete", backref="cobros")
    empleado = db.relationship("Empleado", foreign_keys=[recibido_por], backref="cobros_recibidos")
