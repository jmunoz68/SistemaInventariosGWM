from peewee import  *
from playhouse.flask_utils import FlaskDB

bd= FlaskDB()


class Usuarios(bd.Model):
    idUsuario = AutoField(primary_key=True)
    cedula = TextField()
    usuario = TextField()
    nombre = TextField()
    direccion = TextField()
    email = TextField()
    clave = TextField()
    tipoUsuario = TextField() # 0 - SuperAdministrador, 1 - Administrador, 3 - Usuario Final
    estado  = TextField()# 0 - Inactivo, 1 - Activo
    cambiarClave = IntegerField()# 0 - No, 1 - Si
    aceptarPolitica = IntegerField() # 0 - No, 1 - Si
    idUsuarioCrea = ForeignKeyField('self', backref='usu_usu_crea') #referencia inversa
    idUsuarioEdita = ForeignKeyField('self', backref='usu_usu_edita') #referencia inversa


class Productos(bd.Model):
    idProducto = AutoField(primary_key=True)
    codigo = TextField()
    nombreProducto = TextField()
    cantMin = IntegerField() # Cantidad Minina
    cantDispo = IntegerField() # Cantidad Disponible
    estado = TextField()# 0 - No, 1 - Si
    idUsuarioCrea = ForeignKeyField(Usuarios, backref='prod_usu_crea') #referencia inversa
    idUsuarioEdita = ForeignKeyField(Usuarios, backref='prod_usu_edita') #referencia inversa


class Proveedores(bd.Model):
    idProveedor = AutoField(primary_key=True)
    nit = TextField()
    nombre = TextField()
    direccion = TextField() 
    telefono = TextField() 
    email = TextField()
    estado = TextField()# 0 - No, 1 - Si
    idUsuarioCrea = ForeignKeyField(Usuarios, backref='prov_usu_crea') #referencia inversa
    idUsuarioEdita = ForeignKeyField(Usuarios, backref='prov_usu_edita') #referencia inversa


class RelProdProv(bd.Model):
    id = AutoField(primary_key=True)
    producto = ForeignKeyField(Productos, backref='prod_prov') #referencia inversa muchos a muchos
    proveedor = ForeignKeyField(Proveedores, backref='prov_prod') #referencia inversa muchos a muchos


class Compras(bd.Model):
    id = AutoField(primary_key=True)
    cantCompra =  IntegerField()
    costoUnidad =   FloatField()
    costoTotal = FloatField()
    fecha = DateTimeField()
    producto = ForeignKeyField(Productos, backref='compras_prod') #referencia inversa muchos a muchos
    proveedor = ForeignKeyField(Proveedores, backref='compras_prov') #referencia inversa muchos a muchos
    usuario = ForeignKeyField(Usuarios, backref='compras_usuario') #referencia inversa muchos a muchos


class Ventas(bd.Model):
    id = AutoField(primary_key=True)
    cantVenta =  IntegerField()
    precioUnidad =   FloatField()
    precioTotal =   FloatField()
    fecha = DateTimeField()
    producto = ForeignKeyField(Productos, backref='ventas_prod') #referencia inversa muchos a muchos
    usuario = ForeignKeyField(Usuarios, backref='ventas_usuario') #referencia inversa muchos a muchos


class Stock(bd.Model):
    id = AutoField(primary_key=True)
    cantMin =  IntegerField()
    cantDispo =  IntegerField()
    fecha = DateTimeField()
    producto = ForeignKeyField(Productos, backref='stock_prod') #referencia inversa muchos a muchos
    usuario = ForeignKeyField(Usuarios, backref='stock_usuario') #referencia inversa muchos a muchos

