from pymongo import MongoClient
import json

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
connection()

** Descripcion del metodo **
Crea la conexion con la base de datos

**Return**
conexion
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def connection():
    client = MongoClient('localhost', 27017)
    db = client['TFG']
    return db


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
api_data_find_by_questionId(id, db_connection)

** Descripcion del metodo **
Realiza la busqueda del documento dentro de la coleccion 'api_data' filtrando por el id de la pregunta

** Descripcion de parametros **
id: identificador de la pregunta
db_connection: conexion con la base de datos

**Return**
documento encontrado o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def api_data_find_by_questionId(id, db_connection):
    db = db_connection
    question = db.api_data.find_one({'question_id': id})
    return question


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
question_answer_find_by_questionId(id, db_connection)

** Descripcion del metodo **
Realiza la busqueda del documento dentro de la coleccion 'question_answer' filtrando por el id de la pregunta

** Descripcion de parametros **
id: identificador de la pregunta
db_connection: conexion con la base de datos

**Return**
documento encontrado o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def question_answer_find_by_questionId(id, db_connection):
    db = db_connection
    question = db.question_answer.find_one({'question_id': id})
    return question

if __name__=='__main__':
    db = connection()
    print api_data_find_by_questionId(950087, db)
    print question_answer_find_by_questionId(950087, db)