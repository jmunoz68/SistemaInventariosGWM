from logging import NullHandler
from SistemaInventarios.modelsDB import *
from playhouse.shortcuts import model_to_dict
import sqlite3
from random import randint

permisosUsuario = {}


#Validacion datos Vacios
def is_empty(data_structure):
    if data_structure:
        return True
    else:
        return False


def fijar_permisosUsuario(tipoUsuario):
    global permisosUsuario
    permisosUsuario = {}
    if tipoUsuario == "UsuarioFinal":
        permisosUsuario = {
            "Usuarios": ("",),
            "Proveedores": ("ver","cre", "mod", "eli"),
            "Productos": ("ver","cre", "mod", "eli"),
            "Dashboard": ("ver")
        }
    elif tipoUsuario == "Administrador":
        permisosUsuario = {
            "Usuarios": ("ver","cre", "mod", "eli"),
            "Proveedores": ("",),
            "Productos": ("ver"),
            "Dashboard": ("",)
        }
    elif tipoUsuario == "SuperAdministrador":
        permisosUsuario = {
            "Usuarios": ("ver","cre", "mod", "eli"),
            "Proveedores": ("ver","cre", "mod", "eli"),
            "Productos": ("ver","cre", "mod", "eli"),
            "Dashboard": ("ver")
        }


#CRUD USUARIOS

class Usuario():
    def __init__(self, datosUsuario):
      self.idUsuario = datosUsuario['idUsuario']
      self.cedula = datosUsuario['cedula']
      self.usuario = datosUsuario['usuario']
      self.nombre = datosUsuario['nombre']
      self.email = datosUsuario['email']
      self.direccion = datosUsuario['direccion']
      self.tipoUsuario = datosUsuario['tipoUsuario']
      self.estado = datosUsuario['estado']
      self.clave = datosUsuario['clave']
      self.cambiarClave = datosUsuario['cambiarClave']
      self.aceptarPolitica = (datosUsuario['aceptarPolitica'] if 'aceptarPolitica' in datosUsuario else 0)
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass

def consultar_usuarios(campoBuscar="", valor=""):
    query = []
    if len(campoBuscar) == 0:
        query = list(Usuarios.select().dicts())
    if campoBuscar == "idUsuario":
        query = list(Usuarios.select().where(Usuarios.idUsuario == valor).dicts())
    elif campoBuscar == "usuario":
        query = list(Usuarios.select().where(Usuarios.usuario == valor).dicts())
    elif campoBuscar == "nombre":
        query = list(Usuarios.select().where(Usuarios.nombre.contains(valor)).dicts())
    elif campoBuscar == "tipoUsuario":
        query = list(Usuarios.select().where(Usuarios.tipoUsuario == valor).dicts())
    elif campoBuscar == "estado":
        query = list(Usuarios.select().where(Usuarios.estado == valor).dicts())
    return query

def consultar_usuario(idUsuario=-1, usuario=""):
    
    if idUsuario != -1:
            datosUsuario = list(Usuarios.select().where(Usuarios.idUsuario == idUsuario).dicts())
            usuario = Usuario(datosUsuario[0])
    elif len(usuario) > 0:
            datosUsuario = list(Usuarios.select().where(Usuarios.usuario == usuario).dicts())
            if (is_empty(datosUsuario)):
                usuario = Usuario(datosUsuario[0])
            else:
                usuario = None
    else:
            usuario = None
        
    return usuario
    

def insertar_usuario(datosUsuario):
    datosUsuario['aceptarPolitica'] = 0
    try:
        rta = Usuarios.insert(**datosUsuario).execute()
    except:
        rta = 0
    return rta
    
def actualizar_usuario(idUsuario, datosUsuario):
    try:
        rta = Usuarios.update(**datosUsuario).where(Usuarios.idUsuario == idUsuario).execute()
    except:
        rta = 0
    return rta

def eliminar_usuario(idUsuario):
    try:
        rta = Usuarios.delete().where(Usuarios.idUsuario == idUsuario).execute()
    except:
        rta = 0
    return rta


# CRUD PROVEEDORES

class Proveedor():
    def __init__(self, datosProveedor):
      self.idProveedor = datosProveedor['idProveedor']
      self.nit = datosProveedor['nit']
      self.nombre = datosProveedor['nombre']
      self.direccion = datosProveedor['direccion']
      self.telefono = datosProveedor['telefono']
      self.email = datosProveedor['email']
      self.estado = datosProveedor['estado']
      
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass


