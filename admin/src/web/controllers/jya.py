from flask import abort, render_template, request, redirect, flash, url_for, current_app
from os import fstat
from flask import Blueprint
from src.web.handlers.auth import login_required, check
from src.core import auth
from src.core import jya
from src.core import equipo
from src.core.database import db
from src.core.jya.forms import AddJineteForm
from src.core.jya.models import Jinete, PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum, Dias, DiasEnum, Familiar, JineteDocumento, TipoDiscapacidad, EscolaridadEnum
from src.core.equipo import list_terapeutas_y_profesores, list_auxiliares_pista, list_conductores_caballos
from src.core.ecuestre import list_ecuestre

from datetime import timedelta

bp = Blueprint("jya", __name__, url_prefix="/jinetes")


@bp.get("/")
@login_required
@check("jya_index")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    nombre = request.args.get("nombre", '')
    apellido = request.args.get("apellido", '')
    dni = request.args.get("dni", '')
    profesionales = request.args.get("profesionales", '')
    page = request.args.get('page', 1, type=int)
    jinetes = jya.list_jinetes(
        sort_by=sort_by,
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        profesionales=profesionales,
        page=page
    )
    return render_template("jya/listado_jya.html", jinetes=jinetes)



@bp.get("/agregar_jinete")
@login_required
@check("jya_create")
def add_jinete_form():

    form = AddJineteForm()
    cargar_choices_form(form)

    return render_template("jya/agregar_jya.html", form=form)


