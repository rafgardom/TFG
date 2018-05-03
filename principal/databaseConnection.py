import pymongo

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
    client = pymongo.MongoClient('localhost', 27017)
    db = client['TFG']
    return db


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
api_data_find_by_questionId(id, db_connection)

** Descripcion del metodo **
Realiza la busqueda del documento dentro de la coleccion 'api_data' filtrando por el id de la pregunta

** Descripcion de parametros **
question_id: identificador de la pregunta
db_connection: conexion con la base de datos

**Return**
documento encontrado o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def api_data_find_by_questionId(question_id, db_connection):
    db = db_connection
    question = db.api_data.find_one({'question_id': question_id})
    return question


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
question_answer_find_by_questionId(id, db_connection)

** Descripcion del metodo **
Realiza la busqueda del documento dentro de la coleccion 'question_answer' filtrando por el id de la pregunta

** Descripcion de parametros **
question_id: identificador de la pregunta
db_connection: conexion con la base de datos

**Return**
documento encontrado o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def question_answer_find_by_questionId(question_id, db_connection):
    db = db_connection
    question = db.question_answer.find_one({'question_id': question_id})
    return question


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
question_answer_find_all(db_connection)

** Descripcion del metodo **
Devuelve todos los documentos de la coleccion 'question_answer'

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
documentos encontrados o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def question_answer_find_all(db_connection):
    db = db_connection
    collection = db['question_answer']
    cursor = collection.find({})
    result = []
    for document in cursor:
        result.append(document)
    return result


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
results_by_questionId(id, db_connection)

** Descripcion del metodo **
Realiza la busqueda del documento dentro de la coleccion 'results' filtrando por el id de la pregunta

** Descripcion de parametros **
question_id: identificador de la pregunta
db_connection: conexion con la base de datos

**Return**
documento encontrado o None si no encuentra ninguno
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def results_by_questionId(question_id, db_connection):
    db = db_connection
    results = db.results.find_one({'question_id': question_id})
    return results


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
find_all_api_data(db_connection)

** Descripcion del metodo **
Devuelve los documentos contenidos en la coleccion 'results' ordenados por fecha de generacion

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
lista con los documentos
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def find_all_results(db_connection):
    db = db_connection
    collection = db['results']
    cursor = collection.find({}).sort('time_now',pymongo.DESCENDING)
    result = []
    for document in cursor:
        result.append(document)
    return result

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
remove_one_result(db_connection)

** Descripcion del metodo **
Elimina un documento de la coleccion 'results'

** Descripcion de parametros **
db_connection: conexion con la base de datos
question_id: identificador de la pregunta que hace referencia al documento a eliminar

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def remove_one_result(db_connection, question_id):
    db = db_connection
    collection = db['results']
    collection.delete_one({"question_id": question_id})


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
find_all_api_data(db_connection)

** Descripcion del metodo **
Devuelve los documentos contenidos en la coleccion 'api_data'

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
lista con los documentos
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def find_all_api_data(db_connection):
    db = db_connection
    collection = db['api_data']
    cursor = collection.find({})
    result = []
    for document in cursor:
        result.append(document)
    return result

if __name__=='__main__':
    db = connection()
    #print api_data_find_by_questionId(950087, db)
    #print question_answer_find_by_questionId(950087, db)
    api_data = find_all_api_data(db)
    print api_data

