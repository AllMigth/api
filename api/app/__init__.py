from flask import Flask
from .models import db

#IMPORTANDO EL MODELO A CREAR
from .models.task import Task
#TASK ES EL MODELO

from . views import api_v1

#creamos instancia de flask
app = Flask(__name__)

def create_app(enviroment):
    app.config.from_object(enviroment)

    app.register_blueprint(api_v1)

    with app.app_context():
        db.init_app(app)
        #crear todas nuestras tablas modelos
        db.create_all()

    return app