@bp.post("/agregar_jinete")
@login_required
@check("jya_create")
def add_jinete():
    form = AddJineteForm(request.form)
    cargar_choices_form(form)

    if form.validate_on_submit():  # Asegurarse de que el formulario está correctamente validado
        # Obtener los objetos Localidad y Provincia
        localidad = jya.get_localidad_by_id(form.domicilio_localidad.data)
        provincia = jya.get_provincia_by_id(form.domicilio_provincia.data)

        # Crear el nuevo Domicilio
        nuevo_domicilio = jya.add_domiclio(
            calle=form.domicilio_calle.data,
            numero=form.domicilio_numero.data,
            departamento=form.domicilio_departamento.data,
            piso=form.domicilio_piso.data,
            localidad=localidad,
            provincia=provincia,
        )

        # Crear el nuevo Contacto de Emergencia
        nuevo_contacto_emergencia = jya.add_contacto_emergencia(
            nombre=form.contacto_emergencia_nombre.data,
            apellido=form.contacto_emergencia_apellido.data,
            telefono=form.contacto_emergencia_telefono.data,
        )

        dias_seleccionados = form.dias.data
        dias_db = Dias.query.filter(Dias.dias.in_(dias_seleccionados)).all()

        # Convertir los IDs de las discapacidades seleccionadas a objetos de la base de datos
        discapacidades_seleccionadas = form.discapacidades.data  # Esto trae los IDs seleccionados en el formulario
        discapacidades_db = TipoDiscapacidad.query.filter(TipoDiscapacidad.tipos_discapacidad.in_(discapacidades_seleccionadas)).all()

        dni= request.form["dni"]
        if jya.jinete_dni_exists(dni):
            flash("El DNI ya está registrado. Por favor elige otro.", "error")
            return redirect(url_for("jya.add_jinete_form"))

        # Crear el nuevo jinete con todos los datos
        nuevo_jinete = jya.create_jinete(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            dni=dni,
            edad=form.edad.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            localidad_nacimiento=localidad,
            provincia_nacimiento=provincia,
            domicilio=nuevo_domicilio,
            telefono=form.telefono.data,
            contacto_emergencia=nuevo_contacto_emergencia,
            becado=form.becado.data,
            observaciones_becado=form.observaciones_becado.data,
            certificado_discapacidad=form.certificado_discapacidad.data,
            diagnostico=form.diagnostico.data,
            otro=form.otro.data,
            beneficiario_pension=form.beneficiario_pension.data,
            pension=form.pension.data,
            asignacion_familiar=form.asignacion_familiar.data,
            tipo_asignacion=form.tipo_asignacion.data,
            obra_social=form.obra_social.data,
            nro_afiliado=form.nro_afiliado.data,
            curatela=form.curatela.data,
            observaciones_curatela=form.observaciones_curatela.data,
            nombre_institucion=form.nombre_institucion.data,
            direccion=nuevo_domicilio,
            telefono_institucion=form.telefono_institucion.data,
            grado=form.grado.data,
            observaciones_institucion=form.observaciones_institucion.data,
            profesionales=form.profesionales.data,
            trabajo_institucional=form.trabajo_institucional.data,
            condicion=form.condicion.data,
            sede=form.sede.data,
        )

        # Asociar los días seleccionados al jinete
        nuevo_jinete.dias.extend(dias_db)

        # Asociar las discapacidades seleccionadas al jinete
        nuevo_jinete.discapacidades.extend(discapacidades_db)

        #localidad = jya.get_localidad_by_id(form.localidad_familiar.data)
        #provincia = jya.get_provincia_by_id(form.provincia_familiar.data)
        # Crear el familiar asociado al jinete
        nuevo_familiar = jya.add_familiar(
            parentesco_familiar=form.parentesco_familiar.data,
            nombre_familiar=form.nombre_familiar.data,
            apellido_familiar=form.apellido_familiar.data,
            dni_familiar=form.dni_familiar.data,
            domicilio_familiar=nuevo_domicilio,
            #localidad_familiar=localidad,
            #provincia_familiar=provincia,
            celular_familiar=form.celular_familiar.data,
            email_familiar=form.email_familiar.data,
            nivel_escolaridad_familiar=form.nivel_escolaridad_familiar.data,
            actividad_ocupacion_familiar=form.actividad_ocupacion_familiar.data,
        )

        # Añadir el familiar a la lista de familiares del jinete
        nuevo_jinete.familiares.append(nuevo_familiar)

        nuevo_jinete.profesor_o_terapeuta_id = form.profesor_o_terapeuta.data
        nuevo_jinete.conductor_caballo_id = form.conductor_caballo.data
        nuevo_jinete.caballo_id = form.caballo.data
        nuevo_jinete.auxiliar_pista_id = form.auxiliar_pista.data

        # Guardar todo en la base de datos
        db.session.commit()

        flash("Jinete registrado exitosamente", "success")
        return redirect(url_for("jya.listar_jinetes"))

    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "error")

    return render_template("jya/agregar_jya.html", form=form)


@bp.get("/ver_jinete/<int:jinete_id>")
@login_required
@check("jya_show")
def view_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    page=request.args.get("page", 1, type=int)
    active_tab=request.args.get("tab", "general")
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    documentos = jya.traer_documentos(jinete_id, page=page, sort_by=sort_by, search=search)
    return render_template("jya/ver_jya.html", jinete=jinete, documentos=documentos, active_tab=active_tab)


@bp.get("/eliminar_jinete/<int:jinete_id>")
@login_required
@check("jya_destroy")
def delete_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/eliminar_jya.html", jinete=jinete)



@bp.post("/eliminar_jinete/<int:jinete_id>")
@login_required
@check("jya_destroy")
def delete_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    ##jya.delete_jinete(jinete_id)
    jya.aplicar_borrado_logico(jinete)
    return redirect(url_for("jya.listar_jinetes"))


