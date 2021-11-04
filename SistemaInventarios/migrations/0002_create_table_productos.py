"""
create table productos
date created: 2021-10-23 01:06:45.354014
"""


def upgrade(migrator):
    with migrator.create_table('productos') as table:
        table.primary_key('idProducto')
        table.int('codigo', null=10)
        table.text('nombreProducto')
        table.int('cantMin')
        table.int('cantDispo', null=10)
        table.int('estado', null=1)
        table.foreign_key('AUTO', 'idUsuariCrea_id', on_delete=None, on_update=None, references='usuarios.idUsuario')
        table.foreign_key('AUTO', 'idUsuarioEdita_id', on_delete=None, on_update=None, references='usuarios.idUsuario')


def downgrade(migrator):
    migrator.drop_table('productos')
