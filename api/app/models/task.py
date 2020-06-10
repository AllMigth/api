from . import db

from sqlalchemy import desc, asc 
# NUESTRO MODELO
# 'BASE DE DATOS'
from sqlalchemy.event import listen
'''
a partir de la def listen seremos capaces de programar ciertas
acciones cuando ciertos eventos ocurran
en este caso queremos insertar regisgros cuando la tabla task se cree
'''

class Task(db.Model):
    # NOMBRE DE LA TABLA
    __tablename__ = 'tasks'

    # ATRIBUTOS DE LA TABLA
    # se convertiran en las columns of the table
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable=False)
    #Text almacena mas texto que un string
    deadline = db.Column(db.DateTime(), nullable=False)
    #deadline Fecha de entrega almacena fecha
    created_at = db.Column(db.DateTime(), nullable=False,
        default = db.func.current_timeStamp())
        #obtener la fecha de creacion del registro
    
    @classmethod
    def new(cls, title, description, deadline):
        return Task(title = title, description = description, deadline = deadline)
    
    #AQUI ESTAR ORDENADOR LAS PAGINAS  ascendente o descendente
    @classmethod
    def get_by_page(cls, order, page, per_page=10):  
        sort = desc(Task.id) if order == 'desc' else asc(Task.id)      #   AQUI PER_PAGE ASIGNA EL NUMERO DE DATOS POR PAGINA
        return Task.query.order_by(sort).paginate(page, per_page).items
        #page is current page
        #per_page is separete page per page...
    def save(self):
        #operacion para persistir datos
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False 

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    def __str__(self):
        return self.title

"""    def serialize(self):
        #AQUI SEERIALIZAMOS EL OBJETO JSON
        return {
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'deadline':self.deadline
        }#estos datos seran expuestos al cliente"""


#este es el callback 
# **kwargs = diccionario de argumentos

def insert_tasks(*args, **kwargs):
    #estos 3 atributos son capaces de crear una nueva tarea
    #generamos 2 objetos de tipo tarea, los agregamos a la session 
    db.session.add(
        Task(title='Title 1', description='Description',
            deadline='2020/06/22 12:00:00')
    ) 
    db.session.add(
        Task(title='Title 2', description='Description',
            deadline='2020/06/23 12:00:00')
    ) 
    db.session.commit()
    #posteriormente persistimos con db.session.commit()
   

listen(Task.__table__, 'after_create', insert_tasks)
# despues de que la tabla tasks se creee se ejecuta el callback insert task