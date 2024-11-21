from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from src.core.equipo.models import Empleado
from src.core.jya.models import Jinete


class RegistroCobroForm(FlaskForm):
    jinete = SelectField(
        "Jinete y Amazona", choices=[], coerce=int, validators=[DataRequired()]
    )
    fecha_pago = DateField(
        "Fecha de Pago", format="%Y-%m-%d", validators=[DataRequired()]
    )
    medio_pago = SelectField(
        "Medio de Pago",
        choices=[
            ("efectivo", "Efectivo"),
            ("tarjeta_credito", "Tarjeta de Crédito"),
            ("tarjeta_debito", "Tarjeta de Débito"),
        ],
        validators=[DataRequired()],
    )
    monto = DecimalField("Monto", validators=[DataRequired()])
    recibido_por = SelectField(
        "Recibido por", choices=[], coerce=int, validators=[DataRequired()]
    )
    observaciones = TextAreaField(
        "Observaciones (Opcional)", validators=[Optional(), Length(max=200)]
    )
    submit = SubmitField("Registrar Cobro")

    def __init__(self, *args, **kwargs):
        super(RegistroCobroForm, self).__init__(*args, **kwargs)
        self.jinete.choices = [
            (j.id, f"{j.nombre} {j.apellido}") for j in Jinete.query.all()
        ]
        self.recibido_por.choices = [
            (e.id, f"{e.nombre} {e.apellido}") for e in Empleado.query.all()
        ]
