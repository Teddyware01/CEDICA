from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from src.core.equipo.models import Empleado  


class PagoForm(FlaskForm):
    beneficiario = SelectField("Beneficiario (Empleado)", choices=[], coerce=int, validators=[Optional()])
    otro_beneficiario = StringField("Otro Beneficiario", validators=[DataRequired(), Length(max=100)])
    monto = DecimalField("Monto", validators=[DataRequired()])
    fecha_pago = DateField("Fecha de Pago", format='%Y-%m-%d', validators=[DataRequired()])
    
    tipo_pago = SelectField("Tipo de Pago", 
                            choices=[('honorario', 'Honorario'), 
                                     ('proveedor', 'Proveedor'), 
                                     ('gastos_varios', 'Gastos Varios')],
                            validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[Length(max=200)])
    submit = SubmitField("Registrar Pago")

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        self.beneficiario.choices = [(empleado.id, f"{empleado.nombre} {empleado.apellido}") for empleado in Empleado.query.all()]

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self, extra_validators=extra_validators):
            return False
        
        if self.tipo_pago.data != 'honorario' and not self.otro_beneficiario.data:
            self.otro_beneficiario.errors.append("Debe ingresar un beneficiario si no es un pago de honorarios.")
            return False
        
        return True