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
from .models import PensionEnum, DiagnosticoEnum

class AddJineteForm(FlaskForm):
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
    edad = StringField(
        "Edad",
        validators=[
            DataRequired(message="La edad es obligatoria"),
            Length(max=3),
            Regexp(r"^\d+$", message="La edad debe contener solo números"),
        ],
    )
    
    fecha_nacimiento = DateTimeField(
        "Fecha de Nacimiento",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de nacimiento es obligatoria")],
        widget=DateInput()
    )
    
    telefono = StringField(
        "Telefono",
        validators=[DataRequired(message="El telefono es obligatorio"), Length(max=15)],
    )
    
    becado = BooleanField("Becado")
    
    observaciones = StringField("Observaciones")
    
    certificado_discapacidad = BooleanField("Certificado de discapacidad")
    
    diagnostico = SelectField(
        "Diagnostico", 
        choices=[(diag.name, diag.value) for diag in DiagnosticoEnum],
        validators=[DataRequired(message="El tipo de diagnostico es obligatorio")],
    )
    
    pension = SelectField(
        "Tipo pension",
        choices=[(pens.name, pens.value) for pens in PensionEnum],
        validators=[DataRequired(message="El tipo de pension es obligatorio")],
    )
    '''
    localidad_nacimiento = SelectField(
        "Localidad de Nacimiento", coerce=int, validators=[DataRequired()]
    )
    
    provincia_nacimiento = SelectField(
        "Provincia de Nacimiento", coerce=int, validators=[DataRequired()]
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
    
    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio"),
            Length(max=15),
            Regexp(r"^\d+$", message="El teléfono debe contener solo números"),
        ],
    )
    
    contacto_emergencia_nombre = StringField(
        "Nombre", validators=[DataRequired(), Length(max=100)]
    )
    contacto_emergencia_telefono = StringField(
        "Teléfono", validators=[DataRequired(), Length(max=15)]
    )
    
    becado = BooleanField("Becado")

####################### PORCENTAJE DE BECAS #################

    observaciones = StringField(
        "Observaciones",
        validators=[DataRequired(message="observaciones es obligatorio")],
    )

    certificado_discapacidad = BooleanField("Posee certificado de discapacidad?")
    
    #beneficiario_pension=BooleanField("beneficiario pension")


    profesionales = SelectField(
        "Profesionales",
        validators=[DataRequired(message="Los profesionales son obligatorios")],
    )
    
    tipo_discapacidad
    
    asignacion_familiar
    
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
    
    curatela
    
    observaciones
    
    nombre_institucion
    
    direccion_institucion
    
    telefono_institucion
    
    grado_institucion
    
    parentesco_familiar
    
    nombre_familiar
    
    apellido_familiar
    
    dni_familiar
    
    domicilio_calle_familiar
    
    domicilio_numero_familiar
    
    domicilio_piso_familiar
    
    domicilio_departamento_familiar
    
    domicilio_localidad_familiar
    
    domicilio_provincia_familiar
    
    telefono_familiar
    
    Email_familiar
    
    escolaridad_familiar #desplegable
    
    ocupacion_familiar
    
    trabajo_institucion
    
    condicion_institucion
    
    sede_institucion
    
    dia_institucion
    
    profesor_institucion
    
    conductor_caballo_institucion
    
    caballo_institucion
    
    auxiliar_institucion
'''
    
    submit = SubmitField("Guardar")