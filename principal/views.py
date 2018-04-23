# Create your views here.
from django.shortcuts import render_to_response
import forms
from django.template import RequestContext
import time
import databaseConnection as dbc
import databaseInserts as dbi
import generateJSON as gJSON
import util as util


import generateJSON as gJson

def main_view(request):
    result_list = []
    if request.method == 'POST':
        formulario = forms.api_search_form(request.POST)
        if formulario.is_valid():
            cd = formulario.cleaned_data
            order= None
            sort = None
            page = cd['page']
            pageSize = cd['pageSize']

            if cd['order']:
                order = cd['order'].order_type

            fecha_inicio = cd['fecha_inicio']
            if fecha_inicio:
                timestamp_inicio = time.mktime(fecha_inicio.timetuple())
                fecha_inicio = str(timestamp_inicio).replace(".0", "")

            fecha_fin = cd['fecha_fin']
            if fecha_fin:
                timestamp_fin = time.mktime(fecha_fin.timetuple())
                fecha_fin = str(timestamp_fin).replace(".0", "")

            if cd['sort']:
                sort = cd['sort'].sort_type

            q = cd['q']
            answers = cd['answers']
            body = cd['body']
            tagged = cd['tagged']
            title = cd['title']

            if not order:
                order = "desc"
            if not sort:
                sort = "activity"

            #Conexion con API y generacion de archivos JSON
            db_connection = dbc.connection()
            gJson.generate_processed_api_data_json(page = page, page_size = pageSize, from_date = fecha_inicio, to_date = fecha_fin,
                           order = order, sort = sort, q = q, accepted = None, answers = answers, body = body, closed = None,
                           notice = None, not_tagged = None, tagged = tagged, title = title, user = None, url = None,
                           views = None, wiki = None)

            # Inserciones en base de datos de resultados de la busqueda usando la API
            api_data = open("principal/api_data.json", 'r')
            raw_api_data = open("principal/raw_api_data.json", 'r')

            dbi.drop_api_data(db_connection)
            dbi.drop_raw_api_data(db_connection)

            dbi.insert_api_data(api_data, db_connection)
            dbi.insert_raw_api_data(raw_api_data, db_connection)

            #Insercion en base de datos de los datos especificos de cada hilo
            api_data_documents = dbc.find_all_api_data(db_connection)
            dbi.drop_question_answer(db_connection)

            for document in api_data_documents:
                gJSON.generate_question_answer_json(document['link'], document['question_id'])
                question_answer = open("principal/question_answer.json", 'r')
                dbi.insert_question_answer(question_answer, db_connection)
                question_answer = dbc.question_answer_find_by_questionId(document['question_id'],db_connection)
                result_list.append([document, question_answer])
                '''if len(result_list) == 2:
                    break'''

    else:
        formulario = forms.api_search_form()

    return render_to_response('home.html',{'formulario':formulario, 'result_list':result_list, 'begin':0}, context_instance=RequestContext(request))

def analyze_thread(request, id):
    db = dbc.connection()
    question_id = int(id)

    answers = dbc.question_answer_find_by_questionId(question_id, db)['answers']
    question_body = dbc.question_answer_find_by_questionId(question_id, db)['question_body']
    question_title = dbc.question_answer_find_by_questionId(question_id, db)['question_title']
    question_code = dbc.question_answer_find_by_questionId(question_id, db)['question_code']

    processed_question_code = util.question_code_processing(question_code)
    gensim_similarity_tf_idf_code_result = None
    nltk_title_analyze_code_result = None

    #Resultados de los analisis:
    gensim_similarity_tf_idf_body_result = util.gensim_similarity_tf_idf(answers, question_body)

    if processed_question_code:
        gensim_similarity_tf_idf_code_result = util.gensim_similarity_tf_idf(answers, processed_question_code)

    return render_to_response('actual_results.html', {'answers': answers, 'gensim_similarity_tf_idf_body_result':gensim_similarity_tf_idf_body_result,
                                                      'gensim_similarity_tf_idf_code_result':gensim_similarity_tf_idf_code_result},
                              context_instance=RequestContext(request))