def consultar_proveedores(campoBuscar="", valor=""):
    query = []
    if len(campoBuscar) == 0:
        query = list(Proveedores.select().dicts())
    if campoBuscar == "idProveedor":
        query = list(Proveedores.select().where(Proveedores.idProveedor == valor).dicts())
    elif campoBuscar == "nit":
        query = list(Proveedores.select().where(Proveedores.nit == valor).dicts())
    elif campoBuscar == "nombre":
        query = list(Proveedores.select().where(Proveedores.nombre.contains(valor)).dicts())
    elif campoBuscar == "direccion":
        query = list(Proveedores.select().where(Proveedores.direccion.contains(valor)).dicts())
    elif campoBuscar == "telefono":
        query = list(Proveedores.select().where(Proveedores.telefono.contains(valor)).dicts())
    elif campoBuscar == "email":
        query = list(Proveedores.select().where(Proveedores.email.contains(valor)).dicts())
    elif campoBuscar == "estado":
        query = list(Proveedores.select().where(Proveedores.estado == valor).dicts())
    return query


def consultar_proveedor(idProveedor):
    datosProveedor = list(Proveedores.select().where(Proveedores.idProveedor == idProveedor).dicts())
    proveedor = Proveedor(datosProveedor[0])
    return proveedor


def insertar_proveedor(datosProveedor):
    try:
        rta = Proveedores.insert(**datosProveedor).execute()
    except:
        rta = 0
    return rta


def actualizar_proveedor(idProveedor, datosProveedor):
    try:
        rta = Proveedores.update(**datosProveedor).where(Proveedores.idProveedor == idProveedor).execute()
    except:
        rta = 0
    return rta


def eliminar_Proveedor(idProveedor):
    try:
        rta = Proveedores.delete().where(Proveedores.idProveedor == idProveedor).execute()
    except:
        rta = 0
    return rta


#CRUD PRODUCTOS

class Producto():
    def __init__(self, datosProducto):
      self.idProducto = datosProducto['idProducto']
      self.codigo = datosProducto['codigo']
      self.nombreProducto = datosProducto['nombreProducto']
      self.cantMin = datosProducto['cantMin']
      self.cantDispo = datosProducto['cantDispo']
      self.estado = datosProducto['estado']
      
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass


def consultar_productos(campoBuscar="", valor=""):
    query = []
    if len(campoBuscar) == 0:
        query = list(Productos.select().dicts())
    if campoBuscar == "idProducto":
        query = list(Productos.select().where(Productos.idProducto == valor).dicts())
    elif campoBuscar == "codigo":
        query = list(Productos.select().where(Productos.codigo == valor).dicts())
    elif campoBuscar == "nombre":
        #query = list(Productos.select().where(Productos.nombreProducto.startswith(valor)).dicts())
        query = list(Productos.select().where(Productos.nombreProducto.contains(valor)).dicts())
    elif campoBuscar == "cantMin":
        query = list(Productos.select().where(Productos.cantMin == valor).dicts())
    elif campoBuscar == "cantDispo":
        query = list(Productos.select().where(Productos.cantDispo == valor).dicts())
    elif campoBuscar == "estado":
        query = list(Productos.select().where(Productos.estado == valor).dicts())
    return query


def consultar_producto(idProducto):
    datosProducto = list(Productos.select().where(Productos.idProducto == idProducto))
    for producto in datosProducto:
        return producto


def consultar_producto_eli(idProducto):
    datosProducto = list(Productos.select().where(Productos.idProducto == idProducto))
    
    #producto = Productos(datosProducto[0])
    for item in datosProducto:
        producto = model_to_dict(item)
    return producto


def insertar_producto(datosProducto):
    try:
        rta = Productos.insert(**datosProducto).execute()
    except:
        rta = 0
    return rta


def actualizar_producto(idProducto, datosProducto):
    try:
        rta = Productos.update(**datosProducto).where(Productos.idProducto == idProducto).execute()
    except:
        rta = 0
    return rta


def eliminar_producto(idProducto):
    try:
        rta = Productos.delete().where(Productos.idProducto == idProducto).execute()
    except:
        rta = 0
    return rta


#RELACION DE PRODUCTOS Y PROVEEDORES

def max_proveedor():
    query = Proveedores.select((fn.MAX(Proveedores.idProveedor)+1).alias('maximop'))
    max = query[0].maximop
    return max

