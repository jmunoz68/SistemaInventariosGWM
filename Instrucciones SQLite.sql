-- CREACION DE TABLAS
drop table usuarios;
CREATE TABLE usuarios (
    idUsuario         INTEGER NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    cedula            TEXT    UNIQUE,
    usuario           TEXT    NOT NULL
                              UNIQUE,
    nombre            TEXT    NOT NULL,
    direccion         TEXT    NOT NULL,
    email             TEXT    NOT NULL
                              UNIQUE,
    clave             TEXT    NOT NULL,
    tipoUsuario       TEXT,
    estado            TEXT,
    cambiarClave      TEXT,
    aceptarPolitica   TEXT,
    idUsuarioCrea_id  INTEGER REFERENCES usuarios (idUsuario) 
                              NOT NULL,
    idUsuarioEdita_id INTEGER REFERENCES usuarios (idUsuario) 
                              NOT NULL
);

drop table productos;
CREATE TABLE productos (
    idProducto        INTEGER NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    codigo            TEXT,
    nombreProducto    TEXT    NOT NULL,
    cantMin           INTEGER NOT NULL,
    cantDispo         INTEGER,
    estado            TEXT,
    idUsuarioCrea_id  INTEGER NOT NULL,
    idUsuarioEdita_id INTEGER NOT NULL,
    FOREIGN KEY (
        idUsuarioCrea_id
    )
    REFERENCES usuarios (idUsuario),
    FOREIGN KEY (
        idUsuarioEdita_id
    )
    REFERENCES usuarios (idUsuario) 
);


drop table proveedores;
CREATE TABLE proveedores (
    idProveedor       INTEGER NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    nit               TEXT    NOT NULL,
    nombre            TEXT    NOT NULL,
    direccion         TEXT    NOT NULL,
    telefono          TEXT    NOT NULL,
    email             TEXT    NOT NULL,
    estado            TEXT,
    idUsuarioCrea_id  INTEGER NOT NULL,
    idUsuarioEdita_id INTEGER NOT NULL,
    FOREIGN KEY (
        idUsuarioCrea_id
    )
    REFERENCES usuarios (idUsuario),
    FOREIGN KEY (
        idUsuarioEdita_id
    )
    REFERENCES usuarios (idUsuario) 
);


drop table relprodprov;
CREATE TABLE relprodprov (
    id           INTEGER NOT NULL
                         PRIMARY KEY AUTOINCREMENT,
    producto_id  INTEGER NOT NULL,
    proveedor_id INTEGER NOT NULL,
    FOREIGN KEY (
        producto_id
    )
    REFERENCES productos (idProducto),
    FOREIGN KEY (
        proveedor_id
    )
    REFERENCES proveedores (idProveedor) 
);


drop table compras;
CREATE TABLE compras (
    id           INTEGER  NOT NULL
                          PRIMARY KEY AUTOINCREMENT,
    producto_id  INTEGER  NOT NULL,
    proveedor_id INTEGER  NOT NULL,
    cantCompra   INTEGER  NOT NULL,
    costoUnidad  REAL,
    costoTotal   REAL,
    fecha        DATETIME,
    usuario_id   INTEGER  REFERENCES usuarios (idUsuario),
    FOREIGN KEY (
        producto_id
    )
    REFERENCES productos (idProducto),
    FOREIGN KEY (
        proveedor_id
    )
    REFERENCES proveedores (idProveedor) 
);


drop table ventas;
CREATE TABLE ventas (
    id           INTEGER  NOT NULL
                          PRIMARY KEY AUTOINCREMENT,
    producto_id  INTEGER  NOT NULL,
    cantVenta    INTEGER  NOT NULL,
    precioUnidad REAL,
    precioTotal  REAL,
    fecha        DATETIME,
    usuario_id   INTEGER  REFERENCES usuarios (idUsuario),
    FOREIGN KEY (
        producto_id
    )
    REFERENCES productos (idProducto) 
);


drop table stock;
CREATE TABLE stock (
    id          INTEGER  NOT NULL
                         PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER  NOT NULL,
    cantMin     INTEGER  NOT NULL,
    cantDispo   INTEGER  NOT NULL,
    fecha       DATETIME,
    usuario_id  INTEGER  REFERENCES usuarios (idUsuario),
    FOREIGN KEY (
        producto_id
    )
    REFERENCES productos (idProducto) 
);


-- INSERCION DE DATOS

delete from productos; 
INSERT INTO productos (codigo,nombreProducto,cantMin,cantDispo,estado,idUsuariCrea_id,idUsuarioEdita_id)
                      VALUES 
                      ('01','Producto1',10,5,1,1,1),
                      ('02','Producto2',20,15,1,1,1),
                      ('03','Producto3',30,50,1,1,1),
                      ('04','Producto4',40,60,1,1,1);
                      

