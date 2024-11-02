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
    FieldList, 
    FormField,
)
from src.core.equipo.extra_models import Localidad
from src.core.equipo.models import PuestoLaboral
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError, NumberRange
from wtforms.widgets import DateInput, ListWidget, CheckboxInput
from .models import PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum, DiasEnum, TrabajoEnum, SedeEnum, EscolaridadEnum
from src.core.ecuestre import list_ecuestre
from src.core.equipo import list_terapeutas_y_profesores, list_auxiliares_pista, list_conductores_caballos

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
    
    observaciones_becado = StringField(
        "Observaciones becado",
        validators=[Optional()]
    )
    
    certificado_discapacidad = BooleanField("Certificado de discapacidad")
    
    otro = StringField("Otro")
    
    diagnostico = SelectField(
        "Diagnostico", 
        choices=[(diag.name, diag.value) for diag in DiagnosticoEnum],
        validators=[Optional()],
    )
    
    beneficiario_pension = BooleanField("Es beneficiario de una pension?")
    
    pension = SelectField(
        "Tipo pension",
        choices=[(pens.name, pens.value) for pens in PensionEnum],
        validators=[DataRequired(message="El tipo de pension es obligatorio")],
    )
    
    discapacidades = SelectMultipleField(
        "Tipos de Discapacidad",
        choices=[],
        coerce=str,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
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
    domicilio_departamento = StringField("Departamento", validators=[Optional()])
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
        validators=[Optional()],
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
    
    estado_pago = BooleanField("Estado de Pago (Marcar si está al día)", default=True)
    
    curatela = BooleanField("Curatela", validators=[DataRequired("Indique si posee curatela")])
    
    observaciones_curatela = StringField("Observaciones curatela", validators=[Optional()])

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
    institucion_direccion_departamento = StringField("Departamento", validators=[Optional()])
    institucion_direccion_piso = IntegerField("Piso", validators=[Optional()])
    institucion_direccion_provincia = SelectField("Provincia", coerce=int, validators=[DataRequired()])
    institucion_direccion_localidad = SelectField("Localidad", coerce=int, validators=[DataRequired()])
    


    grado = IntegerField("Grado", validators=[DataRequired("Ingrese el grado / año actual")])
    
    observaciones_institucion = StringField("Observaciones institucion", validators=[Optional()])
    
    profesionales = StringField(
        "Profesionales",
        validators=[DataRequired(message="Los profesionales son obligatorios")],
    )

    # ---------- FAMILIARES ---------- 
    parentesco_familiar = StringField('Parentesco', validators=[Optional()])
    nombre_familiar = StringField("Nombre", validators=[Optional()])
    
    apellido_familiar = StringField("Apellido", validators=[Optional()])
    dni_familiar = StringField("DNI", validators=[Optional()])
    
    domicilio_familiar_calle = StringField("Calle", validators=[Optional()])
    domicilio_familiar_numero = IntegerField("Número", validators=[Optional()])
    domicilio_familiar_departamento = StringField("Departamento", validators=[Optional()])
    domicilio_familiar_piso = IntegerField("Piso", validators=[Optional()])  
    domicilio_familiar_provincia = SelectField("Provincia", coerce=int, validators=[Optional()])
    domicilio_familiar_localidad = SelectField("Localidad", coerce=int, validators=[Optional()])
    #direccion_familiar = StringField("Direccion", validators=[Optional()])
    celular_familiar = StringField("Celular", validators=[Optional()])
    email_familiar = StringField('Email', validators=[Optional()])
    nivel_escolaridad_familiar = SelectField(
        'Nivel de escolaridad', choices=[(esc.name, esc.value) for esc in EscolaridadEnum], 
        validators=[Optional()])        
    actividad_ocupacion_familiar = StringField('Actividad u ocupación', validators=[Optional()])
    
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
    
    dias = SelectMultipleField(
        "Dias", 
        coerce=str,
        choices=[],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
    )
    
    
    caballo = SelectField(
        "Caballo",
        choices=[],
        validators=[DataRequired(message="El caballo es obligatorio")],
    )

    profesor_o_terapeuta = SelectField(
        "Profesor o terapeuta",
        choices=[],
        validators=[Optional()],
    )
    
    conductor_caballo = SelectField(
        "Conductor de caballo",
        choices=[],
        validators=[Optional()],
    )
    auxiliar_pista = SelectField(
        "Auxiliar de pista",
        choices=[],
        validators=[Optional()],
    )
            
    submit = SubmitField("Guardar")