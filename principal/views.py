# Create your views here.
from django.shortcuts import render_to_response
import forms
from django.template import RequestContext
import time
import databaseConnection as dbc
import databaseInserts as dbi
import generateJSON as gJSON
import util as util
import generateJSON as genJSON
import models


import generateJSON as gJson

def populate(request):
    loaded_order_asc = models.Order.objects.filter(order_type="asc")
    if loaded_order_asc:
        loaded_order_asc.update(order_type="asc")
    else:
        models.Order.objects.create(order_type="asc")

    loaded_order_desc = models.Order.objects.filter(order_type="desc")
    if loaded_order_desc:
        loaded_order_desc.update(order_type="desc")
    else:
        models.Order.objects.create(order_type="desc")

    loaded_sort_activity = models.Sort.objects.filter(sort_type="activity")
    if loaded_sort_activity:
        loaded_sort_activity.update(sort_type="activity", spanish_name="actividad")
    else:
        models.Sort.objects.create(sort_type="activity", spanish_name="actividad")

    loaded_sort_votes = models.Sort.objects.filter(sort_type="votes")
    if loaded_sort_votes:
        loaded_sort_votes.update(sort_type="votes", spanish_name="votos")
    else:
        models.Sort.objects.create(sort_type="votes", spanish_name="votos")

    loaded_sort_creation = models.Sort.objects.filter(sort_type="creation")
    if loaded_sort_creation:
        loaded_sort_creation.update(sort_type="creation", spanish_name="creacion")
    else:
        models.Sort.objects.create(sort_type="creation", spanish_name="creation")

    loaded_sort_relevance = models.Sort.objects.filter(sort_type="relevance")
    if loaded_sort_relevance:
        loaded_sort_relevance.update(sort_type="relevance", spanish_name="relevancia")
    else:
        models.Sort.objects.create(sort_type="relevance", spanish_name="relevancia")

    formulario = forms.api_search_form()
    return render_to_response('home.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


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
    question = dbc.question_answer_find_by_questionId(question_id, db)
    question_link = dbc.api_data_find_by_questionId(question_id, db)['link']

    processed_question_code = util.question_code_processing(question_code)
    gensim_similarity_tf_idf_code_result = None
    nltk_title_analyze_code_result = None
    merge_gensim_nltk_code = None
    gensim_similarity_tf_idf_body_result = None
    nltk_title_analyze_title_result = None
    merge_gensim_nltk_title=None
    K_means_clustering_result=None

    #Resultados de los analisis:
    if(answers is not None):
        gensim_similarity_tf_idf_body_result = util.gensim_similarity_tf_idf(answers, question_body)

        if processed_question_code:
            gensim_similarity_tf_idf_code_result = util.gensim_similarity_tf_idf(answers, processed_question_code)

        nltk_title_analyze_title_result = util.nltk_title_analyze(question_title, answers)

        if processed_question_code:
            nltk_title_analyze_code_result = util.nltk_title_analyze(processed_question_code, answers)

        merge_gensim_nltk_title = util.merge_results(gensim_similarity_tf_idf_body_result, nltk_title_analyze_title_result, answers)

        if processed_question_code:
            merge_gensim_nltk_code = util.merge_results(gensim_similarity_tf_idf_code_result, nltk_title_analyze_code_result, answers)

        if len(question['answers']) <5 and len(question['answers'])>=2:
            K_means_clustering_result = util.K_means_clustering(question_body, question_title, answers, len(question['answers']))
        elif len(question['answers']) >= 5:
            K_means_clustering_result = util.K_means_clustering(question_body, question_title, answers,5)

    question_prepared_dic = {'question_title':question_title, 'question_body':question_body, 'question_code':question_code}

    genJSON.generate_results_json(answers, gensim_similarity_tf_idf_body_result,
                                  gensim_similarity_tf_idf_code_result, nltk_title_analyze_title_result,
                                  nltk_title_analyze_code_result, merge_gensim_nltk_title, merge_gensim_nltk_code,
                                  K_means_clustering_result, question_id, question_prepared_dic)

    results = open("principal/results.json", 'r')
    dbi.insert_results(results, db)

    return render_to_response('actual_results.html', {'answers': answers, 'gensim_similarity_tf_idf_body_result':gensim_similarity_tf_idf_body_result,
                                                      'gensim_similarity_tf_idf_code_result':gensim_similarity_tf_idf_code_result,
                                                      'nltk_title_analyze_title_result':nltk_title_analyze_title_result,
                                                      'nltk_title_analyze_code_result':nltk_title_analyze_code_result,
                                                      'merge_gensim_nltk_title':merge_gensim_nltk_title,
                                                      'merge_gensim_nltk_code':merge_gensim_nltk_code,
                                                      'K_means_clustering_result':K_means_clustering_result,
                                                      'question_id':question_id,
                                                      'question_link':question_link},
                              context_instance=RequestContext(request))


def results_list(request):
    db = dbc.connection()
    results = dbc.find_all_results(db)

    return render_to_response('results.html', {'results': results},
                              context_instance=RequestContext(request))

def view_result(request, id):
    db = dbc.connection()
    question_id = int(id)
    result = dbc.results_by_questionId(question_id, db)

    answers = result['answers']
    gensim_similarity_tf_idf_body_result = result['gensim_similarity_tf_idf_body_result']
    gensim_similarity_tf_idf_code_result = result['gensim_similarity_tf_idf_code_result']
    nltk_title_analyze_title_result = result['nltk_title_analyze_title_result']
    nltk_title_analyze_code_result = result['nltk_title_analyze_code_result']
    merge_gensim_nltk_title = result['merge_gensim_nltk_title']
    merge_gensim_nltk_code = result['merge_gensim_nltk_code']
    K_means_clustering_result = result['K_means_clustering_result']

    return render_to_response('results.html', {'old_result': True, 'answers': answers,
                                               'gensim_similarity_tf_idf_body_result':gensim_similarity_tf_idf_body_result,
                                                'gensim_similarity_tf_idf_code_result':gensim_similarity_tf_idf_code_result,
                                                'nltk_title_analyze_title_result':nltk_title_analyze_title_result,
                                                'nltk_title_analyze_code_result':nltk_title_analyze_code_result,
                                                'merge_gensim_nltk_title':merge_gensim_nltk_title,
                                                'merge_gensim_nltk_code':merge_gensim_nltk_code,
                                                'K_means_clustering_result':K_means_clustering_result,
                                                'question_id':question_id}, context_instance=RequestContext(request))

def remove_one_result(request, id):
    db = dbc.connection()
    question_id = int(id)

    dbc.remove_one_result(db, question_id)

    results = dbc.find_all_results(db)

    return render_to_response('results.html', {'results': results, 'delete_one': True},
                              context_instance=RequestContext(request))


def drop_results(request):
    db = dbc.connection()
    dbi.drop_results_data(db)

    return render_to_response('results.html', {'delete_all': True},
                              context_instance=RequestContext(request))
