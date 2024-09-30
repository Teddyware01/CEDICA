from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    DateTimeField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length
from .models import CondicionEnum


# Todavia falta revisar si es la forma correcta de validar
class AddEmpleadoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=100)],
    )
    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(message="El apellido es obligatorio"),
            Length(max=100),
        ],
    )
    dni = StringField(
        "DNI",
        validators=[DataRequired(message="El DNI es obligatorio"), Length(max=11)],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El Email es obligatorio"),
            Email(),
            Length(max=255),
        ],
    )
    telefono = StringField(
        "Teléfono",
        validators=[DataRequired(message="El telefono es obligatorio"), Length(max=15)],
    )
    fecha_inicio = DateTimeField(
        "Fecha de Inicio",
        validators=[DataRequired(message="La fecha de inicio es obligatoria")],
    )
    fecha_cese = DateTimeField("Fecha de Cese", validators=[])
    condicion = SelectField(
        "Condición",
        choices=[(cond.name, cond.value) for cond in CondicionEnum],
        validators=[DataRequired(message="La condicion es obligatoria")],
    )
    activo = BooleanField("Activo", validators=[DataRequired()])
    profesion_id = SelectField(
        "Profesión",
        coerce=int,
        validators=[DataRequired(message="La profesion es obligatoria")],
    )
    puesto_laboral_id = SelectField(
        "Puesto Laboral",
        coerce=int,
        validators=[DataRequired(message="El puesto laboral es obligatorio")],
    )
    obra_social = StringField(
        "ObraSocial",
        validators=[
            DataRequired(message="El nombre de obra social es obligatorio"),
            Length(max=11),
        ],
    )
    nro_afiliado = IntegerField(
        "NroAfiliado",
        coerce=int,
        validators=[
            DataRequired(message="El numero de afiliado de obra social es obligatorio")
        ],
    )

    domicilio_calle = StringField("Calle", coerce=int, validators=[DataRequired()])
    domicilio_numero = IntegerField("Numero", coerce=int, validators=[DataRequired()])
    domicilio_departamento = IntegerField(
        "Departamento", coerce=int, validators=[DataRequired()]
    )
    domicilio_piso = IntegerField("Piso", coerce=int, validators=[DataRequired()])
    domicilio_localidad = SelectField(
        "Localidad", coerce=int, validators=[DataRequired()]
    )
    domicilio_provincia = SelectField(
        "Provincia", coerce=int, validators=[DataRequired()]
    )
    contacto_emergencia_nombre = StringField(
        "Nombre", validators=[DataRequired(), Length(max=100)]
    )
    contacto_emergencia_apellido = StringField(
        "Apellido", validators=[DataRequired(), Length(max=100)]
    )
    contacto_emergencia_telefono = StringField(
        "Teléfono", validators=[DataRequired(), Length(max=15)]
    )

    submit = SubmitField("Guardar")