def cargar_choices_form(form):
    # Cargar las opciones para los campos de selección
    form.pension.choices = [(p.name, p.value) for p in PensionEnum]
    form.diagnostico.choices = [(d.name, d.value) for d in DiagnosticoEnum]

    form.tipo_asignacion.choices = [(asig.name, asig.value) for asig in AsignacionEnum]
    form.domicilio_provincia.choices = [(p.id, p.nombre) for p in jya.list_provincias()]
    form.domicilio_localidad.choices = [(l.id, l.nombre) for l in jya.list_localidades()]

    form.localidad_nacimiento.choices = [(l.id, l.nombre) for l in jya.list_localidades()]
    form.provincia_nacimiento.choices = [(p.id, p.nombre) for p in jya.list_provincias()]

    form.institucion_direccion_localidad.choices = [(l.id, l.nombre) for l in jya.list_localidades()]
    form.institucion_direccion_provincia.choices = [(p.id, p.nombre) for p in jya.list_provincias()]

    form.domicilio_familiar_localidad.choices = [(l.id, l.nombre) for l in jya.list_localidades()]
    form.domicilio_familiar_provincia.choices = [(p.id, p.nombre) for p in jya.list_provincias()]

    form.caballo.choices = [(ecuestre.id, ecuestre.nombre) for ecuestre in list_ecuestre()]
    form.profesor_o_terapeuta.choices = [(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_terapeutas_y_profesores()]

    form.conductor_caballo.choices=[(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_conductores_caballos()]
    form.auxiliar_pista.choices=[(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_auxiliares_pista()]

    form.discapacidades.choices = [(tipo.name, tipo.value) for tipo in TiposDiscapacidadEnum]
    form.dias.choices = [(dia.name, dia.value) for dia in DiasEnum]
    form.nivel_escolaridad_familiar.choices = [(esc.name, esc.value) for esc in EscolaridadEnum]

@bp.get("/editar_jinete/<int:jinete_id>")
@login_required
@check("jya_update")
def edit_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    fecha_nacimiento = jinete.fecha_nacimiento.strftime('%Y-%m-%d') if jinete.fecha_nacimiento else ''
    tipos_discapacidad = jya.list_discapacidades()
    dias_semana = jya.list_dias_semana()
    jinete_dias_semana = jya.list_jinete_dias_semana(jinete_id)
    localidades = equipo.list_localidades()
    provincias = equipo.list_provincias()
    tipos_diagnostico =  jya.list_tipos_diagnostico()
    tipos_de_asignacion = jya.list_tipos_asignacion()
    tipos_pensiones = jya.list_tipos_pensiones()
    trabajos_institucionales = jya.list_trabajo_institucional()
    list_sedes = jya.list_sedes()
    list_profes_terapeutas = equipo.list_terapeutas_y_profesores()
    list_conductores = equipo.list_conductores_caballos()
    list_auxiliares_pista = equipo.list_auxiliares_pista()
    list_caballos = list_ecuestre()
    jinete_dias_name = [dia['name'] for dia in jinete_dias_semana if 'name' in dia]
    jinete_tipos_discapacidades = jya.list_jinete_tipos_discapacidades(jinete_id)
    jinete_tipos_discapacidad_name = [disc['name'] for disc in jinete_tipos_discapacidades if 'name' in disc]
    list_nivel_escolaridad=jya.list_nivel_escolaridad()
    familiar = jya.get_primer_familiar(jinete_id)



    return render_template("jya/editar_jya.html", jinete=jinete, fecha_nacimiento=fecha_nacimiento, jinete_dias_name=jinete_dias_name, jinete_tipos_discapacidad_name=jinete_tipos_discapacidad_name,
        jinete_tipos_discapacidades=jinete_tipos_discapacidades, tipos_discapacidad=tipos_discapacidad,dias_semana=dias_semana,jinete_dias_semana=jinete_dias_semana,localidades=localidades,
        provincias=provincias, tipos_diagnostico=tipos_diagnostico,tipos_de_asignacion=tipos_de_asignacion,tipos_pensiones=tipos_pensiones,
        familiar=familiar,trabajos_institucionales=trabajos_institucionales,list_sedes=list_sedes,
        list_profes_terapeutas=list_profes_terapeutas,
        list_conductores=list_conductores,
        list_auxiliares_pista=list_auxiliares_pista,
        list_nivel_escolaridad=list_nivel_escolaridad,
        list_caballos=list_caballos, form=form)



#agregar que levante el "nuevo_familiar"
@bp.post("/editar_jinete/<int:jinete_id>")
@login_required
@check("jya_update")
def editar_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = request.form

    jinete.nombre = form["nombre"]
    jinete.apellido = form["apellido"]
    jinete.dni = form["dni"]
    jinete.edad = form["edad"]
    jinete.fecha_nacimiento = form["fecha_nacimiento"]
    jinete.provincia_nacimiento_id = form["provincia_nacimiento"]
    jinete.localidad_nacimiento_id = form["localidad_nacimiento"]
    #domicilio actual
    jinete.domicilio.calle = form["domicilio.calle"]
    jinete.domicilio.numero = form["domicilio.numero"]
    jinete.domicilio.piso= form["domicilio.piso"] if (form["domicilio.piso"] and form["domicilio.piso"] !="") else None
    jinete.domicilio.departamento= form["domicilio.departamento"] if (form["domicilio.departamento"] and form["domicilio.departamento"] !="") else None
    jinete.domicilio.provincia_id = form["domicilio.provincia"]
    jinete.domicilio.localidad_id = form["domicilio.localidad"]
    jinete.telefono = form["telefono"]
    #contacto emergencia:
    jinete.contacto_emergencia.nombre= form["contacto_emergencia.nombre"]
    jinete.contacto_emergencia.apellido= form["contacto_emergencia.apellido"]
    jinete.contacto_emergencia.telefono= form["contacto_emergencia.telefono"]
    #empieza:
    jinete.estado_pago = (form["estado_pago"] == "si")
    jinete.becado = (form["becado"] == "si")
    jinete.observaciones_becado = form["observaciones_becado"]
    jinete.certificado_discapacidad = (form["certificado_discapacidad"] == "si")
    jinete.diagnostico = form["diagnostico"] if  (form["diagnostico"] and form["diagnostico"] !="") else None
    jinete.otro = form["otro"]  if (form["otro"] and form["otro"] !="") else None

    #tipos_discapacidades:
    jya.clear_jinete_discapacidades(jinete_id)
    for tipo in form.getlist("tipos_discapacidad[]"):
        jya.associate_jinete_discapacidad_name(jinete_id, tipo)

    jinete.asignacion_familiar = (form["asignacion"] == "si")
    jinete.tipo_asignacion = form.get("tipo_asignacion") if form.get("tipo_asignacion") and form.get("tipo_asignacion") != "" else None
    jinete.beneficiario_pension = (form["beneficiario_pension"] == "si")
    jinete.pension = form.get("pension") if form.get("pension") and form.get("pension") != "" else None
    jinete.obra_social = form["obra_social"]
    jinete.nro_afiliado = form["nro_afiliado"]
    jinete.curatela = (form["curatela"] == "si")
    jinete.observaciones_curatela = form["observaciones_curatela"]

    #Institucion escolar:
    jinete.nombre_institucion = form["nombre_institucion"]
    jinete.direccion.calle = form["direccion.calle"]
    jinete.direccion.numero = form["direccion.numero"]
    jinete.direccion.piso= form["direccion.piso"] if (form["direccion.piso"] and form["direccion.piso"] !="") else None
    jinete.direccion.departamento= form["direccion.departamento"] if (form["direccion.departamento"] and form["direccion.departamento"] !="") else None
    jinete.direccion.provincia_id = form["direccion.provincia"]
    jinete.direccion.localidad_id = form["direccion.localidad"]
    jinete.telefono_institucion = form["telefono_institucion"]
    jinete.grado = form["grado"]
    jinete.observaciones_institucion = form["observaciones_institucion"]
    jinete.profesionales = form.get("profesionales") if form.get("profesionales") and form.get("profesionales") != "" else None

    #levanto campos del familiar:
    parentezco_familiar = form.get("familiar.parentesco_familiar") or None
    nombre_familiar = form.get("familiar.nombre_familiar") or None
    apellido_familiar = form.get("familiar.apellido_familiar") or None
    dni_familiar = form.get("familiar.dni_familiar") or None
    domicilio_familiar_calle = form.get("domicilio_familiar.calle") or None
    domicilio_familiar_numero = form.get("domicilio_familiar.numero") or None
    domicilio_familiar_piso = form.get("domicilio_familiar.piso") or None
    domicilio_familiar_departamento = form.get("domicilio_familiar.departamento") or None
    domicilio_familiar_provincia_id = form.get("familiar.domicilio_familiar_provincia") or None
    domicilio_familiar_localidad_id = form.get("familiar.domicilio_familiar_localidad") or None
    celular_familiar = form.get("familiar.celular_familiar") or None
    email_familiar = form.get("familiar.email_familiar") or None
    nivel_escolaridad_familiar = form.get("familiar.nivel_escolaridad_familiar") or None
    actividad_ocupacion_familiar = form.get("familiar.actividad_ocupacion_familiar") or None

    if jinete.familiares:
        familiar_id= jya.get_primer_familiar(jinete_id).id
        jya.edit_familiar(familiar_id=familiar_id, parentezco_familiar=parentezco_familiar, nombre_familiar=nombre_familiar,apellido_familiar=apellido_familiar, dni_familiar=dni_familiar,domicilio_familiar_calle=domicilio_familiar_calle,domicilio_familiar_numero=domicilio_familiar_numero,
                        domicilio_familiar_piso=domicilio_familiar_piso, domicilio_familiar_departamento=domicilio_familiar_departamento, domicilio_familiar_provincia_id=domicilio_familiar_provincia_id,domicilio_familiar_localidad_id=domicilio_familiar_localidad_id,celular_familiar=celular_familiar,
                        email_familiar=email_familiar, nivel_escolaridad_familiar=nivel_escolaridad_familiar, actividad_ocupacion_familiar=actividad_ocupacion_familiar)
    else:
        jya.add_familiar(familiar_id=familiar_id, parentezco_familiar=parentezco_familiar, nombre_familiar=nombre_familiar,apellido_familiar=apellido_familiar, dni_familiar=dni_familiar,domicilio_familiar_calle=domicilio_familiar_calle,domicilio_familiar_numero=domicilio_familiar_numero,
                        domicilio_familiar_piso=domicilio_familiar_piso, domicilio_familiar_departamento=domicilio_familiar_departamento, domicilio_familiar_provincia_id=domicilio_familiar_provincia_id,domicilio_familiar_localidad_id=domicilio_familiar_localidad_id,celular_familiar=celular_familiar,
                        email_familiar=email_familiar, nivel_escolaridad_familiar=nivel_escolaridad_familiar, actividad_ocupacion_familiar=actividad_ocupacion_familiar)


    # trabajo en institucion:
    jinete.trabajo_institucional = form.get("trabajo_institucional")
    jinete.condicion = (form["condicion"]  == "si")
    jinete.sede = form.get("sede")
    # dias:
    jya.clear_jinete_dias(jinete_id)
    for dia_name in form.getlist("dias_semana"):
    # asignacion de dias:
        jya.associate_jinete_dias_name(jinete_id,dia_name)



    jinete.profesor_o_terapeuta_id = form.get("profesor_o_terapeuta")
    jinete.conductor_caballo_id = form.get("conductor_caballo")
    jinete.caballo_id = form.get("caballo")
    jinete.auxiliar_pista_id = form.get("auxiliar_pista")

    flash("Jinete actualizado  exitosamente", "success")
    db.session.commit()
    return redirect(url_for("jya.view_jinete",jinete_id=jinete.id))





# AGREGAR ARCHIVO GET
@bp.get("/<int:jinete_id>/agregar_documento")
@login_required
@check("jya_update")
def add_documento_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)

    return render_template("jya/add_documento.html", jinete=jinete)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


MAX_CANT_MEGABYTES = 20  # cant megabytes
MAX_CONTENT_LENGTH = MAX_CANT_MEGABYTES * 1024 * 1024

@bp.before_request
def limit_content_length():
    if request.content_length is not None and request.content_length > MAX_CONTENT_LENGTH:
        abort(413)  # Payload Too Large

'''# AGREGAR DOCUMENTO
@bp.post("/<int:jinete_id>/update")
@login_required
@check("jya_update")
def update(jinete_id):
    params = request.form.copy()

    if "documento" not in request.files or request.files["documento"].filename == "":
        flash("El archivo es obligatorio.", "error")  # Mensaje de error
        return redirect(url_for("jya.subir_archivo_form", jinete_id=jinete_id))

    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size

        #ulid = u.new()

        client.put_object(
            "grupo15", file.filename, file, size, content_type=file.content_type
        )           #f"avatars/{ulid}-{file.filename}",
        params["documento"] = file.filename #Hacer funcion para que genere nombres unicos para el archivo y guardarlo en el usuario. Libreria ULID

    jya.update_jinete(jinete_id, **params)
    flash("Usuario modificado correctamente", "success")

    return redirect(url_for("jya.listar_jinetes"))'''

# AGREGAR ARCHIVO POST
@bp.post("/<int:jinete_id>/agregar_documento")
@login_required
@check("jya_update")
def agregar_documento(jinete_id):
    params = request.form.copy()
    if "documento" not in request.files or request.files["documento"].filename == "":
        flash("El archivo es obligatorio.", "error")  # Mensaje de error
        return redirect(url_for("jya.add_documento_form", jinete_id=jinete_id))

    if "documento" in request.files:
        file = request.files["documento"]
        if not allowed_file(file.filename):
            flash("Tipo de archivo no permitido.", "error")
            return redirect(url_for("jya.add_documento_form", jinete_id=jinete_id))

        if file.content_length > MAX_CONTENT_LENGTH:
            flash("El archivo excede el tamaño máximo permitido de 5 MB.", "error")
            return redirect(url_for("jya.add_documento_form", jinete_id=jinete_id))

        tipo_documento = request.form.get("tipo_documento")
        if not tipo_documento:
            flash("Debe seleccionar un tipo de archivo.", "error")
            return redirect(url_for("jya.add_documento_form", form=request.form, jinete_id=jinete_id))
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size

        nuevo_nombre_archivo = f"jya_{jinete_id}_{file.filename}"
        client.put_object("grupo15", nuevo_nombre_archivo, file, size, content_type=file.content_type)
        jya.add_documento(
            titulo_documento=file.filename,
            nombre_archivo=request.form["nombre_archivo"],
            tipo_documento=request.form["tipo_documento"],
            jinete_id=jinete_id
        )

    flash("Documento agregado exitosamente", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))

# DESCARGAR ARCHIVO
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<string:file_name>")
@login_required
@check("jya_show")
def mostrar_archivo(jinete_id, file_name):
    client = current_app.storage.client
    nuevo_nombre_archivo = f"jya_{jinete_id}_{file_name}"
    expiration = timedelta(seconds=120)
    url =  client.presigned_get_object("grupo15", nuevo_nombre_archivo, expires=expiration) # Esto sirve para archivos sensibles como documento de jya.
    return redirect(url)



# ELIMINAR ARCHIVO GET
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/eliminar")
@login_required
@check("jya_destroy")
def eliminar_documento_form(jinete_id, documento_id):
    jinete = jya.traer_jinete(jinete_id)
    documento = jya.traer_documento_id(documento_id)
    return render_template("jya/delete_documento.html", jinete=jinete, doc=documento)

# ELIMINAR ARCHIVO POST
@bp.post("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/eliminar")
@login_required
@check("jya_destroy")
def eliminar_documento(jinete_id, documento_id):
    documento = jya.traer_documento_id(documento_id)
    if not documento.is_enlace:
        client = current_app.storage.client
        nuevo_nombre_archivo = f"jya_{jinete_id}_{documento.titulo_documento}"
        client.remove_object("grupo15", nuevo_nombre_archivo)
    jya.delete_documento(documento_id)
    flash("Documento eliminado correctamente.", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id, tab='documentos'))




