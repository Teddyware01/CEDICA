from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from src.core.equipo.models import Empleado
from src.core.jinetes.models import Jinete

class RegistroCobroForm(FlaskForm):
    # Campo para seleccionar el Jinete o Amazona
    jinete_id = SelectField("Jinete o Amazona", choices=[], coerce=int, validators=[DataRequired()])

    # Fecha del Pago
    fecha_pago = DateField("Fecha de Pago", format='%Y-%m-%d', validators=[DataRequired()])

    # Medio de Pago
    medio_pago = SelectField("Medio de Pago", 
                             choices=[('efectivo', 'Efectivo'), 
                                      ('tarjeta_credito', 'Tarjeta de Crédito'), 
                                      ('tarjeta_debito', 'Tarjeta de Débito')],
                             validators=[DataRequired()])

    # Monto del Pago
    monto = DecimalField("Monto", validators=[DataRequired()])

    # Campo para seleccionar el empleado que recibe el dinero
    recibido_por = SelectField("Recibido por", choices=[], coerce=int, validators=[DataRequired()])

    # Observaciones
    observaciones = TextAreaField("Observaciones", validators=[Optional()])

    # Estado de Pago: Al día o En deuda
    estado_pago = SelectField("Estado del Pago", 
                              choices=[('al_dia', 'Al día'), 
                                       ('en_deuda', 'En deuda')],
                              validators=[DataRequired()])

    # Botón de Submit
    submit = SubmitField("Registrar Cobro")

    def __init__(self, *args, **kwargs):
        super(RegistroCobroForm, self).__init__(*args, **kwargs)
        # Cargar los Jinetes y Empleados desde la base de datos
        self.jinete_id.choices = [(j.id, f"{j.nombre} {j.apellido}") for j in Jinete.query.all()]
        self.recibido_por.choices = [(e.id, f"{e.nombre} {e.apellido}") for e in Empleado.query.all()]
