from flask import request
from flask import Blueprint
#jsonify permite serializar objetos y enviarlos usando http
from .models.task import Task

from .reponses import response
from .reponses import not_found
from .reponses import bad_request

from .schemas import task_schema
from .schemas import tasks_schema
from .schemas import params_task_schema

api_v1 = Blueprint('api', __name__,url_prefix='/api/v1')
#/api/v1 ES EL PREFIJO PARA TODOS LOS ENDPOINTS
def set_task(function): # el parametro es LA FUNCION a decorar
    #El objetivo de esta funcion es evitar repetir codigo
    #que consulta la primer tarea y verfica si es None o no
    def wrap(*args, **kwargs):      #con **kwargs obtenemos el diccionario de parametros
        id = kwargs.get('id', 0)
        task = Task.query.filter_by(id=id).first()  #obtener la primer tarea

        if task is None:
            return not_found()
        
        return function(task) #retornamos la ejecucion de la funcion

    wrap.__name__ = function.__name__
    return wrap


#PRIMER ENDPOINT

@api_v1.route('/tasks/', methods=['GET'])       #DECORADOR DE FUNCION
#route.(1er argumento la ruta, parametro para definir mediante que metodo http podra ser accedido a este endpoint)
# listamos todas las tareas
def get_tasks():
    #PAGINACION
    page = int(request.args.get('page', 1)) #Dic
    order = request.args.get('order', 'desc')

    # AQUI APRENDEMOS A RESPONDER UNA PETICION DEL CLIENTE :D MEDIANTE UN JSON
    #SERIALIZANDO UN DIRECCIONARIO
    #obtener todas las tareas de la tabla
    #tasks es un diccionario
    #tasks =Task.query.all() #select * from tasks;
    #all retorna una LISTA de objetos
    #PAGINACION
    tasks = Task.get_by_page(order, page)
    return response(tasks_schema.dump(tasks))

#2 ENDPOINT ES PARA MOSTRAR UNA TAREA POR ID
@api_v1.route('/tasks/<id>', methods=['GET'])
# podra retornar 1 tarea o listamos 1 tarea
@set_task
def get_task(task):
    """
    ESTE ES EL CODIGO REPETIDO al que aplicamos refactor 
    con la funcion set_task

    tasks = Task.query.filter_by(id=id).first()
    if tasks is None:
        return not_found()"""

    #ESTO ES UNA SERIALIZACION
    return response(task_schema.dump(task))
    #serialize es una def del task.py
    

#3 ENDPOINT
@api_v1.route('/tasks', methods=['POST'])
# sera accedido por POST
# podra crear 1 tarea
def create_task():
    json = request.get_json(force=True)         #obtener el json que envia el cliente
    #VALIDAR PARAMETROS
    error = params_task_schema.validate(json)
    if error: #validate devuelve un error
        print(error)
        return bad_request()

    task = Task.new(json['title'], json['description'], json['deadline']) #crear
    if task.save():
        return response(task_schema.dump(task))
    
    return bad_request()


#4 ENDPOINT
@api_v1.route('/tasks/<id>', methods=['PUT'])
# sera accedido por POST
# podra actualizar 1 tarea
@set_task
def update_task(task):
    json = request.get_json(force=True)  #objeto json que envia el cliente
    task.title = json.get('title', task.title) # despues de la , es un valor por default
    # el valor por default es por si no se envia un dato
    task.description = json.get('description', task.description)
    task.deadline = json.get('deadline', task.deadline)

    if task.save():                               #persistir cambios
        return response(task_schema.dump(task))      

    return bad_request()

#5 ENDPOINT
@api_v1.route('/tasks/<id>', methods=['DELETE'])
# sera accedido por POST
# podra eliminar 1 tarea
@set_task
def delete_task(task):
    if task.delete():
        return response(task_schema.dump(task))
    
    return bad_request()