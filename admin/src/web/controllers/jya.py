from flask import abort, render_template, request, redirect, flash, url_for, current_app
from flask import abort, render_template, request, redirect, flash, url_for, current_app
from os import fstat
from flask import Blueprint
from src.core import auth
from src.core import jya
from src.core import equipo
from src.core.database import db
from src.core.jya.forms import AddJineteForm
from src.core.jya.models import Jinete, PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum, Dias, DiasEnum, Familiar, JineteDocumento, TipoDiscapacidad
from src.core.equipo import list_terapeutas_y_profesores, list_auxiliares_pista, list_conductores_caballos
from src.core.ecuestre import list_ecuestre

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
    cargar_choices_form(form)

    return render_template("jya/agregar_jya.html", form=form)


@bp.post("/agregar_jinete")
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

        # Crear el nuevo jinete con todos los datos
        nuevo_jinete = jya.create_jinete(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            dni=form.dni.data,
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
        
        localidad = jya.get_localidad_by_id(form.localidad_familiar.data)
        provincia = jya.get_provincia_by_id(form.provincia_familiar.data)
        # Crear el familiar asociado al jinete
        nuevo_familiar = jya.add_familiar(
            parentesco_familiar=form.parentesco_familiar.data,
            nombre_familiar=form.nombre_familiar.data,
            apellido_familiar=form.apellido_familiar.data,
            dni_familiar=form.dni_familiar.data,
            direccion_familiar=form.direccion_familiar.data,
            localidad_familiar=localidad,
            provincia_familiar=provincia,
            celular_familiar=form.celular_familiar.data,
            email_familiar=form.email_familiar.data,
            nivel_escolaridad_familiar=form.nivel_escolaridad_familiar.data,
            actividad_ocupacion_familiar=form.actividad_ocupacion_familiar.data,
        )

        # Añadir el familiar a la lista de familiares del jinete
        nuevo_jinete.familiares.append(nuevo_familiar)

        # Guardar todo en la base de datos
        db.session.commit()

        flash("Jinete registrado exitosamente", "success")
        return redirect(url_for("jya.listar_jinetes"))

    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")

    return render_template("jya/agregar_jya.html", form=form)


@bp.get("/ver_jinete/<int:jinete_id>")
def view_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    page=request.args.get("page", 1, type=int)
    active_tab=request.args.get("tab", "general")
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    documentos = jya.traer_documentos(jinete_id, page=page, sort_by=sort_by, search=search)
    page=request.args.get("page", 1, type=int)
    active_tab=request.args.get("tab", "general")
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    documentos = jya.traer_documentos(jinete_id, page=page, sort_by=sort_by, search=search)
    #tipos_discapacidad_nombres = [tipo.name for tipo in jinete.tipos_discapacidad] if jinete.tipos_discapacidad else []
    #dias_nombres = [d.name for d in jinete.dia] if jinete.dia else []
    #return render_template("jya/ver_jya.html", jinete=jinete, tipos_discapacidad=tipos_discapacidad_nombres, dia=dias_nombres, documentos=documentos)
    return render_template("jya/ver_jya.html", jinete=jinete, documentos=documentos, active_tab=active_tab)
    




@bp.get("/eliminar_jinete/<int:jinete_id>")
def delete_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/eliminar_jya.html", jinete=jinete)



@bp.post("/eliminar_jinete/<int:jinete_id>")
def delete_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    jya.delete_jinete(jinete_id)
    
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
    
    form.localidad_familiar.choices = [(l.id, l.nombre) for l in jya.list_localidades()]
    form.provincia_familiar.choices = [(p.id, p.nombre) for p in jya.list_provincias()]
        
    form.caballo.choices = [(ecuestre.id, ecuestre.nombre) for ecuestre in list_ecuestre()]
    form.profesor_o_terapeuta.choices = [(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_terapeutas_y_profesores()]

    form.conductor_caballo.choices=[(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_conductores_caballos()]
    form.auxiliar_pista.choices=[(emp.id, f"{emp.apellido}, {emp.nombre}") for emp in list_auxiliares_pista()]

    form.discapacidades.choices = [(tipo.name, tipo.value) for tipo in TiposDiscapacidadEnum]
    form.dias.choices = [(dia.name, dia.value) for dia in DiasEnum]


@bp.get("/editar_jinete/<int:jinete_id>")
def edit_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)
    fecha_nacimiento = jinete.fecha_nacimiento.strftime('%Y-%m-%d') if jinete.fecha_nacimiento else ''
    tipos_discapacidad = jya.list_discapacidades()
    jinete_tipos_discapacidades = jya.list_jinete_tipos_discapacidades(jinete_id)
    dias_semana = jya.list_dias_semana()
    jinete_dias_semana = jya.list_jinete_dias_semana(jinete_id)
    localidades = equipo.list_localidades()
    provincias = equipo.list_provincias()
    tipos_diagnostico =  jya.list_tipos_diagnostico()
    tipos_de_asignacion = jya.list_tipos_asignacion()
    tipos_pensiones = jya.list_tipos_pensiones()
    familiares = jya.list_familiares_por_jinete(jinete_id)
    trabajos_institucionales = jya.list_trabajo_institucional()
    list_sedes = jya.list_sedes()
    list_profes_terapeutas = equipo.list_terapeutas_y_profesores()
    list_conductores = equipo.list_conductores_caballos()
    list_auxiliares_pista = equipo.list_auxiliares_pista()
    list_caballos = list_ecuestre()
    jinete_dias_name = [dia['name'] for dia in jinete_dias_semana if 'name' in dia]
    tipos_discapacidad_name = [disc['name'] for disc in jinete_tipos_discapacidades if 'name' in disc]
    
    return render_template("jya/editar_jya.html", jinete=jinete, fecha_nacimiento=fecha_nacimiento, jinete_dias_name=jinete_dias_name, tipos_discapacidad_name=tipos_discapacidad_name,
        jinete_tipos_discapacidades=jinete_tipos_discapacidades, tipos_discapacidad=tipos_discapacidad,dias_semana=dias_semana,jinete_dias_semana=jinete_dias_semana,localidades=localidades,
        provincias=provincias, tipos_diagnostico=tipos_diagnostico,tipos_de_asignacion=tipos_de_asignacion,tipos_pensiones=tipos_pensiones, 
        familiares=familiares,trabajos_institucionales=trabajos_institucionales,list_sedes=list_sedes,
        list_profes_terapeutas=list_profes_terapeutas,
        list_conductores=list_conductores,
        list_auxiliares_pista=list_auxiliares_pista,
        list_caballos=list_caballos, form=form)


#agregar que levante el "nuevo_familiar"
@bp.post("/editar_jinete/<int:jinete_id>")
def editar_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    form = AddJineteForm(obj=jinete)  
    
    cargar_choices_form(form)
    #form.tipos_discapacidad.data = [d.id for d in jinete.tipos_discapacidad]
    #form.tipos_discapacidad.data = [tipo.value for tipo in jinete.tipos_discapacidad]
    #form.dia.data = [d.value for d in jinete.dia]
    if form.validate_on_submit():
        # Actualizar los datos del jinete con los valores del formulario
        form.populate_obj(jinete)
        #jinete.discapacidades = [TipoDiscapacidad.query.get(d_id) for d_id in form.discapacidades.data]
                
        for i, doc_data in enumerate(form.documentos.data):
            if len(jinete.documentos) > i:
                # Actualizar documento existente
                for key, value in doc_data.items():
                    setattr(jinete.documentos[i], key, value)
            else:
                # Añadir nuevo documento
                nuevo_documento = JineteDocumento(**doc_data)
                nuevo_documento = JineteDocumento(**doc_data)
                jinete.documentos.append(nuevo_documento)

        # Asignar los valores del domicilio
        jinete.domicilio.calle = form.domicilio_calle.data
        jinete.domicilio.numero = form.domicilio_numero.data
        jinete.domicilio.piso = form.domicilio_piso.data
        jinete.domicilio.departamento = form.domicilio_departamento.data
        jinete.domicilio.localidad_id = (
            form.domicilio_localidad.data
        )  # Asegúrate de que `localidad` es el ID
        jinete.domicilio.provincia_id = (
            form.domicilio_provincia.data
        )  # Asegúrate de que `provincia` es el ID


        # Asignar los valores del contacto de emergencia
        jinete.contacto_emergencia.nombre = form.contacto_emergencia_nombre.data
        jinete.contacto_emergencia.apellido = form.contacto_emergencia_apellido.data
        jinete.contacto_emergencia.telefono = form.contacto_emergencia_telefono.data



        # Valores arreglados.
        jinete.localidad_nacimiento_id = form.localidad_nacimiento.data 
        jinete.provincia_nacimiento_id = form.provincia_nacimiento.data 
        # Guardar los cambios en la base de datos
        flash("Jinete actualizado  exitosamente", "success")
        db.session.commit()
        return view_jinete(jinete_id=jinete.id)
    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")

    return render_template("jya/editar_jya.html", form=form, jinete=jinete)





@bp.get("/<int:jinete_id>/edit")
def edit(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    
    return render_template("jya/edit.html", jinete=jinete)


@bp.post("/<int:jinete_id>/update")
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
    
    return redirect(url_for("jya.listar_jinetes"))


# AGREGAR ARCHIVO GET
@bp.get("/<int:jinete_id>/agregar_documento")
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

# AGREGAR ARCHIVO POST
@bp.post("/<int:jinete_id>/agregar_documento")
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
        client.put_object("grupo15", file.filename, file, size, content_type=file.content_type)
        jya.add_documento(
            nombre_archivo=file.filename,
            titulo_documento=request.form["titulo_documento"],
            tipo_documento=request.form["tipo_documento"], 
            jinete_id=jinete_id
        ) 
    
    flash("Documento agregado exitosamente", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))

# DESCARGAR ARCHIVO
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<string:file_name>") 
def mostrar_archivo(jinete_id, file_name):
    client = current_app.storage.client
    url = client.presigned_get_object("grupo15", file_name, ExpiresIn=10800)  # 3 horas en segundos
    return redirect(url)

# ELIMINAR ARCHIVO GET
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/eliminar")
def eliminar_documento_form(jinete_id, documento_id):
    jinete = jya.traer_jinete(jinete_id)
    documento = jya.traer_documento_id(documento_id)
    return render_template("jya/delete_documento.html", jinete=jinete, doc=documento)

# ELIMINAR ARCHIVO POST
@bp.post("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/eliminar")
def eliminar_documento(jinete_id, documento_id):
    jya.delete_documento(documento_id)
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id, tab='documentos'))

