from flask import render_template, request, redirect, flash, url_for, current_app
from os import fstat
from flask import Blueprint
from src.core import auth
from src.core import jya
from src.core.database import db
from src.core.jya.forms import AddJineteForm
from src.core.jya.models import Jinete, PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum, DiasEnum
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
import src.web.controllers.jya
from src.core.jya.legajo import list_documentos

bp = Blueprint("jya", __name__, url_prefix="/jinetes")


@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 3  
    jinetes = jya.list_jinetes(sort_by=sort_by, search=search).paginate(page=page, per_page=per_page)

    return render_template("jya/listado_jya.html", jinetes=jinetes)

@bp.get("/agregar_jinete")
def add_jinete_form():
    form = AddJineteForm()
    form.pension.choices = [(p.name, p.value) for p in PensionEnum]
    form.diagnostico.choices = [(d.name, d.value) for d in DiagnosticoEnum]
    form.tipos_discapacidad.choices = [(disc.name, disc.value) for disc in TiposDiscapacidadEnum]
    form.domicilio_provincia.choices = [
        (p.id, p.nombre) for p in jya.list_provincias()
    ]
    form.domicilio_localidad.choices = [
        (p.id, p.nombre) for p in jya.list_localidades()
    ]
    form.tipo_asignacion.choices = [(asig.name, asig.value) for asig in AsignacionEnum]
    
    form.dia.choices = [(dia.name, dia.value) for dia in DiasEnum]

    return render_template("jya/agregar_jya.html", form=form)


@bp.post("/agregar_jinete")
def add_jinete():
    form = AddJineteForm(request.form)
    cargar_choices_form(form)
    localidad = jya.get_localidad_by_id(form.domicilio_localidad.data)
    provincia = jya.get_provincia_by_id(form.domicilio_provincia.data)
    nuevo_domicilio = jya.add_domiclio(
        calle=form.domicilio_calle.data,
        numero=form.domicilio_numero.data,
        departamento=form.domicilio_departamento.data,
        piso=form.domicilio_piso.data,
        localidad=localidad,
        provincia=provincia,
    )
    
    nuevo_contacto_emergencia = jya.add_contacto_emergencia(
        nombre=form.contacto_emergencia_nombre.data,
        apellido=form.contacto_emergencia_apellido.data,
        telefono=form.contacto_emergencia_telefono.data,
    )

    jya.create_jinete(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
        edad=request.form["edad"],
        fecha_nacimiento=request.form["fecha_nacimiento"],
        domicilio=nuevo_domicilio,
        telefono=request.form["telefono"],
        contacto_emergencia_id=nuevo_contacto_emergencia.id,
        becado=form.becado.data,
        observaciones=form.observaciones.data,
        certificado_discapacidad=form.certificado_discapacidad.data,
        #beneficiario_pension=form.beneficiario_pension.data,
        pension=form.pension.data,
        diagnostico=form.diagnostico.data,
        otro=form.otro.data,
        tipos_discapacidad = [TiposDiscapacidadEnum[tipos_discapacidad] for tipos_discapacidad in form.tipos_discapacidad.data],
        asignacion_familiar=form.asignacion.data,
        tipo_asignacion=[AsignacionEnum[tipo_asignacion] for tipo_asignacion in form.tipo_asignacion.data],
        obra_social=form.obra_social.data,
        nro_afiliado=form.nro_afiliado.data,
        curatela=form.curatela.data,
        observaciones_institucion=form.observaciones_institucion.data,
        profesionales=form.profesionales.data,
        
        dia = [DiasEnum[dia] for dia in form.dia.data],
        
    )
    
    flash("Jinete registrado exitosamente", "success")
    return redirect(url_for("jya.listar_jinetes"))

@bp.get("/ver_jinete<int:jinete_id>")
def view_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    documentos = list_documentos()
    tipos_discapacidad_nombres = [tipo.name for tipo in jinete.tipos_discapacidad] if jinete.tipos_discapacidad else []
    dias_nombres = [dia.name for dia in jinete.dia] if jinete.dia else []
    return render_template("jya/ver_jya.html", jinete=jinete, tipos_discapacidad=tipos_discapacidad_nombres, dia=dias_nombres, documentos=documentos)

