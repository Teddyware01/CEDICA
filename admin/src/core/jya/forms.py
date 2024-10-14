from flask_wtf import FlaskForm
from wtforms import (
    SelectMultipleField,
    StringField,
    IntegerField,
    SelectField,
    DateTimeField,
    BooleanField,
    SubmitField,
    widgets,
)
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError
from wtforms.widgets import DateInput
from .models import PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum
from src.core.equipo.extra_models import Localidad

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
    
    otro = StringField("Otro")
    
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
    
    tipos_discapacidad = SelectMultipleField(
        "Tipo de Discapacidad",
        choices=[(disc.name, disc.value) for disc in TiposDiscapacidadEnum],
        validators=[DataRequired(message="Seleccionar al menos un tipo de discapacidad es obligatorio")],
    )
    
    localidad_nacimiento = SelectField(
        "Localidad de Nacimiento", coerce=int, validators=[DataRequired()]
    )
    
    provincia_nacimiento = SelectField(
        "Provincia de Nacimiento", coerce=int, validators=[DataRequired()]
    )
    
    domicilio_calle = StringField("Calle", validators=[DataRequired("Ingrese calle del domicilio")])
    domicilio_numero = IntegerField("Número", validators=[DataRequired("Ingrese número del domicilio")])
    domicilio_departamento = IntegerField("Departamento", validators=[Optional()])
    domicilio_piso = IntegerField("Piso", validators=[Optional()])
    domicilio_provincia = SelectField(
        "Provincia", coerce=int, validators=[DataRequired("Selecione una provincia")]
    )
    domicilio_localidad = SelectField(
        "Localidad", coerce=int, validators=[DataRequired("Selecione una localidad.")]
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

    # Validación personalizada, el nombre declarado sigue nomenclatura a respetar.
    def validate_domicilio_localidad(self, field_localidad):
        # Obtener la localidad seleccionada
        localidad_id = field_localidad.data
        provincia_id_seleccionada = self.domicilio_provincia.data

        # Consultar la localidad en la base de datos
        localidad = Localidad.query.get(localidad_id)
        if localidad.provincia_id != provincia_id_seleccionada:
            raise ValidationError("La localidad seleccionada no corresponde a la provincia elegida.")
        
    asignacion_familiar = BooleanField("Asignacion familiar")
        
    tipo_asignacion = SelectField(
        "Asignacion familiar", 
        choices=[(asig.name, asig.value) for asig in AsignacionEnum],
        validators=[DataRequired(message="El tipo de asignacion es obligatorio")],
    )

####################### PORCENTAJE DE BECAS #################
'''
    profesionales = SelectField(
        "Profesionales",
        validators=[DataRequired(message="Los profesionales son obligatorios")],
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