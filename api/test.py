import json
import unittest

from app import db
from app import create_app

from config import config 

class TestAPI(unittest.TestCase):
    def setUp(self):
        enviroment = config['test']             #obtenemos el entorno de prueba
        self.app = create_app(enviroment)       #obtenemos la aplicacion
        self.client = self.app.test_client()    #generamos el cliente

        self.content_type = 'application/json' #indicamos el tipo de respuesta y dato que enviamos
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'

    def tearDown(self): 
        with self.app.app_context():
            db.drop_all()                       #eliminamos las tablas

    def test_one_equals_one(self):
        self.assertEqual(1, 1)                  #esto confirma que las 2 defs de arriba estan ok

    def test_get_all_tasks(self):
        response = self.client.get(path = self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_first_task(self):
        new_path = self.path + '/1'

        response = self.client.get(path=new_path, contet_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8')) #poseera la respuesta por parte del servidor
        task_id = data['data']['id']

        self.assertEqual(task_id, 1)

    def test_not_found(self):
        new_path = self.path + '/100'
        response = self.client.get(path=new_path, contet_type=self.content_type)
    
        self.assertEqual(response.status_code, 404)

    def test_create_tasks(self):
        data = {
            'title':'title', 'description':'description',
            'deadline': '2020-12-12 12:00:00'
        }

        response = self.client.post(path=self.path, data=json.dumps(data),
        content_type = self.content_type)
        self.assertEqual(response.status_code, 200)
        #convertir tarea a json
        data = json.loads(response.data.decode('utf-8'))
        task_id = data['data'] ['id']
        
        self.assertEqual(task_id, 3)

if __name__ == '__main__':
    unittest.main()
