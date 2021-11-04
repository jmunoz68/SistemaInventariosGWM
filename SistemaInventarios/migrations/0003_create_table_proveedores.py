"""
create table proveedores
date created: 2021-10-23 01:06:45.364985
"""


def upgrade(migrator):
    with migrator.create_table('proveedores') as table:
        table.primary_key('idProveedor')
        table.int('nit')
        table.text('razonSocial')
        table.text('direccion')
        table.text('telefono')
        table.text('email')
        table.int('estado', null=1)
        table.foreign_key('AUTO', 'idUsuariCrea_id', on_delete=None, on_update=None, references='usuarios.idUsuario')
        table.foreign_key('AUTO', 'idUsuarioEdita_id', on_delete=None, on_update=None, references='usuarios.idUsuario')


def downgrade(migrator):
    migrator.drop_table('proveedores')
