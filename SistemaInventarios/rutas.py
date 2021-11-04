from flask import render_template, redirect, request, flash, jsonify, make_response, session, url_for
from SistemaInventarios.dashboard import appDash
from SistemaInventarios.dashboard import dashboard_principal

from datetime import date
from random import randint

from SistemaInventarios.modelsDB import *
from SistemaInventarios.config import dev2
import SistemaInventarios.crud as crud

from werkzeug.security import generate_password_hash, check_password_hash

def quitar_nones(dic):
    rta= {}
    for clave, valor in dic.items():
        if valor != None:
            rta[clave] = valor
    return rta

def miFlash(mensaje):
    flash(mensaje+". ")

def opcBusquedaHTML(listBusqueda, campoSelec=""):
    opciones = ""
    for campo,opc in listBusqueda.items():
        if campo == campoSelec:
            txtSelected = "selected"
        else:
            txtSelected = ""
        opciones += f'<option value="{campo}" {txtSelected}>{opc[0]}</option>'
    return(opciones)

def opcMenuHTML(permisosUsuario):
    opcMenu = ""
    if "ver" in permisosUsuario["Usuarios"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/usuarios">Usuarios</a></li>\n'
    if "ver" in permisosUsuario["Proveedores"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/proveedores">Proveedores</a></li>\n'
    if "ver" in permisosUsuario["Productos"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/productos">Productos</a></li>\n'
    if "ver" in permisosUsuario["Dashboard"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/dashboard">Dashboard</a></li>\n'
    opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/cerrarSesion">Cerrar Sesión</a></li>\n'
    return(opcMenu)


appDash.server.config.from_object(dev2)

bd.init_app(appDash.server)

# Interacción de Proveedores
cabeceraProv = ("Nit","Razón Social","Dirección","Telefono","email","estado","acciones")

# Interacción de Usuarios
cabeceraUsuar = ("Usuario","Nombre","Perfil","Estado","acciones")

# Interacción de Productos
cabeceraProd = ("Identificador","Nombre"," Cantidad Minima","Cantidad Disponible","Estado","acciones")

listaBusquedaUsuarios = {
    "usuario": ["Usuario","=="],
    "nombre": ["Nombre","in"],
    "tipoUsuario": ["Perfil","=="],
    "estado": ["Estado","=="],
}
opcionesUsuarios = opcBusquedaHTML(listaBusquedaUsuarios)

listaBusquedaProveedores = {
    "nit": ["Nit", "=="],
    "nombre": ["Razon Social", "in"],
    "direccion": ["Direccion", "in"],
    "telefono": ["Telefono", "in"],
    "email": ["Email", "in"],
    "estado": ["Estado", "=="],
}
opcionesProveedores = opcBusquedaHTML(listaBusquedaProveedores)

listaBusquedaProductos = {
    "idProducto": ["Identificador", "=="],
    "nombre": ["Nombre", "In"],
    "descripcion": ["Descripcion", "in"],
    "estado": ["Estado", "=="],
}
opcionesProductos = opcBusquedaHTML(listaBusquedaProductos)


@appDash.server.route('/', methods=['GET'])
def raiz():
    return redirect(url_for("index"))


@appDash.server.route('/index', methods=['GET'])
def index():
    rtaHTML = make_response(render_template("index.html"))
    return rtaHTML


@appDash.server.route('/cerrarSesion', methods=['GET'])
def cerrarSesion():
    # Borra las variables de sesión creadas
    session.clear()
    return redirect(url_for("index"))


@appDash.server.route('/ajaxValidarLogin', methods=['POST'])
def ajaxValidarLogin():
    #print("entro /ajaxValidarLogin")
    global usuarios
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        userName = request.form['username']
        password = request.form['password']
        #print("userName:", userName)
        #print("password:", password)
        
        usuario = crud.consultar_usuario(usuario = userName)
        #print("usuario.idUsuario:", usuario)

        if usuario != None and check_password_hash("pbkdf2:sha256:"+usuario.clave, password):
            # Usuario y clave correctos
            #print("usuario.idUsuario:", usuario.idUsuario)
            #print("usuario.cambiarClave:", usuario.cambiarClave)
            #print("usuario.aceptarPolitica:", usuario.aceptarPolitica)
            if usuario.cambiarClave == 1 or usuario.aceptarPolitica == 0:
                # Se debe llamar al formulario de cambio de clave y/o politica de datos.
                #print("entro /ajaxValidarLogin")
                usuario.clave = ""

                if usuario.aceptarPolitica == 1:
                    usuario.aceptarPoliticaChk = "checked"
                else:
                    usuario.aceptarPoliticaChk = ""

                rtaHTML = render_template('regUsuario.html', infoUsuario=usuario)

                # rta=1, para indicar que debe desplegar la ventana "modal".
                return jsonify({'rta': 1, 'htmlresponse': rtaHTML})

            else:
                # Ingresar al sistema
                session['idUsuario'] = usuario.idUsuario
                session['usuario'] = usuario.usuario
                session['tipoUsuario'] = usuario.tipoUsuario
                #return redirect(url_for("inicio"))

                # rta=2, para indicar que debe desplegar la ventana "/inicio".
                return jsonify({'rta': 2, 'otraRuta': '/inicio'})

        else:
            # Usuario o clave incorrecta.
            miFlash("Datos de ingreso incorrectos")
            # Borra las variables de sesión creadas
            session.clear()
            #return redirect(url_for("index"))
            # rta=3, para indicar que debe desplegar la ventana "/index".
            return jsonify({'rta': 2, 'otraRuta': '/index'})

    else:
        # Entra cuando el llamado es hecho por metodo GET.
        return redirect(url_for("index"))


@appDash.server.route('/registrarUsuario', methods=['POST'])
def registroUsuario():
    #print("entro /registroUsuario")
    if request.method == 'POST':
        datosUsuario = {
            'idUsuario': int(request.form['idUsuario']),
            'cedula': None,
            'usuario': None,
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'direccion': request.form['direccion'],
            'tipoUsuario': None,
            'estado': None,
            'clave': request.form['clave'].strip(),
            'cambiarClave': None,
            'aceptarPolitica': (1 if 'aceptarPolitica' in request.form else 0),
            'idUsuarioCrea_id': None,
            'idUsuarioEdita_id': int(request.form['idUsuario']),
        }
        usuario = crud.Usuario(datosUsuario)
        #print("datosUsuario['aceptarPolitica']:", datosUsuario['aceptarPolitica'])

        # Quitar la llave para que no se actualice.
        datosUsuario.pop("idUsuario")

        if len(datosUsuario['clave']) > 0:
            # Si digito una clave se encripta.
            #print("Si digito clave", datosUsuario['clave'])
            datosUsuario['clave'] = generate_password_hash(datosUsuario['clave']).split(":")[2]
            # Se resetea el indicador de cambio de clave.
            datosUsuario['cambiarClave'] = 0
        else:
            #print("No digito clave")
            # No digito clave, se quita el campo para que no lo actualice.
            datosUsuario.pop("clave")

        # Elimina campos con valor None en los datos del registro.
        datosUsuario = quitar_nones(datosUsuario)
        rta = crud.actualizar_usuario(usuario.idUsuario, datosUsuario)
        #print("rta:", rta)
        
        usuario = crud.consultar_usuario(idUsuario = usuario.idUsuario)
        if usuario.cambiarClave == 0 and usuario.aceptarPolitica == 1:
            # Cambio exitosamente la clave o acepto la politica de datos,
            # por lo caul se le permite ingresar al sistema.
            #print("cambio clave o acepto politica")
            session['idUsuario'] = usuario.idUsuario
            session['usuario'] = usuario.usuario
            session['tipoUsuario'] = usuario.tipoUsuario
            return redirect(url_for("inicio"))
        else:
            #print("No cambio clave o  no acepto politica")
            # Se lo devuelve al index.
            if rta == 1:
                miFlash("Registro Actualizado, sin cambio de clave o  aceptar politica")
            else:
                miFlash("Fallo la actualización del registro")
            return redirect(url_for("index"))

    else:
        return redirect(url_for("index"))


@appDash.server.route('/inicio', methods=['GET'])
def inicio():
    if "usuario" in session:
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        rtaHTML = make_response(render_template("Inicio.html", title="Inicio", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))
        return rtaHTML
    else:
        return redirect(url_for("index"))


#LOGICA USUARIOS
@appDash.server.route('/usuarios', methods=['GET'])
def usuarios():
    global opcionesUsuarios, cabeceraUsuar
    
    if "usuario" in session:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        if "ver" in crud.permisosUsuario["Usuarios"]:
            opcMenu = opcMenuHTML(crud.permisosUsuario)
            return render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opcionesUsuarios, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
            return redirect(url_for("inicio"))
    else:
        # No inicio sesion
        return redirect(url_for("index"))



@appDash.server.route('/buscarUsuarios', methods=('GET', 'POST'))
def buscarUsuarios():
    global listaBusquedaUsuarios, opcionesUsuarios, cabeceraUsuar
    if request.method == 'POST' and "usuario" in session:
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)

        campoBuscar = request.form['select']
        texto = request.form['text'].strip()

        if len(texto) > 0:
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            listRta = crud.consultar_usuarios()

        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarUsr'] = campoBuscar
        session['textoBuscarUsr'] = texto
        return rtaHTML

    else:
        return redirect(url_for("usuarios"))


@appDash.server.route('/ajaxUsuarioMod', methods=['POST'])
def ajaxUsuarioMod():
    global opcionesUsuarios, cabeceraUsuar
    if request.method == 'POST' and "usuario" in session:
        idUsuario = int(request.form['id'])
        
        if idUsuario == 0:
            # Crear usuario
            datosUsuario = {
                'idUsuario': 0,
                'cedula': "",
                'usuario': "",
                'nombre': "",
                'email': "",
                'direccion': "",
                'tipoUsuario': "UsuarioFinal",
                'estado': "Activo",
                'clave': "",
                'cambiarClave': 1,
            }
            usuario = crud.Usuario(datosUsuario)

        else:
            usuario = crud.consultar_usuario(idUsuario=idUsuario)
            usuario.clave = ""
        
        if usuario.tipoUsuario == "UsuarioFinal":
            usuario.tipoUsuario1 = "selected"
        elif usuario.tipoUsuario == "Administrador":
            usuario.tipoUsuario2 = "selected"
        elif usuario.tipoUsuario == "SuperAdministrador":
            usuario.tipoUsuario3 = "selected"
        #            
        if usuario.estado == "Activo":
            usuario.estado1 = "selected"
        else:
            usuario.estado2 = "selected"
        #            
        if usuario.cambiarClave == 1:
            usuario.cambiarClaveChk = "checked"
        else:
            usuario.cambiarClaveChk = ""

        rtaHTML = render_template('modUsuarios.html',infoUsuario=usuario)

        return jsonify({'htmlresponse': rtaHTML})

    else:
        return redirect(url_for("usuarios"))
 

@appDash.server.route('/ajaxUsuarioEli', methods=['POST'])
def ajaxUsuarioEli():
    global opcionesUsuarios, cabeceraUsuar
    if "usuario" in session and request.method == 'POST':
        idUsuario = int(request.form['id'])
        usuario = crud.consultar_usuario(idUsuario=idUsuario)
        rtaHTML = render_template('eliUsuarios.html',infoUsuario=usuario)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect(url_for("usuarios"))


@appDash.server.route('/modificarUsuarios', methods=['POST'])
def modificarUsuarios():
    global opcionesUsuarios, cabeceraUsuar
    if "usuario" in session and request.method == 'POST':
        idUsuarioLogin = session['idUsuario']
        usuarioLogin = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        datosUsuario = {
            'idUsuario': int(request.form['idUsuario']),
            'cedula': request.form['cedula'],
            'usuario': request.form['usuario'],
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'direccion': request.form['direccion'],
            'tipoUsuario': request.form['tipoUsuario'],
            'estado': request.form['estado'],
            'clave': request.form['clave'].strip(),
            'cambiarClave': (1 if 'cambiarClave' in request.form else 0),
            'idUsuarioCrea_id': idUsuarioLogin,
            'idUsuarioEdita_id': idUsuarioLogin,
        }
        usuario = crud.Usuario(datosUsuario)

        # Quitar la llave para que no se actualice.
        datosUsuario.pop("idUsuario")

        if len(datosUsuario['clave']) > 0:
            # Si digito una clave se encripta.
            datosUsuario['clave'] = generate_password_hash(datosUsuario['clave']).split(":")[2]
        else:
            # No digito clave se quita el campo para que no lo actualice.
            datosUsuario.pop("clave")

        datosUsuario = quitar_nones(datosUsuario)
        if usuario.idUsuario == 0:
            # Registro nuevo
            datosUsuario['aceptarPolitica'] = 0
            rta = crud.insertar_usuario(datosUsuario)
            if rta > 0:
                miFlash("Se inserto un registro")
            else:
                miFlash("Fallo la creacion del registro")
        else:
            # Quitar idUsuarioCrea_id para que no se actualice cuando el registro ya exite.
            datosUsuario.pop("idUsuarioCrea_id")
            rta = crud.actualizar_usuario(usuario.idUsuario, datosUsuario)
            if rta == 1:
                miFlash("Registro Actualizado")
            else:
                miFlash("Fallo la actualización del registro")

        # cargar datos de busqueda desde las cookies.
        if 'campoBuscarUsr' in session:
            campoBuscar = session['campoBuscarUsr']
            texto = session['textoBuscarUsr']
        else:
            campoBuscar = "usuario"
            texto = datosUsuario['usuario']

        if len(texto) > 0:
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            listRta = crud.consultar_usuarios()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuarioLogin, infoUser = (usuarioLogin+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuarioLogin, infoUser = (usuarioLogin+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("usuarios"))


@appDash.server.route('/eliminarUsuario', methods=('GET', 'POST'))
def eliminarUsuario():
    global opcionesUsuarios, cabeceraUsuar
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        idUsuario= int(request.form['idUsuario'])
        sino= request.form['sino']

        if sino == "Si":
            rta = crud.eliminar_usuario(idUsuario)
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarUsr']
        texto = session['textoBuscarUsr']

        if len(texto) > 0:
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            listRta = crud.consultar_usuarios()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuario, opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("usuarios"))


#LOGICA PROVEEDORES
@appDash.server.route('/proveedores', methods=['GET'])
def proveedores():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']        
        crud.fijar_permisosUsuario(tipoUsuario)
        if "ver" in crud.permisosUsuario["Proveedores"]:
            opcMenu = opcMenuHTML(crud.permisosUsuario)
            return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opcionesProveedores, title="Proveedores", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
            return redirect(url_for("inicio"))

    else:
        # No inicio sesion
        return redirect(url_for("index"))


@appDash.server.route('/ajaxProveedorMod', methods=['POST'])
def ajaxProveedorMod():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session and request.method == 'POST':
        idProveedor = int(request.form['id'])
        
        if idProveedor == 0:
            # Crear proveedor
            datosProveedor = {
                "idProveedor": 0,
                "nit": "",
                "nombre": "",
                "direccion": "",
                "telefono": "",
                "email": "",
                "estado": "Activo",
            }
            proveedor = crud.Proveedor(datosProveedor)
            productos = crud.consultar_productos()
            proveedor.canSelec = 0

        else:
            proveedor = crud.consultar_proveedor(idProveedor)
            
            if proveedor.estado == "Activo":
                proveedor.estado1 = "selected"
            else:
                proveedor.estado2 = "selected"
            
            #relacion productos
            productos =  crud.consultar_productos_rel(idProveedor)
            proveedor.canSelec = sum(map(lambda item : item['seleccion'] == 'checked', productos))


        rtaHTML = render_template('modProveedor.html',infoProveedor=proveedor,infoProductos=productos)

        return jsonify({'htmlresponse': rtaHTML})

    else:
        return redirect(url_for("proveedores"))


@appDash.server.route('/ajaxProveedorEli', methods=['POST'])
def ajaxProveedorEli():
    global opcionesProveedores, cabeceraProv

    if "usuario" in session and request.method == 'POST':
        idProveedor = int(request.form['id'])
        proveedor = crud.consultar_proveedor(idProveedor)
        rtaHTML = render_template('eliProveedor.html',infoProveedor=proveedor)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect(url_for("proveedores"))


@appDash.server.route('/buscarProveedores', methods=('POST','GET'))
def buscarproveedores():
    global listaBusquedaProveedores, opcionesProveedores, cabeceraProv

    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        campoBuscar = request.form['select']
        texto = request.form['text'].strip()

        if len(texto) > 0:
            listRta = crud.consultar_proveedores(campoBuscar, texto)
        else:
            listRta = crud.consultar_proveedores()
        
        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = make_response(render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario),opcMenu=opcMenu))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = make_response(render_template("Proveedores.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarProv'] = campoBuscar
        session['textoBuscarProv'] = texto

        return rtaHTML

    else:
        return redirect(url_for("proveedores"))



@appDash.server.route('/modificarProveedor', methods=('GET', 'POST'))
def modificarProveedor():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session and request.method == 'POST':
        idUsuarioLogin = session['idUsuario']
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        
        idProv = int(request.form['idProveedor'])
        crud.eliminar_rel_prov(idProv)

        prod = request.form['selectProd']

        if (len(prod) > 0 and idProv != "0"):
            productosProveedor = request.form['selectProd'].split(',')
            for idProd in productosProveedor:
                crud.insertar_relacion_proveedores(idProd,idProv)

        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        datosProveedor = {
            'idProveedor': int(request.form['idProveedor']),
            'nit': request.form['nit'],
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'telefono': request.form['telefono'],
            'email': request.form['email'],
            'estado': request.form['estado'],
            'idUsuarioCrea_id': idUsuarioLogin,
            'idUsuarioEdita_id': idUsuarioLogin,
        }
        
        ## inicia nuevo
        proveedor = crud.Proveedor(datosProveedor)
        datosProveedor.pop("idProveedor")
        
        #se toma el id de proveedor para agregar a la relacion cuando es nuevo
        maxp = crud.max_proveedor()
        if proveedor.idProveedor == 0:
            # Registro nuevo
            rta = crud.insertar_proveedor(datosProveedor)
            #inserta relacion producto - proveedor
            productosProveedor = request.form['selectProd'].split(',')
            for idProd in productosProveedor:
                crud.insertar_relacion_proveedores(idProd,maxp)
            if rta > 0:
                miFlash("Se inserto un registro")
            else:
                miFlash("Fallo la creacion del registro")
        else:
            # Quitar idUsuarioCrea_id para que no se actualice cuando el registro ya exite.
            datosProveedor.pop("idUsuarioCrea_id")
            rta = crud.actualizar_proveedor(proveedor.idProveedor, datosProveedor)
            if rta == 1:
                miFlash("Registro Actualizado")
            else:
                miFlash("Fallo la actualización del registro")

        # cargar datos de busqueda desde las cookies.
        if 'campoBuscarProv' in session:
            campoBuscar = session['campoBuscarProv']
            texto = session['textoBuscarProv']
        else:
            campoBuscar = "nombre"
            texto = datosProveedor['nombre']
        ## fin nuevo ##

        if len(texto) > 0:
            listRta = crud.consultar_proveedores(campoBuscar, texto)
        else:
            listRta = crud.consultar_proveedores()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("proveedores"))


@appDash.server.route('/eliminarProveedor', methods=('GET', 'POST'))
def eliminarProveedor():
    global opcionesProveedores, cabeceraProv
  
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        idProveedor= request.form['idProveedor']
        sino= request.form['sino']

        if sino == "Si":
            rta = crud.eliminar_Proveedor(idProveedor)
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarProv']
        texto = session['textoBuscarProv']

        if len(texto) > 0:
            listRta = crud.consultar_proveedores(campoBuscar, texto)
        else:
            listRta = crud.consultar_proveedores()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario, opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, title="Proveedores", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("proveedores"))



#LOGICA PRODUCTOS

@appDash.server.route('/productos', methods=['GET'])
def productos():
    global opcionesProductos, cabeceraProd
    if "usuario" in session:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        if "ver" in crud.permisosUsuario["Productos"]:
            opcMenu = opcMenuHTML(crud.permisosUsuario)
            return render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opcionesProductos, title="Productos", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
            return redirect(url_for("inicio"))

    else:
        return redirect(url_for("index"))


@appDash.server.route('/ajaxProductoMod', methods=['POST'])
def ajaxProductoMod():
    global opcionesProductos, cabeceraProd
    if "usuario" in session and request.method == 'POST':
        idProducto = int(request.form['id'])
        
        if idProducto == 0:
            # Crear producto
            datosProducto = {
                "idProducto": 0,
                "codigo": "",
                "nombreProducto": "",
                "cantMin": "",
                "cantDispo": "",
                "estado": "Activo",
            }

            producto = crud.Producto(datosProducto)
            proveedores = crud.consultar_proveedores()
            producto.canSelec = 0

        else:
            producto = crud.consultar_producto(idProducto)
            if producto.estado == "Activo":
                producto.estado1 = "selected"
            else:
                producto.estado2 = "selected"
        
            #relacion proveedores
            proveedores =  crud.consultar_proveedores_rel(idProducto)
            producto.canSelec = sum(map(lambda item : item['seleccion'] == 'checked', proveedores))
            
        rtaHTML = render_template('modProducto.html',infoProducto=producto,infoProveedores=proveedores)

        return jsonify({'htmlresponse': rtaHTML})

    else:
        return redirect(url_for("productos"))


@appDash.server.route('/ajaxProductoEli', methods=['POST'])
def ajaxProductoEli():
    global opcionesProductos, cabeceraProd
   
    if "usuario" in session and request.method == 'POST':
        idProducto = int(request.form['id'])
        producto = crud.consultar_producto_eli(idProducto)
        rtaHTML = render_template('eliProducto.html',infoProducto=producto)
        return jsonify({'htmlresponse': rtaHTML})

    else:
        return redirect(url_for("productos"))


@appDash.server.route('/buscarProductos', methods=('GET', 'POST'))
def buscarProductos(): #JMSS
    global listaBusquedaProductos, opcionesProductos, cabeceraProd

    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        campoBuscar = request.form['select']
        texto = request.form['text'].strip()

        if len(texto) > 0:
            listRta = crud.consultar_productos(campoBuscar, texto)
        else:
            listRta = crud.consultar_productos()
        
        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = make_response(render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario),opcMenu=opcMenu))        
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = make_response(render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarProd'] = campoBuscar
        session['textoBuscarProd'] = texto

        return rtaHTML

    else:
        return redirect(url_for("productos"))


@appDash.server.route('/modificarProducto', methods=('POST','GET'))
def modificarProducto(): #JMSS
    global opcionesProductos, cabeceraProd
   
    if "usuario" in session and request.method == 'POST':
        idUsuarioLogin = session['idUsuario']
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        idProd = request.form['idProducto']
        crud.eliminar_rel_prod(idProd)

        prov = request.form['selectProv']

        if (len(prov) > 0 and idProd != "0"):
            proveedorProductos = request.form['selectProv'].split(',')
            for idProv in proveedorProductos:
                crud.insertar_relacion_productos(idProd,idProv)
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        datosProducto = {
            'idProducto': int(request.form['idProducto']),
            'codigo' : request.form['codigo'],
            'nombreProducto': request.form['nombre'],
            'cantMin': int(request.form['cantMin']),
            'cantDispo': int(request.form['cantDispo']),
            # 'descripcion': request.form['descripcion'],
            'estado': request.form['estado'],
            'idUsuarioCrea_id': idUsuarioLogin,
            'idUsuarioEdita_id': idUsuarioLogin,
            
        }

        ## inicia nuevo
        producto = crud.Producto(datosProducto)
        datosProducto.pop("idProducto")

    	#se toma el id de proveedor para agregar a la relacion cuando es nuevo
        maxp = crud.max_producto()
        if producto.idProducto == 0:
            # Registro nuevo
            rta = crud.insertar_producto(datosProducto)
	        #inserta relacion producto - proveedor	        
            proveedorProductos = request.form['selectProv'].split(',')
            for idProv in proveedorProductos:
                crud.insertar_relacion_productos(maxp,idProv)
            if rta > 0:
                miFlash("Se inserto un registro")
            else:
                miFlash("1. Fallo la creacion del registro")
            cantDispoAnt = 0

        else:
            # Guardar datos anteriores del producto, para ventas y compras.
            datosAnt = crud.consultar_producto(producto.idProducto)
            cantDispoAnt = datosAnt.cantDispo

            # Quitar idUsuarioCrea_id para que no se actualice cuando el registro ya exite.
            datosProducto.pop("idUsuarioCrea_id")
            rta = crud.actualizar_producto(producto.idProducto, datosProducto)
            if rta == 1:
                miFlash("Registro Actualizado")
            else:
                miFlash("2. Fallo la actualización del registro")

        # Insertar la venta.
        if producto.cantDispo > cantDispoAnt:
            # Ocurrio una compra de producto.
            cantCompra = producto.cantDispo - cantDispoAnt
            costoUnidad = randint(1, 9) * 10000                # costoUnidad aleatorio.
            costoTotal = costoUnidad * cantCompra
            fecha = date(2021, randint(1, 12), randint(1, 27))  # fecha aleatoria.
            idProveedorX = crud.idProveedor_random()
            idUsuarioX = crud.idUsuario_random()
            crud.insertar_compra(producto.idProducto, idProveedorX, cantCompra, costoUnidad, costoTotal, fecha, idUsuarioX)

        elif producto.cantDispo < cantDispoAnt:
            # Ocurrio una venta de producto.
            cantVenta = cantDispoAnt - producto.cantDispo
            precioUnidad = randint(1, 9) * 10000                # precioUnidad aleatorio.
            precioTotal = precioUnidad * cantVenta
            fecha = date(2021, randint(1, 12), randint(1, 27))  # fecha aleatoria.
            idUsuarioX = crud.idUsuario_random()
            crud.insertar_venta(producto.idProducto, cantVenta, precioUnidad, precioTotal, fecha, idUsuarioX)

        # cargar datos de busqueda desde las cookies.
        if 'campoBuscarProd' in session:
            campoBuscar = session['campoBuscarProd']
            texto = session['textoBuscarProd']
        else:
            campoBuscar = "nombre"
            texto = datosProducto['nombreProducto']
        ## fin nuevo ##

        if len(texto) > 0:
            listRta = crud.consultar_productos(campoBuscar, texto)
        else:
            listRta = crud.consultar_productos()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("productos"))



@appDash.server.route('/eliminarProducto', methods=('GET', 'POST'))
def eliminarProducto(): #JMSS
    global opcionesProductos, cabeceraProd
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(crud.permisosUsuario)
        idProducto= int(request.form['idProducto'])
        sino= request.form['sino']

        if sino == "Si":
            rta = crud.eliminar_producto(idProducto)
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarProd']
        texto = session['textoBuscarProd']

        if len(texto) > 0:
            listRta = crud.consultar_productos(campoBuscar, texto)
        else:
            listRta = crud.consultar_productos()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario, opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect(url_for("productos"))


@appDash.server.route('/dashboard', methods=('GET',))
def dashboard():
    if "usuario" in session:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        crud.fijar_permisosUsuario(tipoUsuario)
        if "ver" in crud.permisosUsuario["Dashboard"]:
            opcMenu = opcMenuHTML(crud.permisosUsuario)
            dashboard_principal(tipoUsuario, usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu = opcMenu)
            return appDash.index()
        else:
            # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
            return redirect(url_for("inicio"))

    else:
        # No inicio sesion
        return redirect(url_for("index"))

