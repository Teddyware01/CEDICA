from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    DateTimeField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired,ValidationError, Email, Length, Optional, Regexp
from wtforms.widgets import DateInput
from .models import CondicionEnum, Empleado
from .extra_models import Localidad


class AddEmpleadoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=100),Regexp(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", message="El nombre solo puede contener letras y espacios")],
    )
    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(message="El apellido es obligatorio"),
            Length(max=100),
            Regexp(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", message="El apellido solo puede contener letras y espacios"),
        ],
    )
    dni = StringField(
        "DNI",
        validators=[
            DataRequired(message="El DNI es obligatorio"),
            Length(min=10, max=11),
            Regexp(r"^\d+$", message="El DNI debe contener solo números"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El Email es obligatorio"),
            Length(max=255),
            Email(message="Ingrese un correo electrónico válido"),
        ],
    )
    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio"),
            Length(min=10,max=15),
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
            Length(max=25),
        ],
    )
    nro_afiliado = StringField(
        "Número Afiliado",
        validators=[
            Length(max=25),
            DataRequired(message="El número de afiliado de obra social es obligatorio")
        ],
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
        "Nombre", validators=[DataRequired("Es necesario un nombre para el contacto de emergencia"), Length(max=100),Regexp(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", message="El nombre solo puede contener letras y espacios")]
    )
    contacto_emergencia_apellido = StringField(
        "Apellido", validators=[DataRequired("Es necesario un apellido para el contacto de emergencia"), Length(max=100),Regexp(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", message="El apellido solo puede contener letras y espacios")]
    )
    contacto_emergencia_telefono = StringField(
        "Teléfono", validators=[DataRequired("Es necesario un numero de teléfono para el contacto de emergencia"),Length(min=10,max=15), Regexp(r"^\d+$", message="El teléfono debe contener solo números"),]
    )

    submit = SubmitField("Guardar")

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj  # Guardar el objeto que se está editando
        

    # Validación personalizada, el nombre declarado sigue nomenclatura a respetar.
    def validate_domicilio_localidad(self, field_localidad):
        # Obtener la localidad seleccionada
        localidad_id = field_localidad.data
        provincia_id_seleccionada = self.domicilio_provincia.data

        # Consultar la localidad en la base de datos
        localidad = Localidad.query.get(localidad_id)
        if localidad.provincia_id != provincia_id_seleccionada:
            raise ValidationError("La localidad seleccionada no corresponde a la provincia elegida.")       
        print("ACA ESTAMOS")
    
    
    def validate_dni(self, dni):
        empleado = Empleado.query.filter_by(dni=dni.data).first()
        if empleado and (self.obj is None or empleado.id != self.obj.id):
            raise ValidationError("Este DNI ya está registrado.")

    def validate_email(self, email):
        empleado = Empleado.query.filter_by(email=email.data).first()
        if empleado and (self.obj is None or  empleado.id != self.obj.id):
            raise ValidationError("Este correo electrónico ya está registrado.")

    def validate_telefono(self, telefono):
        empleado = Empleado.query.filter_by(telefono=telefono.data).first()
        if empleado and (self.obj is None or empleado.id != self.obj.id):
            raise ValidationError("Este número de teléfono ya está registrado.")

    def validate_fecha_cese(self, field):
        if field.data and field.data <= self.fecha_inicio.data:
            raise ValidationError("La fecha de cese debe ser posterior a la fecha de inicio.")
