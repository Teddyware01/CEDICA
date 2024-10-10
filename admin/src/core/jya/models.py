'''
from src.core.database import db
from datetime import datetime
#from src.core.equipo.extra_models import Domicilio, ContactoEmergencia, Localidad, Provincia
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY
'''
'''
class TipoDiscapacidadEnum(Enum):
    mental="Mental"
    motora="Motora"
    sensorial="Sensorial"
    visceral="Visceral"
    
    
class DiasEnum(Enum):
    lunes="Lunes"
    martes="Martes"
    miercoles="Miércoles"
    jueves="Jueves"
    viernes="Viernes"
    sabado="Sábado"
    domingo="Domingo"
    
    
class DiagnosticoEnum(Enum):
    ecne='ECNE'
    lesion_postraumatica='Lesión postraumática'
    mielomeningocele='Mielomeningocele'
    escoliosis_multiple='Escoliosis múltiple'
    escoliosis_leve='Escoliosis Leve'
    secuelas_ACV='Secuelas de ACV'
    discapacidad_intelectual='Discapacidad Intelectual'
    trastorno_espectro_autista='Trastorno del Espectro Autista'
    trastorno_aprendizaje='Trastorno del Aprendizaje'
    trastorno_deficit_Atencion='Trastorno por Déficit de Atención/Hiperactividad'
    trastorno_comunicacion='Trastorno de la Comunicación'
    trastorno_ansiedad='Trastorno de Ansiedad'
    sindrome_down='Síndrome de Down'
    retraso_madurativo='Retraso Madurativo'
    psicosis='Psicosis'
    trastorno_conducta='Trastorno de Conducta'
    trastornos_animo_afectivos='Trastornos del ánimo y afectivos'
    trastorno_alimentario='Trastorno Alimentario'
    otro='Otro'
    
    
class AsignacionEnum(Enum):
    por_hijo='Asignación Universal por hijo'
    por_discapacidad='Asignación Universal por hijo con Discapacidad'
    escolar='Asignación por ayuda escolar anual'
        

class PensionEnum(Enum):
    provincial='Provincial'
    nacional='Nacional'


class SituacionPrevisional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obra_social = db.Column(db.String(100), nullable=False)
    numero_afiliado = db.Column(db.String(50), nullable=True)
    tiene_curatela = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.String(255), nullable=True)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'))
    jinete = db.relationship('Jinete', back_populates='situacion_previsional')


class Familiar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(10), nullable=False, unique=True)
    domicilio = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    relacion = db.Column(db.String(50), nullable=False)
    nivel_escolaridad = db.Column(db.String(100), nullable=True)
    actividad_ocupacion = db.Column(db.String(100), nullable=True)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'))
    jinete = db.relationship('Jinete', back_populates='familiares')
    
    
class TrabajoInstitucional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'))
    jinete = db.relationship('Jinete', back_populates='jinete')
    
class TrabajoInstitucional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    jinete_id = db.Column(db.Integer, db.ForeignKey('jinete.id'))  # Agrega la clave foránea a Jinete
    jinete = db.relationship('Jinete', back_populates='trabajos_institucionales')  # Actualiza el back_populates
'''    
'''  
class Jinete(db.Model):
    __tablename__ = 'jinete'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(10), nullable=False, unique=True)
    #edad = db.Column(db.Integer, nullable=False)
    #fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    #lugar_nacimiento = db.Column(db.localidad, db.provincia, nullable=False)
    #domicilio_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=False)
    #domicilio = db.relationship("Domicilio", back_populates="jinete")
    #telefono = db.Column(db.String(15), nullable=False)
    #contacto_emergencia_id = db.Column(db.Integer, db.ForeignKey("contacto_emergencia.id"), nullable=False)
    #contacto_emergencia = db.relationship("ContactoEmergencia")
    #becado = db.Column(db.Boolean)
    #observaciones = db.Column(db.String(255), nullable=True)
    #certificado_discapacidad = db.Column(db.Boolean)
    #diagnostico = db.Column(db.Enum(DiagnosticoEnum))
    #otro_diagnostico = db.Column(db.String(100), nullable=True)
    #tipo_discapacidad = db.Column(db.Enum(TipoDiscapacidadEnum), nullable=True)
    #asignacion_familiar = db.Column(db.Boolean)
    #tipo_asignacion = db.Column(db.Enum(AsignacionEnum), nullable=True)
    #beneficiario_pension = db.Column(db.Boolean)
    #tipo_pension = db.Column(db.Enum(PensionEnum), nullable=True)
    #situacion_previsional = db.relationship('SituacionPrevisional', back_populates='jinete', uselist=False)
    #trabajos_institucionales = db.relationship('TrabajoInstitucional', back_populates='jinete')
    #institucion_escolar_id = db.Column(db.Integer, db.ForeignKey('institucion_escolar.id'))
    #institucion_escolar = db.relationship('InstitucionEscolar')
    #profesionales = db.Column(db.String(255), nullable=False)
    #familiares = db.relationship('Familiar', back_populates='jinete')
    
    def __repr__(self):
        return f"<Jinete #{self.id}. Apellido y Nombre = {self.apellido}, {self.nombre}. DNI = {self.dni}>"
'''
from src.core.database import db
from datetime import datetime
from enum import Enum


class PensionEnum(Enum):
    provincial='Provincial'
    nacional='Nacional'
    
    
class Jinete(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(10), nullable=False, unique=True)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    '''
    becado = db.Column(db.Boolean)
    observaciones = db.Column(db.String(255), nullable=True)
    certificado_discapacidad = db.Column(db.Boolean)
    beneficiario_pension = db.Column(db.Boolean)
    tipo_pension = db.Column(db.Enum(PensionEnum), nullable=True)
    profesionales = db.Column(db.String(255), nullable=False)
    '''
    def __repr__(self):
        return f"<User #{self.id} nombre = {self.nombre}>"
    
