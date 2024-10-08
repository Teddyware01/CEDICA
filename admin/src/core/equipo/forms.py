from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    DateTimeField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from wtforms.widgets import DateInput
from .models import CondicionEnum


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
        validators=[
            DataRequired(message="El DNI es obligatorio"),
            Length(max=11),
            Regexp(r"^\d+$", message="El DNI debe contener solo números"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El Email es obligatorio"),
            Length(max=255),
        ],
    )
    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio"),
            Length(max=15),
            Regexp(r"^\d+$", message="El teléfono debe contener solo números"),
        ],
    )
    fecha_inicio = DateTimeField(
        "Fecha de Inicio",
        format="%Y-%m-%d",  # Especificar el formato aquí
        validators=[DataRequired(message="La fecha de inicio es obligatoria")],
        widget=DateInput(),  # Widget para la selección de fecha
    )

    fecha_cese = DateTimeField(
        "Fecha de Cese",
        format="%Y-%m-%d",  # Especificar el formato aquí
        widget=DateInput(),
        validators=[Optional()],
    )

    condicion = SelectField(
        "Condición",
        choices=[(cond.name, cond.value) for cond in CondicionEnum],
        validators=[DataRequired(message="La condición es obligatoria")],
    )
    activo = BooleanField("Activo")

    profesion_id = SelectField(
        "Profesión",
        coerce=int,
        validators=[DataRequired(message="La profesión es obligatoria")],
    )
    puesto_laboral_id = SelectField(
        "Puesto Laboral",
        coerce=int,
        validators=[DataRequired(message="El puesto laboral es obligatorio")],
    )

    obra_social = StringField(
        "Obra Social",
        validators=[
            DataRequired(message="El nombre de obra social es obligatorio"),
            Length(max=100),  # Cambiado a 100 por consistencia
        ],
    )
    nro_afiliado = IntegerField(
        "Número Afiliado",
        validators=[
            DataRequired(message="El número de afiliado de obra social es obligatorio")
        ],
    )

    domicilio_calle = StringField("Calle", validators=[DataRequired()])
    domicilio_numero = IntegerField("Número", validators=[DataRequired()])
    domicilio_departamento = IntegerField("Departamento", validators=[DataRequired()])
    domicilio_piso = IntegerField("Piso", validators=[DataRequired()])

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
