"""
create table relprodprov
date created: 2021-10-23 01:06:45.379946
"""


def upgrade(migrator):
    with migrator.create_table('relprodprov') as table:
        table.primary_key('id')
        table.foreign_key('AUTO', 'producto_id', on_delete=None, on_update=None, references='productos.idProducto')
        table.foreign_key('AUTO', 'proveedor_id', on_delete=None, on_update=None, references='proveedores.idProveedor')


def downgrade(migrator):
    migrator.drop_table('relprodprov')
