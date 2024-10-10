from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PagoForm(FlaskForm):
    beneficiario = StringField("Beneficiario", validators=[DataRequired(), Length(max=100)])
    monto = DecimalField("Monto", validators=[DataRequired()])
    fecha_pago = DateField("Fecha de Pago", format='%Y-%m-%d', validators=[DataRequired()])
    tipo_pago = SelectField("Tipo de Pago", 
                            choices=[('honorarios', 'Honorarios'), 
                                     ('proveedor', 'Proveedor'), 
                                     ('gastos_varios', 'Gastos Varios')],
                            validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[Length(max=200)])
    submit = SubmitField("Registrar Pago")
