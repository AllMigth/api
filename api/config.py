
"""
A partir de esta clase seremos capaces 
de configurar nuestra aplicacion para el entorno 
de desarroollo 
"""
class Config:
    pass

#ambiente para desarrollo
class DevelpmentConfig(Config):
    DEBUG = True
    #AGREGANDO ATRIBUTOS A LA CLASE
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/api' #esta si conecta
    #SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/api'  ASI NO CONECTA A LA DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False


#ambiente para pruebas
#aca usamos otra base de datos
class TestConfig(Config):
    DEBUG = False
    #AGREGANDO ATRIBUTOS A LA CLASE
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/api_test'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/api_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'test': TestConfig,
    'development': DevelpmentConfig
}