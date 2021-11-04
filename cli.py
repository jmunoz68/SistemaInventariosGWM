from SistemaInventarios import serverFlask
from SistemaInventarios.app import *
from playhouse.shortcuts import model_to_dict

@serverFlask.cli.command("crear_master")
def crear_master():
    bd.init_app(serverFlask)

    #get_or_create lo crea u obtiene si existe
    #crea usuarios
    user, creado = Usuarios.get_or_create(cedula=9999, usuario='master',nombreCompleto = 'master',direccion='',email='',clave='',tipoUsuario=0,estado=1,cambiaClave=0,aceptarPolitica=0)
    print(user)
    
serverFlask.cli()
