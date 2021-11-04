"""
create table usuarios
date created: 2021-10-23 01:06:45.345039
"""


def upgrade(migrator):
    with migrator.create_table('usuarios') as table:
        table.primary_key('idUsuario')
        table.text('cedula')
        table.text('usuario')
        table.text('nombre')
        table.text('direccion')
        table.text('email')
        table.text('clave')
        table.text('tipoUsuario')
        table.text('estado')
        table.text('cambiarClave')
        table.text('aceptarPolitica')


def downgrade(migrator):
    migrator.drop_table('usuarios')
