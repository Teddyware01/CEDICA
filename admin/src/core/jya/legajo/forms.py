from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateTimeField,
)
from wtforms.validators import DataRequired,Regexp, ValidationError, Length
from wtforms.widgets import DateInput
from src.core.jya.models import TipoDocumentoEnum

class AddDocumentoForm(FlaskForm):
    titulo = StringField(
        "Titulo",
        validators=[DataRequired(message="El titulo es obligatorio"), Length(max=100)],
    )
    
    fecha_subida = DateTimeField(
        "Fecha de subida",
        format="%Y-%m-%d",
        widget=DateInput()
    )
    
    tipo = SelectField(
        "Tipo",
        choices=[(tipo.name, tipo.value) for tipo in TipoDocumentoEnum],
        validators=[DataRequired(message="El tipo de documento es obligatorio")],
    )