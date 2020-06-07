from flask import jsonify

def bad_request():
    return jsonify({
            'succes': False,
            'data': {},
            'messages': 'Bad request',
            'code': 400
        }), 400

#FUNCION PARA CUANDO EL CLIENTE NO ENCUENTRE RESPUESTA EN EL SERVIDOR
def not_found():
    return jsonify(
        {
            'success': False,
            'data': {},
            'message': 'Resource not found',
            'code': 404
        }
    ), 404 #codigo para el cliente

def response(data):
    return jsonify(
        {
            'succes': True,
            'data': data
        }
    ), 200


'''
DATA PUEDE SER UN OBJETO TIPO DICCIONARIO O LISTA
esta como parametro

200 indica al cliente que la respuesta es exitosa
'''