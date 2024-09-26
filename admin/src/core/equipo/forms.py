from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from .models import CondicionEnum


#Todavia falta revisar si es la forma correcta de validar
class EmpleadoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    dni = StringField('DNI', validators=[DataRequired(), Length(max=11)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=15)])
    fecha_inicio = DateTimeField('Fecha de Inicio', validators=[DataRequired()])
    fecha_cese = DateTimeField('Fecha de Cese', validators=[])
    condicion = SelectField('Condición', choices=[(cond.name, cond.value) for cond in CondicionEnum], validators=[DataRequired()])
    activo = BooleanField('Activo')
    profesion_id = SelectField('Profesión', coerce=int, validators=[DataRequired()])
    puesto_laboral_id = SelectField('Puesto Laboral', coerce=int, validators=[DataRequired()])
    domicilio_id = SelectField('Domicilio', coerce=int, validators=[DataRequired()])
    contacto_emergencia_id = SelectField('Contacto de Emergencia', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')
