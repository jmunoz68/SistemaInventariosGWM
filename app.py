from flask import Flask
from SistemaInventarios.modelsDB import *
from SistemaInventarios.config import dev2
from SistemaInventarios import serverFlask

serverFlask.config.from_object(dev2)

bd.init_app(serverFlask)
