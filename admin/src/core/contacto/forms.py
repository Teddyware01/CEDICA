from flask_wtf import FlaskForm
from wtforms import (SelectField, StringField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError, NumberRange
from .models import EstadoEnum

class AddConsultaForm(FlaskForm):
    
    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=100)],
    )
    
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El Email es obligatorio"),
            Length(max=255),
            Email(message="Ingrese un correo electrónico válido"),
        ],
    )
    
    mensaje = TextAreaField(
        Length(max=255), 
        validators=[Optional()],
    )
    
    estado = SelectField(
        "Estado",
        choices=[(est.name, est.value) for est in EstadoEnum],
        validators=[Optional()],
    )
    
    comentario = TextAreaField(
        Length(max=255), 
        validators=[Optional()],
    )
    
    submit = SubmitField("Guardar")
    
    