def eliminar_rel_prov(proveedor):
    try:
        rta = RelProdProv.delete().where(RelProdProv.proveedor_id == proveedor).execute()
    except:
        rta = 0
    return rta


def insertar_relacion_proveedores(prod,prov):
    try:
        rta = RelProdProv.insert(producto_id=prod,proveedor_id=prov).execute()
    except:
        rta = 0
    return rta


#conexion directa Bd
#Retorna SQL as lista de diccionarios

def consultar_productos_rel(param):
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        con.row_factory = sqlite3.Row
        things = con.execute('select T2.idProducto,T2.codigo,T2.nombreProducto,t2.estado,"checked" AS "seleccion" from RelProdProv T1 inner join Productos T2 on T1.producto_id = T2.idProducto and T1.proveedor_id = ? union all select T3.idProducto,T3.codigo,T3.nombreProducto,t3.estado,"" as "seleccion" from Productos T3 where T3.idProducto not in (select T5.idProducto from relprodprov T4 inner join Productos T5 on T4.producto_id = T5.idProducto and T4.proveedor_id = ?)',(param,param)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        return []
    finally:
        con.close()


#RELACION PROVEEDORES PRODUCTOS

def max_producto():
    query = Productos.select((fn.MAX(Productos.idProducto)+1).alias('maximop'))
    max = query[0].maximop
    return max


def eliminar_rel_prod(producto):
    try:
        rta = RelProdProv.delete().where(RelProdProv.producto_id == producto).execute()
        
    except:
        rta = 0
    return rta


def insertar_relacion_productos(prod,prov):
    try:
        rta = RelProdProv.insert(producto_id=prod,proveedor_id=prov).execute()
        
    except:
        rta = 0
    return rta


#conexion directa Bd
#Retorna SQL as lista de diccionarios

def consultar_proveedores_rel(param):
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        con.row_factory = sqlite3.Row
        things = con.execute('select T2.idProveedor,T2.nit,T2.nombre,t2.estado,"checked" AS "seleccion" from RelProdProv T1 inner join Proveedores T2 on T1.proveedor_id = T2.idProveedor and T1.producto_id = ? union all select T3.idProveedor,T3.nit,T3.nombre,t3.estado,"" as "seleccion" from Proveedores T3 where T3.idProveedor not in (select T5.idProveedor from RelProdProv T4 inner join Proveedores T5 on T4.proveedor_id = T5.idProveedor and T4.producto_id = ?)',(param,param)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        return []
    finally:
        con.close()


def consultar_ventas_detallada():
    """
    select ventas.id, productos.nombreProducto, usuarios.nombre as nombreUsuario, ventas.cantVenta, ventas.precioUnidad, ventas.precioTotal, ventas.fecha
        from ventas 
        join productos on ventas.producto_id = productos.idProducto
        join usuarios on ventas.usuario_id = usuarios.idUsuario
        order by ventas.fecha;
    """
    #query = list(Ventas.select().where(Ventas.fecha >= fecha1 & Ventas.fecha <= fecha2).dicts())
    query = list(Ventas.select(Productos.idProducto, Productos.nombreProducto, Usuarios.nombre.alias('nombreUsuario'), 
                               Ventas.cantVenta, 
                               Ventas.precioUnidad, 
                               Ventas.precioTotal, 
                               Ventas.fecha)
                            .join(Productos, on=(Ventas.producto_id == Productos.idProducto))
                            .join(Usuarios, on=(Ventas.usuario_id == Usuarios.idUsuario))
                            .order_by(Ventas.fecha).dicts())
    return query


def consultar_ventas_agrupada():
    """
    select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(ventas.cantVenta) as cantVenta, sum(ventas.precioTotal) as precioTotal, ventas.fecha
        from ventas 
        join productos on ventas.producto_id = productos.idProducto
        join usuarios on ventas.usuario_id = usuarios.idUsuario
        group by ventas.fecha
        order by ventas.fecha;

    """
    #query = list(Ventas.select().where(Ventas.fecha >= fecha1 & Ventas.fecha <= fecha2).dicts())
    query = list(Ventas.select(Productos.nombreProducto, Usuarios.nombre.alias('nombreUsuario'), 
                               fn.SUM(Ventas.cantVenta).alias('cantVenta'), 
                               fn.SUM(Ventas.precioTotal).alias('precioTotal'), 
                               Ventas.fecha)
                            .join(Productos, on=(Ventas.producto_id == Productos.idProducto))
                            .join(Usuarios, on=(Ventas.usuario_id == Usuarios.idUsuario))
                            .group_by(Ventas.fecha)
                            .order_by(Ventas.fecha).dicts())
    return query


def consultar_compras_agrupada():
    """
    select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(compras.cantCompra) as cantCompra, sum(compras.costoTotal) as costoTotal, compras.fecha
        from compras 
        join productos on compras.producto_id = productos.idProducto
        join usuarios on compras.usuario_id = usuarios.idUsuario
        group by compras.fecha
        order by compras.fecha;

    """
    query = list(Compras.select(Productos.nombreProducto, Usuarios.nombre.alias('nombreUsuario'), 
                               fn.SUM(Compras.cantCompra).alias('cantCompra'), 
                               fn.SUM(Compras.costoTotal).alias('costoTotal'), 
                               Compras.fecha)
                            .join(Productos, on=(Compras.producto_id == Productos.idProducto))
                            .join(Usuarios, on=(Compras.usuario_id == Usuarios.idUsuario))
                            .group_by(Compras.fecha)
                            .order_by(Compras.fecha).dicts())
    return query



def insertar_venta(producto_id, cantVenta, precioUnidad, precioTotal, fecha, usuario_id):
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        con.execute("INSERT INTO ventas (producto_id, cantVenta, precioUnidad, precioTotal, fecha, usuario_id) \
                    VALUES (?,?,?,?,?,?)",(producto_id, cantVenta, precioUnidad, precioTotal, fecha, usuario_id))
        con.commit()
        return 1
    except Exception as e:
        return 0
    finally:
        con.close()


def insertar_compra(producto_id, proveedor_id, cantCompra, costoUnidad, costoTotal, fecha, usuario_id):
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        con.execute("INSERT INTO compras (producto_id, proveedor_id, cantCompra, costoUnidad, costoTotal, fecha, usuario_id) \
                    VALUES (?,?,?,?,?,?,?)",(producto_id, proveedor_id, cantCompra, costoUnidad, costoTotal, fecha, usuario_id))
        con.commit()
        return 1
    except Exception as e:
        return 0
    finally:
        con.close()


def idProveedor_random():
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        rta = list(con.execute("select idProveedor from proveedores;"))
        x = randint(1, len(rta)-1)
        rta = rta[x][0]
        return rta
    except Exception as e:
        return None
    finally:
        con.close()


def idUsuario_random():
    try:
        con = sqlite3.connect('SistemaInventarios/SI_GWM.sqlite3')
        rta = list(con.execute("select idUsuario from usuarios;"))
        x = randint(1, len(rta)-1)
        rta = rta[x][0]
        return rta
    except Exception as e:
        return None
    finally:
        con.close()


def dict_consulta(baseDB, query, params=None):
    try:
        con = sqlite3.connect(baseDB)
        con.row_factory = sqlite3.Row
        if params == None:
            things = con.execute(query).fetchall()
        else:
            things = con.execute(query,params).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        return []
    finally:
        con.close()


def consultar_nivelStock():
    rta = dict_consulta("SistemaInventarios/SI_GWM.sqlite3", 
            "select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin as cantidad, 'StockSeguridad' as nivel, 1 as orden \
                from productos \
            union all \
            select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantDispo as cantidad, 'NivelStock' as nivel, 2 as orden \
                from productos \
            union all \
            select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin-productos.cantDispo as cantidad, 'StockFaltante' as nivel, 3 as orden \
                from productos \
                where productos.cantDispo < productos.cantMin \
            order by nombreProducto, orden desc \
            ")
    return rta


def consultar_estadoVentas():
    rta = dict_consulta("SistemaInventarios/SI_GWM.sqlite3", 
            "select nombreProducto, nombreUsuario, ventaTotal, \
                (case \
                when tri=1 then 'Trimestre1' \
                when tri=2 then 'Trimestre2' \
                when tri=3 then 'Trimestre3' \
                when tri=4 then 'Trimestre4' \
                end) as trimestre \
            from ( \
                select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(ventas.precioTotal) as ventaTotal,  \
                    ROUND((CAST(strftime('%m', ventas.fecha) as decimal)-1)/3) + 1 as tri \
                    from ventas \
                    join productos on ventas.producto_id = productos.idProducto \
                    join usuarios on ventas.usuario_id = usuarios.idUsuario \
                    group by productos.nombreProducto, usuarios.nombre, tri \
                ) as t \
            order by nombreProducto, nombreUsuario, trimestre; \
            ")
    return rta
