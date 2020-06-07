from flask import request
from flask import Blueprint
#jsonify permite serializar objetos y enviarlos usando http
from .models.task import Task

from .reponses import response
from .reponses import not_found
from .reponses import bad_request

api_v1 = Blueprint('api', __name__,url_prefix='/api/v1')
#/api/v1 ES EL PREFIJO PARA TODOS LOS ENDPOINTS

#PRIMER ENDPOINT
@api_v1.route('/tasks/', methods=['GET'])
#route.(1er argumento la ruta, parametro para definir mediante que metodo http podra ser accedido a este endpoint)
# listamos todas las tareas
def get_tasks():
    # AQUI APRENDEMOS A RESPONDER UNA PETICION DEL CLIENTE :D MEDIANTE UN JSON
    #SERIALIZANDO UN DIRECCIONARIO
    #obtener todas las tareas de la tabla
    #tasks es un diccionario
    tasks =Task.query.all() #select * from tasks;
    #all retorna una LISTA de objetos
    return response([
        task.serialize() for task in tasks
    ])

#2 ENDPOINT ES PARA MOSTRAR UNA TAREA POR ID
@api_v1.route('/tasks/<id>', methods=['GET'])
# podra retornar 1 tarea o listamos 1 tarea
def get_task(id):
    tasks = Task.query.filter_by(id=id).first()

    if tasks is None:
        return not_found()


    return response(tasks.serialize())
    #serialize es una def del task.py
    

#3 ENDPOINT
@api_v1.route('/tasks', methods=['POST'])
# sera accedido por POST
# podra crear 1 tarea
def create_task():
    json = request.get_json(force=True)         #obtener el json que envia el cliente
    #if para validar que los valores existan para crear una nueva tarea
    if json.get('title') is None or len(json['title']) > 50:
        return bad_request()
    
    if json.get('description') is None:
        return bad_request()

    if json.get('deadline') is None:
        return bad_request()

    task = Task.new(json['title'], json['description'], json['deadline']) #crear
    if task.save():
        return response(task.serialize())
    
    return bad_request()


#4 ENDPOINT
@api_v1.route('/tasks/<id>', methods=['PUT'])
# sera accedido por POST
# podra actualizar 1 tarea
def update_task(id):
    pass

#5 ENDPOINT
@api_v1.route('/tasks/<id>', methods=['DELETE'])
# sera accedido por POST
# podra eliminar 1 tarea
def delete_task():
    pass