# EDITAR ARCHIVO GET
@bp.get("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/editar")
def editar_documento_form(documento_id, jinete_id):
    documento = jya.traer_documento_id(documento_id)
    return render_template("jya/edit_documento.html", documento=documento, jinete_id=jinete_id)


# EDITAR ARCHIVO POST
@bp.post("/editar_jinete/<int:jinete_id>/documentos/<int:documento_id>/editar")
def editar_documento(documento_id, jinete_id):

    if "documento" not in request.files or request.files["documento"].filename == "":
        flash("El archivo es obligatorio.", "error")  # Mensaje de error
        return redirect(url_for("jya.edit_documento_form", documento_id=documento_id))

    if "documento" in request.files:
        file = request.files["documento"]
        if not allowed_file(file.filename):
            flash("Tipo de archivo no permitido.", "error")
            return redirect(url_for("jya.edit_documento_form", documento_id=documento_id))

        if file.content_length > MAX_CONTENT_LENGTH:
            flash("El archivo excede el tamaño máximo permitido de 5 MB.", "error")
            return redirect(url_for("jya.edit_documento_form", documento_id=documento_id))

        tipo_documento = request.form.get("tipo_documento")
        if not tipo_documento:
            flash("Debe seleccionar un tipo de archivo.", "error")
            return redirect(url_for("jya.edit_documento_form", form=request.form, documento_id=documento_id))
        
    flash("Documento editado exitosamente", "success")
    return redirect(url_for("jya.view_jinete", jinete_id=jinete_id))
