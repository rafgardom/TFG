import getAnswer, getQuestion, getThreads
import json
from time import gmtime, strftime

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
generate_question_answer_json(url, question_id)

** Descripcion del metodo **
Genera un archivo JSON que contiene la informacion de un hilo elegido, es decir, tanto la informacion de la pregunta como 
la de las respuestas.

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def generate_question_answer_json(url, question_id, path = "principal/question_answer.json"):
    question_answer_dic = getQuestion.get_question(url, question_id)
    answer_dic = getAnswer.get_answer(url, question_id)
    question_answer_dic['answers'] = answer_dic

    with open(path, 'w') as outfile:
        json.dump(question_answer_dic, outfile)



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
generate_processed_api_data_json(page, page_size, from_date, to_date, order, sort, q, accepted, answers, body, closed, notice,
                           not_tagged, tagged, title, user, url, views, wiki)

** Descripcion del metodo **
Genera el archivo en formato JSON con la informacion ya tratada de la API para insertarla en la base de datos

** Descripcion de parametros **
page: numero de paginas. Nulo por defecto
page_size: tamanio pagina. Nulo por defecto
from_date: fecha inicial para el filtro. Nulo por defecto
to_date: fecha final para el filtro. Nulo por defecto
order: orden de hilos por fecha; ascendente (asc) o descendente (desc).Por defecto es descencente (desc)
sort: orden de hilos por parametro; actividad (activity), votos (votes), creacion (creation), relevancia (relevance). Por defecto es actividad (activity)
q: texto libre que comparara lo introducido con las propiedades de la pregunta. Nulo por defecto
accepted: filtro de respuestas aceptadas. En caso que se quiera activar esta opcion: Verdadero (True) o falso (False). Nulo por defecto
answers: numero minimo de respuestas que tiene una pregunta. Nulo por defecto
body: texto que debe aparecer en el cuerpo de una pregunta. Nulo por defecto
closed: devuelve preguntas cerradas (True) o no cerradas (False). En caso de activar esta opcion: verdadero (True) o falso (False). Nulo por defecto
notice: devuelve o no preguntas con noticias publicadas. En caso de activar esta opcion: verdadero (True) o falso (False). Nulo por defecto
nottagged: etiquetas que no debe tener la pregunta. Se separan por punto y coma (;). Nulo por defecto
tagged: etiquetas que debe tener una pregunta. Se separan por punto y coma (;). Nulo por defecto
title: texto que debe aparecer en el titulo de la pregunta. Nulo por defecto
user: id del usuario propietario de la pregunta. Nulo por defecto
url: url contenida en la publicacion. puede contener un wildcar (parametro comodin). Nulo por defecto
views: numero minimo de vistas devueltas que tiene que tener una pregunta. Nulo por defecto
wiki: preguntas de la wiki de la comunidad. En caso de activar esta opcion: verdadero (True) o falso (False). Nulo por defecto

**Nota** por razones de rendimiento si el parametro "nottagged" esta activado se debe filtrar tambien con otro parametro distinto. De cualquier
otra forma se lanzara una excepcion que impedira la ejecucion del metodo.

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def generate_processed_api_data_json(page = None, page_size = None, from_date = None, to_date = None, order = "desc", sort = "activity",
                           q = None, accepted = None, answers = None, body = None, closed = None, notice = None,
                           not_tagged = None, tagged = None, title = None, user = None, url = None, views = None, wiki = None,
                                     path = "principal/api_data.json"):

    dic = getThreads.get_threads(page, page_size, from_date, to_date, order, sort, q, accepted, answers, body, closed, notice,
                           not_tagged, tagged, title, user, url, views, wiki)

    with open(path, 'w') as outfile:
        json.dump(dic, outfile)



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
generate_results_json(answers, question_id)

** Descripcion del metodo **
Genera un archivo JSON que contiene los resultados de los rankings obtenidos tras el analisis de pregunta y respuestas

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def generate_results_json(answers, gensim_similarity_tf_idf_body_result,
                                  gensim_similarity_tf_idf_code_result, nltk_title_analyze_title_result,
                                  nltk_title_analyze_code_result, merge_gensim_nltk_title, merge_gensim_nltk_code,
                                  K_means_clustering_result, question_id, path = "principal/results.json"):

    time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    result_dic = {'answers':answers, 'question_id': question_id,
                  'gensim_similarity_tf_idf_body_result':gensim_similarity_tf_idf_body_result,
                  'gensim_similarity_tf_idf_code_result':gensim_similarity_tf_idf_code_result,
                  'nltk_title_analyze_title_result':nltk_title_analyze_title_result,
                  'nltk_title_analyze_code_result':nltk_title_analyze_code_result,
                  'merge_gensim_nltk_title':merge_gensim_nltk_title,
                  'merge_gensim_nltk_code':merge_gensim_nltk_code,
                  'K_means_clustering_result':K_means_clustering_result, 'time_now':time_now}


    with open(path, 'w') as outfile:
        json.dump(result_dic, outfile)


if __name__ == '__main__':
    #generate_processed_api_data_json(answers=40)
    '''generate_question_answer_json(
        "https://stackoverflow.com/questions/950087/how-do-i-include-a-javascript-file-in-another-javascript-file",
        950087, path = "api_data.json")'''
    generate_question_answer_json(
        "https://stackoverflow.com/questions/17421104/android-studio-marks-r-in-red-with-error-message-cannot-resolve-symbol-r-but",
        17421104, path = "question_answer.json")