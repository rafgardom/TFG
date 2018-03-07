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
insert_question_answer(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "question_answer"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_question_answer(document):
    db = connection()
    parsed = json.loads(document.read())
    collection = db.question_answer
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_api_data(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "api_data"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_api_data(document):
    db = connection()
    parsed = json.loads(document.read())
    collection = db.api_data
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_raw_api_data(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "raw_api_data"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_raw_api_data(document):
    db = connection()
    parsed = json.loads(document.read())
    collection = db.raw_api_data
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_question(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "question"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_question(document):
    db = connection()
    parsed = json.loads(document.read())
    collection = db.question
    collection.insert(parsed)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
insert_answer(document)

** Descripcion del metodo **
Inserta documentos en la coleccion "answer"

** Descripcion de parametros **
document: documento a insertar (en formato JSON)

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def insert_answer(document):
    db = connection()
    parsed = json.loads(document.read())
    collection = db.answer
    collection.insert(parsed)


if __name__ == '__main__':
    question_answer = open("question_answer.json", 'r')
    api_data = open("api_data.json", 'r')
    raw_api_data = open("raw_api_data.json", 'r')
    question = open("question.json", 'r')
    answer = open("answer.json", 'r')

    insert_question_answer(question_answer)
    insert_api_data(api_data)
    insert_raw_api_data(raw_api_data)
    insert_question(question)
    insert_answer(answer)
