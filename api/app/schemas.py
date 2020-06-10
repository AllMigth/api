from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length 
#la idea es usar marshmallow sobre nuestro metodo serialize

class TaskSchema(Schema):
    class Meta:
        fields = ('id','title','description','deadline') #campos a serializar
        #fields = ('id','title','description') 

class ParamsTaskSchema(Schema): #validacion de campos
    title = fields.Str(required=True, validate=Length(max=50))
    description = fields.Str(required=True, validate=Length(max=200))
    deadline = fields.DateTime(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True) #para serializar lista usamos many

#tambien usamos .dump(aqui va la lista o el objeto)

params_task_schema = ParamsTaskSchema()