'''@bp.get("/editar_jinete<int:jinete_id>")
def edit_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    cargar_choices_form(form)
    # Asignar los valores del domicilio
    form.domicilio_calle.data = jinete.domicilio.calle
    form.domicilio_numero.data = jinete.domicilio.numero
    form.domicilio_piso.data = jinete.domicilio.piso
    form.domicilio_departamento.data = jinete.domicilio.departamento
    form.domicilio_localidad.data = jinete.domicilio.localidad
    form.domicilio_provincia.data = jinete.domicilio.provincia

    # Asignar los valores del contacto de emergencia
    form.contacto_emergencia_nombre.data = jinete.contacto_emergencia.nombre
    form.contacto_emergencia_apellido.data = jinete.contacto_emergencia.apellido
    form.contacto_emergencia_telefono.data = jinete.contacto_emergencia.telefono
    
    return render_template("jya/editar_jya.html", jinete=jinete, form=form)

@bp.post("/editar_jinete<int:jinete_id>")
def editar_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    jya.edit_jinete(
        jinete_id,
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
        telefono=request.form["telefono"],
        fecha_nacimiento=request.form["fecha_nacimiento"],
        domicilio_provincia = request.form["domicilio_provincia"],
        domicilio_localidad = request.form["domicilio_localidad"],
    )
    
    flash("Jinete actualizado exitosamente", "success")
    return redirect(url_for("jya.listar_jinetes"))'''
    
@bp.get("/editar_jinete<int:jinete_id>")
def edit_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    cargar_choices_form(form)
    # Asignar los valores del domicilio
    form.domicilio_calle.data = jinete.domicilio.calle
    form.domicilio_numero.data = jinete.domicilio.numero
    form.domicilio_piso.data = jinete.domicilio.piso
    form.domicilio_departamento.data = jinete.domicilio.departamento
    form.domicilio_localidad.data = jinete.domicilio.localidad
    form.domicilio_provincia.data = jinete.domicilio.provincia

    # Asignar los valores del contacto de emergencia
    form.contacto_emergencia_nombre.data = jinete.contacto_emergencia.nombre
    form.contacto_emergencia_apellido.data = jinete.contacto_emergencia.apellido
    form.contacto_emergencia_telefono.data = jinete.contacto_emergencia.telefono
    
    return render_template("jya/editar_jya.html", jinete=jinete, form=form)

'''@bp.post("/editar_jinete<int:jinete_id>")
def editar_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(request.form, obj=jinete)
    cargar_choices_form(form, jinete=jinete)  # Asegurarse de recargar las opciones para validación

    form.populate_obj(jinete)  # Asignar todos los campos del formulario al modelo

    # Manejar manualmente los campos relacionales si necesario, ejemplo:
    # jinete.domicilio.localidad_id = form.domicilio_localidad.data
    # jinete.domicilio.provincia_id = form.domicilio_provincia.data
    # No olvides manejar otras relaciones si están presentes...

    db.session.commit()  # Guardar los cambios en la base de datos
    flash("Jinete actualizado exitosamente", "success")
    return redirect(url_for("jya.ver_jinete", jinete_id=jinete.id))'''


@bp.post("/editar_jinete<int:jinete_id>")
def editar_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    cargar_choices_form(form, jinete=jinete)
    #form.populate_obj(jinete)
    jya.edit_jinete(
        jinete_id,
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
        edad=request.form["edad"],
        fecha_nacimiento=request.form["fecha_nacimiento"],
        #localidad_nacimiento
        #provincia_nacimiento
        telefono=request.form["telefono"],
        domicilio_provincia = request.form["domicilio_provincia"],
        domicilio_localidad = request.form["domicilio_localidad"],
        
        

    )
    
    flash("Jinete actualizado exitosamente", "success")
    return redirect(url_for("jya.listar_jinetes"))

