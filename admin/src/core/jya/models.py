from src.core.database import db
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY

class PensionEnum(Enum):
    provincial="Provincial"
    nacional="Nacional"

class DiasEnum(Enum):
    lunes="Lunes"
    martes="Martes"
    miercoles="Miércoles"
    jueves="Jueves"
    viernes="Viernes"
    sabado="Sábado"
    domingo="Domingo"


class Dias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dias = db.Column(db.Enum(DiasEnum), nullable=True)
    #dias = db.Column(db.String(50))
    jinetes = db.relationship('Jinete', secondary='jinete_dias', back_populates='dias')

jinete_dias = db.Table('jinete_dias',
    db.Column('jinete_id', db.Integer, db.ForeignKey('jinete.id'), primary_key=True),
    db.Column('dias_id', db.Integer, db.ForeignKey('dias.id'), primary_key=True)
)

class AsignacionEnum(Enum):
    por_hijo='Asignación Universal por hijo'
    por_discapacidad='Asignación Universal por hijo con Discapacidad'
    escolar='Asignación por ayuda escolar anual'
    
class DiagnosticoEnum(Enum):
    ecne="ECNE"
    lesion_postraumatica="Lesión postraumática"
    mielomeningocele="Mielomeningocele"
    escoliosis_multiple="Escoliosis múltiple"
    escoliosis_leve="Escoliosis Leve"
    secuelas_ACV="Secuelas de ACV"
    discapacidad_intelectual="Discapacidad Intelectual"
    trastorno_espectro_autista="Trastorno del Espectro Autista"
    trastorno_aprendizaje="Trastorno del Aprendizaje"
    trastorno_deficit_Atencion="Trastorno por Déficit de Atención/Hiperactividad"
    trastorno_comunicacion="Trastorno de la Comunicación"
    trastorno_ansiedad="Trastorno de Ansiedad"
    sindrome_down="Síndrome de Down"
    retraso_madurativo="Retraso Madurativo"
    psicosis="Psicosis"
    trastorno_conducta="Trastorno de Conducta"
    trastornos_animo_afectivos="Trastornos del ánimo y afectivos"
    trastorno_alimentario="Trastorno Alimentario"
    otro="Otro"

class TiposDiscapacidadEnum(Enum):
    mental="Mental"
    motora="Motora"
    sensorial="Sensorial"
    visceral="Visceral"

class TipoDiscapacidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipos_discapacidad = db.Column(db.Enum(TiposDiscapacidadEnum), nullable=True)
    jinetes = db.relationship('Jinete', secondary='jinete_discapacidad', back_populates='discapacidades')


jinete_discapacidad = db.Table('jinete_discapacidad',
    db.Column('jinete_id', db.Integer, db.ForeignKey('jinete.id'), primary_key=True),
    db.Column('discapacidad_id', db.Integer, db.ForeignKey('tipo_discapacidad.id'), primary_key=True)
)

class EscolaridadEnum(Enum):
    primario="Primario"
    secundario="Secundario"
    terciario="Terciario"
    universitario="Universitario"
    
class TrabajoEnum(Enum):
    hipoterapia="Hipoterapia"
    monta_terapeutica="Monta Terapéutica"
    deporte="Deporte"
    ecuestre_adaptado="Ecuestre Adaptado"
    actividades_recreativas="Actividades Recreativas"
    equitacion="Equitación"
    
class SedeEnum(Enum):
    casj="CASJ"
    hlp="HLP"
    otro="OTRO"

    
class Familiar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'), nullable=False)
    jinetes = db.relationship('Jinete', secondary='jinete_familiar', back_populates='familiares')
    parentesco_familiar = db.Column(db.String(255), nullable=True)
    nombre_familiar = db.Column(db.String(255), nullable=True)
    apellido_familiar = db.Column(db.String(255), nullable=True)
    dni_familiar = db.Column(db.String(10), nullable=True, unique=True)
        
    domicilio_familiar_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=True)
    domicilio_familiar = db.relationship("Domicilio", back_populates="familiares")
    #localidad_familiar_id = db.Column(db.Integer, db.ForeignKey("localidad.id"), nullable=True)
    #localidad_familiar = db.relationship("Localidad", back_populates="familiares")  
    #provincia_familiar_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), nullable=True)
    #provincia_familiar = db.relationship("Provincia", back_populates="familiares")  
    celular_familiar = db.Column(db.String(15), nullable=True)
    email_familiar = db.Column(db.String(255), nullable=True)
    nivel_escolaridad_familiar = db.Column(db.Enum(EscolaridadEnum), nullable=True)
    actividad_ocupacion_familiar = db.Column(db.String(255), nullable=True)

jinete_familiar = db.Table('jinete_familiar',
    db.Column('jinete_id', db.Integer, db.ForeignKey('jinete.id'), primary_key=True),
    db.Column('familiar_id', db.Integer, db.ForeignKey('familiar.id'), primary_key=True)
)

