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
from src.core.equipo.extra_models import Localidad
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError, NumberRange
from wtforms.widgets import DateInput
from .models import PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum, DiasEnum, TrabajoEnum, SedeEnum

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
    
    edad = IntegerField(
        "Edad",
        validators=[
            DataRequired(message="La edad es obligatoria"),
            NumberRange(min=0, max=120, message="La edad debe estar entre 0 y 120 años"),
        ],
    )
        
    fecha_nacimiento = DateTimeField(
        "Fecha de Nacimiento",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de nacimiento es obligatoria")],
        widget=DateInput()
    )

    
    becado = BooleanField("Becado")
    
    observaciones_becado = StringField("Observaciones becado")
    
    certificado_discapacidad = BooleanField("Certificado de discapacidad")
    
    otro = StringField("Otro")
    
    diagnostico = SelectField(
        "Diagnostico", 
        choices=[(diag.name, diag.value) for diag in DiagnosticoEnum],
        validators=[DataRequired(message="El tipo de diagnostico es obligatorio")],
    )
    
    beneficiario_pension = BooleanField("Es beneficiario de una pension?")
    
    pension = SelectField(
        "Tipo pension",
        choices=[(pens.name, pens.value) for pens in PensionEnum],
        validators=[DataRequired(message="El tipo de pension es obligatorio")],
    )
    
    tipos_discapacidad = SelectMultipleField(
        "Tipo de Discapacidad",
        choices=[(disc.name, disc.value) for disc in TiposDiscapacidadEnum],
        coerce=str,
        validators=[DataRequired(message="Seleccionar al menos un tipo de discapacidad es obligatorio")],
    )
    # LUGAR NACIMIENTO
    provincia_nacimiento = SelectField(
        "Provincia de Nacimiento", coerce=int, validators=[DataRequired()]
    )
    
    localidad_nacimiento = SelectField(
        "Localidad de Nacimiento", coerce=int, validators=[DataRequired()]
    )

    # domicilio actual
    domicilio_calle = StringField("Calle", validators=[DataRequired("Ingrese calle del domicilio")])
    domicilio_numero = IntegerField("Número", validators=[DataRequired("Ingrese número del domicilio")])
    domicilio_departamento = IntegerField("Departamento", validators=[Optional()])
    domicilio_piso = IntegerField("Piso", validators=[Optional()])
    domicilio_provincia = SelectField(
        "Provincia", coerce=int, validators=[DataRequired()]
    )
    domicilio_localidad = SelectField(
        "Localidad", coerce=int, validators=[DataRequired()]
    )
    
    telefono = StringField(
        "Teléfono",
        validators=[DataRequired(message="El teléfono es obligatorio"), Length(max=15),
            Regexp(r"^\d+$", message="El telefono debe contener solo números")]
    )
    
    #Contacto emergencia
    contacto_emergencia_nombre = StringField(
        "Nombre", validators=[DataRequired(), Length(max=100)]
    )
    contacto_emergencia_apellido = StringField(
        "Apellido", validators=[DataRequired(), Length(max=100)]
    )
    contacto_emergencia_telefono = StringField(
        "Teléfono", 
        validators=[DataRequired(message="El teléfono es obligatorio"), Length(max=15)],
    )
    
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

    obra_social = StringField(
        "Obra Social",
        validators=[
            DataRequired(message="El nombre de obra social es obligatorio"),
            Length(max=25),
        ],
    )
    nro_afiliado = StringField(
        "Número Afiliado",
        validators=[DataRequired(message="El número de afiliado de obra social es obligatorio")
        ],
    )
    
    ##agrego aca
    estado_pago = BooleanField("Estado de Pago (Marcar si está al día)", default=True)
    ##agrego aca

    curatela = BooleanField("Curatela", validators=[DataRequired("Indique si posee curatela")])
    
    observaciones_curatela = StringField("Observaciones curatela")
    
    nombre_institucion = StringField(
        "Nombre institucion",
        validators=[DataRequired(message="El número de afiliado de obra social es obligatorio")],
    )
    
    telefono_institucion = StringField(
        "Teléfono institucion", 
        validators=[DataRequired(message="El teléfono es obligatorio"), Length(max=15)],
    )
    # direccion de la institucion
    
    # domicilio actual
    institucion_direccion_calle = StringField("Calle", validators=[DataRequired("Ingrese calle del domicilio")])
    institucion_direccion_numero = IntegerField("Número", validators=[DataRequired("Ingrese número del domicilio")])
    institucion_direccion_departamento = IntegerField("Departamento", validators=[Optional()])
    institucion_direccion_piso = IntegerField("Piso", validators=[Optional()])
    institucion_direccion_provincia = SelectField("Provincia", coerce=int, validators=[DataRequired()])
    institucion_direccion_localidad = SelectField("Localidad", coerce=int, validators=[DataRequired()])
    


    grado = IntegerField("Grado", validators=[DataRequired("Ingrese el grado / año actual")])
    
    observaciones_institucion = StringField("Observaciones institucion")
    
    profesionales = StringField(
        "Profesionales",
        validators=[DataRequired(message="Los profesionales son obligatorios")],
    )
    
    trabajo_institucional = SelectField(
        "Trabajo institucional",
        choices=[(trab.name, trab.value) for trab in TrabajoEnum],
        validators=[DataRequired(message="Los profesionales son obligatorios")],
    )
    
    condicion=BooleanField("Condicion")

    sede=SelectField("Sede",
        choices=[(sede.name, sede.value) for sede in SedeEnum],
        validators=[DataRequired(message="La sede es obligatoria")],
    )
    
    dia = SelectMultipleField(
        "DIA",
        choices=[(dia.name, dia.value) for dia in DiasEnum],
        validators=[DataRequired(message="Seleccionar al menos un dia")],
    )
    
    
    submit = SubmitField("Guardar")
    
'''
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
        
    profesor_institucion
    
    conductor_caballo_institucion
    
    caballo_institucion
    
    auxiliar_institucion
'''