@bp.get("/eliminar_jinete<int:jinete_id>")
def delete_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/eliminar_jya.html", jinete=jinete)


@bp.post("/eliminar_jinete<int:jinete_id>")
def delete_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    jya.delete_jinete(jinete_id)
    
    return redirect(url_for("jya.listar_jinetes"))


@bp.get("/<int:jinete_id>/edit")
def edit(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    
    return render_template("jya/edit.html", jinete=jinete)

@bp.post("/<int:jinete_id>/update")
def update(jinete_id):
    params = request.form.copy()
    
    if "avatar" in request.files:
        file = request.files["avatar"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        #ulid = u.new()
        
        client.put_object(
            "grupo15", file.filename, file, size, content_type=file.content_type
        )           #f"avatars/{ulid}-{file.filename}",
        params["avatar"] = file.filename #Hacer funcion para que genere nombres unicos para el archivo y guardarlo en el usuario. Libreria ULID
                                
    jya.update_jinete(jinete_id, **params)
    flash("Usuario modificado correctamente", "success")
    
    return redirect(url_for("jya.listar_jinetes"))

def cargar_choices_form(form, jya=None):
    # Cargar las opciones para los campos de selección
    form.pension.choices = [(p.name, p.value) for p in PensionEnum]
    form.diagnostico.choices = [(d.name, d.value) for d in DiagnosticoEnum]
    form.tipos_discapacidad.choices = [(disc.name, disc.value) for disc in TiposDiscapacidadEnum]
    form.tipo_asignacion.choices = [(asig.name, asig.value) for asig in AsignacionEnum]
    #form.domicilio_provincia.choices = [(p.id, p.nombre) for p in jya.list_provincias()]
    #form.domicilio_localidad.choices = [(l.id, l.nombre) for l in jya.list_localidades()]
    
    
'''provincia_nacimiento = db.relationship("Provincia", back_populates="jinetes")
domicilio_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"), nullable=False)
domicilio = db.relationship("Domicilio", foreign_keys=[domicilio_id], back_populates="jinetes")
fecha_nacimiento = db.Column(db.DateTime, nullable=False)
telefono = db.Column(db.String(15), nullable=False)
avatar = db.Column(db.String(255), nullable=True)
contacto_emergencia_id = db.Column(db.Integer, db.ForeignKey("contacto_emergencia.id"), nullable=False)
contacto_emergencia = db.relationship("ContactoEmergencia", back_populates="jinete")
becado = db.Column(db.Boolean, default=False)
observaciones_becado = db.Column(db.String(255), nullable=True)
certificado_discapacidad = db.Column(db.Boolean, nullable=True)
diagnostico = db.Column(db.Enum(DiagnosticoEnum), nullable=True)
otro = db.Column(db.String(100), nullable=True)
beneficiario_pension = db.Column(db.Boolean)
pension = db.Column(db.Enum(PensionEnum), nullable=False)
tipos_discapacidad =  db.Column(ARRAY(db.Enum(TiposDiscapacidadEnum)), nullable=True)
asignacion_familiar = db.Column(db.Boolean, nullable=True)
tipo_asignacion = db.Column(db.Enum(AsignacionEnum), nullable=True)
obra_social = db.Column(db.String(25), nullable=False, unique=False)
nro_afiliado = db.Column(db.String(25), nullable=False, unique=False)
curatela = db.Column(db.Boolean, nullable=False)
observaciones_curatela = db.Column(db.String(255), nullable=True)
nombre_institucion = db.Column(db.String(50), nullable=False)
direccion_id = db.Column(db.Integer, db.ForeignKey("domicilio.id"))
direccion = db.relationship("Domicilio", foreign_keys=[direccion_id], backref="direccion_jinetes")
telefono_institucion = db.Column(db.String(15), nullable=False)
grado = db.Column(db.Integer, nullable=False)
observaciones_institucion = db.Column(db.String(255), nullable=True)
profesionales = db.Column(db.String(255), nullable=True)'''