delete from proveedores; 
INSERT INTO proveedores (nit,razonSocial,direccion,telefono,email,estado,idUsuariCrea_id,idUsuarioEdita_id)
                        VALUES 
                        ('11','Proveedor11','dir11','tel11','email11@zzz.com',1,2,2),
                        ('22','Proveedor22','dir22','tel11','email22@zzz.com',1,2,2),
                        ('33','Proveedor33','dir33','tel11','email33@zzz.com',1,2,2),
                        ('44','Proveedor44','dir44','tel11','email44@zzz.com',1,2,2);


delete from relprodprov; 
INSERT INTO relprodprov (producto_id,proveedor_id)
                        VALUES (1,1),(1,2),(2,1),(2,2),(3,1);
                        
select * from usuarios;
select * from productos;
select * from proveedores;

delete from ventas; 
INSERT INTO ventas (producto_id,cantVenta,precioUnidad,precioTotal,fecha, usuario_id)
                    VALUES
                    (1,5,1000,5000,'2021-01-01',1),
                    (1,10,1000,10000,'2021-02-01',2),
                    (2,20,2000,20000,'2021-03-01',2),
                    (3,20,3000,60000,'2021-04-01',3),
                    (3,5,3000,15000,'2021-05-01',3),
                    (8,10,3000,30000,'2021-06-01',9),
                    (8,15,4000,60000,'2021-07-01',9);

delete from compras; 
INSERT INTO compras (producto_id, proveedor_id, cantCompra, costoUnidad, costoTotal, fecha, usuario_id)
                    VALUES
                    (1, 2, 5, 5000, 25000,'2021-01-15',1),
                    (1, 2, 10, 5000, 50000,'2021-02-15',1),
                    (2, 3, 10, 8000, 80000,'2021-03-15',2),
                    (3, 4, 20, 8000, 160000,'2021-04-15',3),
                    (3, 4, 30, 8000, 240000,'2021-05-15',9);

delete from stock;
INSERT INTO stock (producto_id, cantMin, cantDispo, fecha, usuario_id)
                    VALUES
                    (1, 10, 5,'2021-01-20',1),
                    (1, 10, 25,'2021-02-20',1),
                    (3, 10, 15,'2021-03-20',2),
                    (3, 10, 5,'2021-04-20',3),
                    (8, 10, 20,'2021-05-20',3),
                    (8, 10, 10,'2021-06-20',9);

select * from usuarios;
select * from productos;

select * from productos where cantDispo<cantMin;

select * from ventas;
select * from compras;
select * from stock;



select * from ventas;

-- Ventas detalladas
select ventas.id, productos.nombreProducto, usuarios.nombre as nombreUsuario, ventas.cantVenta, ventas.precioUnidad, ventas.precioTotal, ventas.fecha
    from ventas 
    join productos on ventas.producto_id = productos.idProducto
    join usuarios on ventas.usuario_id = usuarios.idUsuario
    order by ventas.fecha;

-- Ventas acumuladas
select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(ventas.cantVenta) as cantVenta, sum(ventas.precioTotal) as precioTotal, ventas.fecha
    from ventas 
    join productos on ventas.producto_id = productos.idProducto
    join usuarios on ventas.usuario_id = usuarios.idUsuario
    group by ventas.fecha
    order by ventas.fecha;

-- Compras acumuladas
select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(compras.cantCompra) as cantCompra, sum(compras.costoTotal) as costoTotal, compras.fecha
    from compras 
    join productos on compras.producto_id = productos.idProducto
    join usuarios on compras.usuario_id = usuarios.idUsuario
    group by compras.fecha
    order by compras.fecha;

select * from productos;

-- Estado de Inventario de productos
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo,
       (case 
           when productos.cantMin*1.3 < productos.cantDispo then '1.Optimo'
           when productos.cantMin*1.2 < productos.cantDispo then '2.Aceptable'
           when productos.cantMin < productos.cantDispo then '3.Alerta'
           else '4.Critico'
        end
       ) as nivel
    from productos
    order by nivel, productos.nombreProducto;



select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.3, productos.cantDispo, '1.Optimo' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.3;

select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.2, productos.cantDispo, '2.Aceptable' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.2 and productos.cantDispo < productos.cantMin*1.3;

select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, '3.Alerta' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin and productos.cantDispo < productos.cantMin*1.2;

select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, '4.Critico' as nivel
    from productos
    where productos.cantDispo < productos.cantMin;




select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.3, productos.cantDispo, '1.Optimo' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.3
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.2, productos.cantDispo, '2.Aceptable' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.2 and productos.cantDispo < productos.cantMin*1.3
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, '3.Alerta' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin and productos.cantDispo < productos.cantMin*1.2
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, '4.Critico' as nivel
    from productos
    where productos.cantDispo < productos.cantMin;