class TipoDocumentoEnum(Enum):
    entrevista="Entrevista"
    evaluacion="Evaluación"
    planificaciones="Planificaciones"
    evolucion="Evolución"
    cronicas="Crónicas"
    documental="Documental"
    
class JineteDocumento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_documento = db.Column(db.String(100), nullable=True) #el que usa minio
    nombre_archivo = db.Column(db.String(255), nullable=False) #escrito a mano("nombre_asignado")
    fecha_subida_documento = db.Column(db.DateTime, default=datetime.now)
    tipo_documento = db.Column(db.Enum(TipoDocumentoEnum), nullable=True)
    
    is_enlace =  db.Column(db.Boolean, default=False, nullable=False)
    url_enlace = db.Column(db.String(255), nullable=True)

    jinete_id = db.Column(db.Integer, db.ForeignKey("jinete.id"), nullable=False)
    jinete = db.relationship("Jinete", back_populates="documentos")
    
    
class Jinete(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(10), nullable=False, unique=True)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    #nacimiento_id = db.Column(db.Integer, db.ForeignKey("nacimiento.id"), nullable=False)
    #nacimiento = db.relationship("Nacimiento", back_populates="jinetes")
    esta_borrado = db.Column(db.Boolean, default=False)
    
    provincia_nacimiento_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), nullable=False)
    provincia_nacimiento = db.relationship("Provincia", back_populates="jinetes")
    localidad_nacimiento_id = db.Column(db.Integer, db.ForeignKey("localidad.id"), nullable=False)
    localidad_nacimiento = db.relationship("Localidad", back_populates="jinetes")
    domicilio_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=False)
    domicilio = db.relationship("Domicilio", foreign_keys=[domicilio_id], back_populates="jinetes")
    telefono = db.Column(db.String(15), nullable=False)
    contacto_emergencia_id = db.Column(db.Integer, db.ForeignKey("contacto_emergencia.id"), nullable=False)
    contacto_emergencia = db.relationship("ContactoEmergencia", back_populates="jinete")
    becado = db.Column(db.Boolean, default=False)
    observaciones_becado = db.Column(db.String(255), nullable=True)
    certificado_discapacidad = db.Column(db.Boolean, default=False)
    diagnostico = db.Column(db.Enum(DiagnosticoEnum), nullable=True)
    otro = db.Column(db.String(100), nullable=True)
    beneficiario_pension = db.Column(db.Boolean, default=False)
    pension = db.Column(db.Enum(PensionEnum), nullable=True)
    #tipos_discapacidad =  db.Column(ARRAY(db.Enum(TiposDiscapacidadEnum)), nullable=True)
    discapacidades = db.relationship('TipoDiscapacidad', secondary='jinete_discapacidad', back_populates='jinetes')
    asignacion_familiar = db.Column(db.Boolean, default=False)
    tipo_asignacion = db.Column(db.Enum(AsignacionEnum), nullable=True)
    obra_social = db.Column(db.String(25), nullable=False, unique=False)
    nro_afiliado = db.Column(db.String(25), nullable=False, unique=False)
    curatela = db.Column(db.Boolean, default=False)
    observaciones_curatela = db.Column(db.String(255), nullable=True)
    nombre_institucion = db.Column(db.String(50), nullable=True) 
    direccion_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"))
    direccion = db.relationship("Domicilio", foreign_keys=[direccion_id], backref="direccion_jinetes")
    telefono_institucion = db.Column(db.String(15), nullable=False)
    grado = db.Column(db.Integer, nullable=False)
    observaciones_institucion = db.Column(db.String(255), nullable=True)
    profesionales = db.Column(db.String(255), nullable=True)
    estado_pago = db.Column(db.Boolean, default=True)
    trabajo_institucional=db.Column(db.Enum(TrabajoEnum), nullable=False)
    condicion=db.Column(db.Boolean, default=False) # true regular, false de baja
    sede=db.Column(db.Enum(SedeEnum), nullable=False)
    dias = db.relationship('Dias', secondary=jinete_dias, back_populates='jinetes')
    familiares = db.relationship('Familiar', secondary='jinete_familiar', back_populates='jinetes')
    documentos = db.relationship("JineteDocumento", back_populates="jinete", cascade="all, delete-orphan")

    # Relaciones con tres empleados diferentes:
    #ids:
    profesor_o_terapeuta_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    conductor_caballo_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    caballo_id = db.Column(db.Integer, db.ForeignKey('ecuestre.id'), nullable=True)

    # Definir las relaciones
    profesor_o_terapeuta = db.relationship('Empleado', foreign_keys=[profesor_o_terapeuta_id], backref='profesor_o_terapeuta_jinetes')
    conductor_caballo = db.relationship('Empleado', foreign_keys=[conductor_caballo_id], backref='conductor_caballo_jinetes')
    auxiliar_pista = db.relationship('Empleado', foreign_keys=[auxiliar_pista_id], backref='auxiliar_pista_jinetes')
    caballo = db.relationship('Ecuestre', foreign_keys=[caballo_id], backref='caballo_jinetes')


    #ids
    def __repr__(self):
        return f"<User #{self.id} nombre = {self.nombre}>"
