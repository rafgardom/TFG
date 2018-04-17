import json
import databaseConnection as dbc

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_question_answer(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "question_answer"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_question_answer(document, db_connection):
    parsed = json.loads(document.read())
    collection = db_connection.question_answer
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
drop_question_answer(db_connection)

** Descripcion del metodo **
Elimina los documentos de la coleccion "question_answer"

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def drop_question_answer(db_connection):
    db_connection.question_answer.drop()


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_api_data(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "api_data"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_api_data(document, db_connection):
    parsed = json.loads(document.read())
    collection = db_connection.api_data
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
drop_api_data(db_connection)

** Descripcion del metodo **
Elimina los documentos de la coleccion "api_data"

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def drop_api_data(db_connection):
    db_connection.api_data.drop()



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_raw_api_data(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "raw_api_data"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_raw_api_data(document, db_connection):
    parsed = json.loads(document.read())
    collection = db_connection.raw_api_data
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
drop_api_data(db_connection)

** Descripcion del metodo **
Elimina los documentos de la coleccion "raw_api_data"

** Descripcion de parametros **
db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def drop_raw_api_data(db_connection):
    db_connection.raw_api_data.drop()




'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_question(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "question"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_question(document, db_connection):
    parsed = json.loads(document.read())
    collection = db_connection.question
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_answer(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "answer"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)
db_connection: conexion con la base de datos

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_answer(document, db_connection):
    parsed = json.loads(document.read())
    collection = db_connection.answer
    collection.insert(parsed)

if __name__ == '__main__':
    db_connection = dbc.connection()
    question_answer = open("question_answer.json", 'r')
    api_data = open("api_data.json", 'r')
    raw_api_data = open("raw_api_data.json", 'r')
    #question = open("question.json", 'r')
    #answer = open("answer.json", 'r')

    insert_question_answer(question_answer, db_connection)
    insert_api_data(api_data, db_connection)
    insert_raw_api_data(raw_api_data, db_connection)
    #insert_question(question, db_connection)
    #insert_answer(answer, db_connection)