--------ESTADO DEL STOCK FINAL

select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin as cantidad, 'StockSeguridad' as nivel, 1 as orden
    from productos
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantDispo as cantidad, 'NivelStock' as nivel, 2 as orden
    from productos
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin-productos.cantDispo as cantidad, 'StockFaltante' as nivel, 3 as orden
    from productos
    where productos.cantDispo < productos.cantMin
order by nombreProducto, orden desc;

--------

-------- ESTADO DE VENTAS

select round(6/3);

select nombreProducto, nombreUsuario, ventaTotal, fecha, mm,
    (case 
     when tri=1 then 'Trimestre 1' 
     when tri=2 then 'Trimestre 2' 
     when tri=3 then 'Trimestre 3' 
     when tri=4 then 'Trimestre 4' 
    end) as trimestre
from (
    select productos.nombreProducto, usuarios.nombre as nombreUsuario, ventas.precioTotal as ventaTotal, ventas.fecha, strftime('%m', ventas.fecha) as mm,
        ROUND((CAST(strftime('%m', ventas.fecha) as decimal)-1)/3) + 1 as tri
        from ventas 
        join productos on ventas.producto_id = productos.idProducto
        join usuarios on ventas.usuario_id = usuarios.idUsuario
    ) as t
order by nombreProducto, nombreUsuario, trimestre;





select nombreProducto, nombreUsuario, ventaTotal, 
    (case 
     when tri=1 then 'Trimestre 1' 
     when tri=2 then 'Trimestre 2' 
     when tri=3 then 'Trimestre 3' 
     when tri=4 then 'Trimestre 4' 
    end) as trimestre
from (
    select productos.nombreProducto, usuarios.nombre as nombreUsuario, sum(ventas.precioTotal) as ventaTotal, 
        ROUND((CAST(strftime('%m', ventas.fecha) as decimal)-1)/3) + 1 as tri
        from ventas 
        join productos on ventas.producto_id = productos.idProducto
        join usuarios on ventas.usuario_id = usuarios.idUsuario
        group by productos.nombreProducto, usuarios.nombre, tri
    ) as t
order by nombreProducto, nombreUsuario, trimestre;

select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin as cantidad, 'StockSeguridad' as nivel, 1 as orden
    from productos
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantDispo as cantidad, 'NivelStock' as nivel, 2 as orden
    from productos
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin-productos.cantDispo as cantidad, 'StockFaltante' as nivel, 3 as orden
    from productos
    where productos.cantDispo < productos.cantMin
order by nombreProducto, orden desc

--------



select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin as cantidad, 'StockSeguridad' as nivel, 3 as orden
    from productos
    where productos.cantDispo >= productos.cantMin
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantDispo-productos.cantMin as cantidad, 'NivelStock' as nivel, 3 as orden
    from productos
    where productos.cantDispo > productos.cantMin
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantDispo, productos.cantMin-productos.cantDispo as cantidad, 'StockFaltante' as nivel, 3 as orden
    from productos
    where productos.cantDispo < productos.cantMin
order by nombreProducto, orden

    
select productos.idProducto, productos.nombreProducto, productos.cantDispo-productos.cantMin as cantidad,
       (case 
           when productos.cantMin*1.3 < productos.cantDispo then '1.Optimo'
           when productos.cantMin*1.2 < productos.cantDispo then '2.Aceptable'
           when productos.cantMin < productos.cantDispo then '3.Alerta'
           else '4.Critico'
        end
       ) as nivel
    from productos



select productos.idProducto, productos.nombreProducto, productos.cantDispo as cantidad,  '1.Optimo' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.3


select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.3, productos.cantDispo, productos.cantDispo-productos.cantMin as existencias,  '1.Optimo' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.3
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin*1.2, productos.cantDispo, productos.cantDispo-productos.cantMin as existencias,  '2.Aceptable' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin*1.2 and productos.cantDispo < productos.cantMin*1.3
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, productos.cantDispo-productos.cantMin as existencias, '3.Alerta' as nivel
    from productos
    where productos.cantDispo >= productos.cantMin and productos.cantDispo < productos.cantMin*1.2
union all
select productos.idProducto, productos.nombreProducto, productos.cantMin, productos.cantMin, productos.cantDispo, '4.Critico' as nivel
    from productos
    where productos.cantDispo < productos.cantMin;

 
select idProveedor from proveedores;

select * from compras order by fecha;

update compras set fecha='20210830' where id=5;

update compras set fecha=DATETIME('now') where id=5;
SELECT DATETIME('now');

select * from ventas order by fecha;