# EDITAR ARCHIVO GET
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/editar")
@login_required
@check("jya_update")
def edit_documento_form(jinete_id, documento_id):
    documento = jya.traer_documento_id(documento_id)
    return render_template("jya/edit_documento.html", documento=documento, jinete_id=jinete_id)


# EDITAR ARCHIVO POST
@bp.post("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/editar")
@login_required
@check("jya_update")
def editar_documento(jinete_id, documento_id):
    documento = jya.traer_documento_id(documento_id)

    tipo_documento = request.form.get("tipo_documento")
    nombre_archivo = request.form.get("nombre_archivo")

    if not tipo_documento:
        flash("Debe ingresar un titulo de documento.", "error")
        return redirect(url_for("jya.edit_documento_form", form=request.form, documento_id=documento_id))

    if not tipo_documento:
        flash("Debe seleccionar un tipo de archivo.", "error")
        return redirect(url_for("jya.edit_documento_form", form=request.form, documento_id=documento_id))

    jya.edit_documento(jinete_id=jinete_id, tipo_documento=tipo_documento, nombre_archivo=nombre_archivo)
    flash("Documento editado exitosamente", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))


# ENLACES
# agregar enlace GET
@login_required
@check("jya_update")
@bp.get("/editar_jinete/<int:jinete_id>/enlace")
def subir_enlace_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)

    return render_template("jya/add_enlace.html", jinete=jinete)

