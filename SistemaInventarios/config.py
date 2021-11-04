#ambiente de desarrollo
class dev():
    DEBUG = True
    SECRET_KEY = '1234567890123456789012345678901'
    DATABASE = {
        'name' : 'SI_GWM.sqlite3',
        'engine' : 'peewee.SqliteDatabase'
    }

class dev2():
    DEBUG = True
    SECRET_KEY = '1234567890123456789012345678901'
    DATABASE = {
        'name' : 'SistemaInventarios/SI_GWM.sqlite3',
        'engine' : 'peewee.SqliteDatabase'
    }

#ambiente de produccion
class prod():
    DEBUG = False
    SECRET_KEY = 'dqwdddsadas211221'
    DATABASE = {
        'name' : 'NotiUsuario.sqlite3',
        'engine' : 'peewee.MysqlDatabase',
        'host' : 'definir',
        'user' : 'ricardo',
        'pass' : 'pass'
    }