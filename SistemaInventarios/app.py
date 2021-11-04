from SistemaInventarios.modelsDB import *
from SistemaInventarios.config import dev
from SistemaInventarios import serverFlask

serverFlask.config.from_object(dev)

bd.init_app(serverFlask)