# agregar enlace POST
@login_required
@check("jya_update")
@bp.post("/editar_jinete/<int:jinete_id>/enlace")
def agregar_enlace(jinete_id):
    jya.add_documento_tipo_enlace(
        jinete_id=jinete_id,
        url_enlace = request.form["url_enlace"],
        nombre_archivo=request.form["nombre_asignado"]
    )
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))



# EDITAR enlace GET
@bp.get("/editar_jinete/<int:jinete_id>/enlace/<int:documento_id>/editar")
@login_required
@check("jya_update")
def edit_enlace_form(jinete_id, documento_id):
    documento = jya.get_documento(documento_id)
    return render_template("jya/edit_enlace.html", documento=documento, jinete_id=jinete_id)


# EDITAR enlace POST
@bp.post("/editar_jinete/<int:jinete_id>/enlace/<int:documento_id>/editar")
@login_required
@check("jya_update")
def editar_enlace(jinete_id, documento_id):
    nombre_archivo = request.form.get("nombre_asignado")
    url_enlace = request.form.get("url_enlace")

    if not nombre_archivo:
        flash("Debe ingresar un titulo de documento.", "error")
        return redirect(url_for("jya.edit_enlace_form", form=request.form, documento_id=documento_id))

    if not url_enlace:
        flash("Debe ingresar una url para el enlace.", "error")
        return redirect(url_for("jya.edit_enlace_form", form=request.form, documento_id=documento_id))

    jya.edit_documento(documento_id=documento_id,jinete_id=jinete_id, nombre_archivo=nombre_archivo, url_enlace=url_enlace)
    flash("Documento editado exitosamente", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))

@bp.route("/toggle_estado_pago/<int:jinete_id>", methods=["POST"])
@login_required
@check("jya_update")
def toggle_estado_pago(jinete_id):
    jinete = jya.traer_jinete(jinete_id)

    if not jinete:
        flash("El jinete no existe.", "error")
        return redirect(url_for("jya.listar_jinetes"))
    jinete.estado_pago = not jinete.estado_pago
    db.session.commit()

    nuevo_estado = "Al día" if jinete.estado_pago else "En deuda"
    flash(f"El estado de pago del jinete se ha cambiado a: {nuevo_estado}.", "success")
    return redirect(url_for("jya.listar_jinetes"))
