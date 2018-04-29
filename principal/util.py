import nltk
import databaseConnection as dbc
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from nltk.text import Text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
import re
import pandas as pd
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')
stemmer = SnowballStemmer("english")

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
tokenize_text(text)

** Descripcion del metodo **
Tokeniza el texto pasado como parametro

** Descripcion de parametros **
text: texto a tokenizar

**Return**
texto tokenizado
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def tokenize_text(text):
    tokens = nltk.word_tokenize(text.encode("ascii", "ignore"))
    return tokens


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
tokenize_and_stem(text)

** Descripcion del metodo **
Tokenizador que hace uso de un stemmer para eliminar los afijos morfologicos de las palabras para dejarla en forma raiz

** Descripcion de parametros **
text: texto a tokenizar

**Return**
lista de tokens 
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def tokenize_and_stem(text):
    #Tokenizacion de la frase y la palabra eliminando los signos de puntuacion
    raw_tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    analyzed_tokens = []

    #Filtro para eliminar cualquier numero o signo de puntuacion que haya quedado
    for token in raw_tokens:
        if re.search('[a-zA-Z]', token):
            analyzed_tokens.append(token)
    result = [stemmer.stem(t) for t in analyzed_tokens]
    return result


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
tag_tokens(tokens)

** Descripcion del metodo **
Etiqueta las partes de un texto que ha sido tokenizado

** Descripcion de parametros **
tokens: texto tokenizado

**Return**
texto tokenizado ya etiquetado
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def tag_tokens(tokens):
    tagged_tokens = nltk.pos_tag(tokens)
    return tagged_tokens


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
tokenize_answers_body(answers)

** Descripcion del metodo **
Tokeniza el cuerpo de las preguntas pasadas como parametro

** Descripcion de parametros **
answers: cuerpo de las preguntas. Debe ser una lista

**Return**
Lista de preguntas tokenizadas
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def tokenize_answers_body(answers):
    return [tokenize_text(answer["answer_body"].encode("ascii", "ignore")) for answer in answers]



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
gensim_similarity_tf_idf(answers, question)

** Descripcion del metodo **
Analiza la similaridad de las respuestas respecto a la pregunta pasada como parametro

** Descripcion de parametros **
answers: lista de cuerpos de respuestas a analizar
question: parte de la pregunta a analizar

**Return**
Lista de respuestas ordenadas segun su indice de similaridad respecto a la pregunta.
La lista es una lista de listas de respuestas con su puntuacion de similaridad: [[answer, punctuation]]
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def gensim_similarity_tf_idf(answers, question, raw = True):
    if question != None:
        result = []
        token_answers_body = None

        if raw:
            token_answers_body = tokenize_answers_body(answers)
        else:
            token_answers_body = answers

        dictionary = gensim.corpora.Dictionary(token_answers_body)

        corpus = [dictionary.doc2bow(answer) for answer in token_answers_body]
        #print corpus
        tf_idf = gensim.models.TfidfModel(corpus)
        #print(tf_idf)
        sims = gensim.similarities.Similarity(None, tf_idf[corpus],
                                             num_features=len(dictionary))

        '''Tokenizamos la pregunta para comparar su distancia (tf-idf) con las respuestas ya procesadas'''
        if len(question) > 1:
            query_question = tokenize_text(question)
        else:
            query_question = question

        query_question_bow = dictionary.doc2bow(query_question)
        query_question_tf_idf = tf_idf[query_question_bow]
        similarity_list = sims[query_question_tf_idf]

        indexed_similarity_list = []
        cont = 0
        for item in similarity_list:
            indexed_similarity_list.append([cont, item])
            cont += 1

        '''Ordenamos las respuestas segun su indice de similaridad respecto a la pregunta'''
        sorted_similarity_answers = sorted(indexed_similarity_list, key=lambda answer: answer[1], reverse=True)
        #print "Similaridad de las respuestas en base a la pregunta:"
        #print sorted_similarity_answers

        '''Ahora devolvemos las respuestas segun su orden de aparicion'''
        for i in sorted_similarity_answers:
            result.append([answers[i[0]], str(i[1])])
        if raw == True:
            return result
        else:
            return sorted_similarity_answers
    else:
        print"El elemento de la pregunta que ha pasado como parametro es nulo"

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
nltk_title_analyze(question, answers)

** Descripcion del metodo **
Analiza las palabras del titulo de la pregunta y clasifica las respuestas segun el numero de apariciones que tengan las palabras
del titulo de la pregunta.
A mayor numero de aparicion tenga la palabra en el titulo de la pregunta mayor peso tiene esa palabra a la hora de calcular
la puntuacion.

** Descripcion de parametros **
question: parte de la pregunta a analizar
answers: respuestas

**Return**
Lista de respuestas ordenadas segun su puntuacion de frecuencia de palabras respecto al titulo de la pregunta.
La lista es una lista de listas de respuestas con su puntuacion de frecuencia: [[answer, punctuation]]
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def nltk_title_analyze(question, answers):
    if question != None:
        if len(question) > 1:
            token_question = tokenize_text(question)
        else:
            token_question = question

        text = Text(token_question)

        title_frequence_dist = nltk.FreqDist(text)
        first_title_frequence_dist = title_frequence_dist.most_common(20)
        #print "Frecuencia de las palabras del titulo de la pregunta:"
        #print first_title_frequence_dist

        freq_dist_puntuation_list = []

        for answer in answers:
            answer_puntuation = 0
            token_answer = tokenize_text(answer["answer_body"])
            text_token_answer = Text(token_answer)
            for tupla in first_title_frequence_dist:
                punctuation = text_token_answer.count(tupla[0]) * tupla[1]
                answer_puntuation += punctuation

            freq_dist_puntuation_list.append([answer, answer_puntuation])

        freq_dist_puntuation_list = sorted(freq_dist_puntuation_list, key=lambda answer: answer[1], reverse=True)
        index_processed_list = []
        for i in freq_dist_puntuation_list:
            index = answers.index(i[0])
            index_processed_list.append([index, str(i[1])])

        #print "Posicion de los resultados vs puntuacion:"
        #print index_processed_list
        return freq_dist_puntuation_list
    else:
        print"El elemento de la pregunta que ha pasado como parametro es nulo"


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
question_code_processing(question_code)

** Descripcion del metodo **
Procesa los caracteres irrelevantes del codigo

** Descripcion de parametros **
question_code: codigo de la pregunta

**Return**
codigo de la pregunta procesado
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def question_code_processing(question_code):
    result = None
    for i in question_code:
        result = i.replace("@", "")
        result = result.replace("$", "")
        result = result.replace("{", "")
        result = result.replace("}", "")
        result = result.replace("(", "")
        result = result.replace(")", "")
        result = result.replace(":", "")
    return result



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
merge_results(similarity_results, frequence_results, answers)

** Descripcion del metodo **
Union de resultados por puntuacion de similaridad y frecuencia

** Descripcion de parametros **
similarity_results: resultados de similaridad
frequence_results: resultados de frecuencia
answers: preguntas iniciales

**Return**
lista con la respuesta y su puntuacion global asignada
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def merge_results(similarity_results, frequence_results, answers):
    answers_resulting = []
    for answer in answers:
        global_puctuation = 0
        similarity_punctuation = 0
        frequency_puntuation = 0
        for sub_list in similarity_results:
            if sub_list[0] == answer:
                similarity_punctuation = sub_list[1]
        for sub_list in frequence_results:
            if sub_list[0] == answer:
                frequency_puntuation = sub_list[1]

        global_puctuation = similarity_punctuation * frequency_puntuation
        answers_resulting.append([answer, global_puctuation])

    answers_resulting = sorted(answers_resulting, key=lambda answer: answer[1], reverse=True)
    return answers_resulting



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
K_means_clustering(question_body, question_title, answers, cluster_number)

** Descripcion del metodo **
Agrupa las respuestas segun sus caracteristicas morfologicas y sus terminos en varios grupos consiguiendo diferenciar
varios grupos de respuestas que intentan responder a la misma pregunta.
Una vez se han clusterizado las respuestas se realiza el calculo de similaridad de cada cluster con la pregunta obteniendo
una puntuacion. Dicha puntuacion se utilizara para clasificar finalmente las respuestas.

** Descripcion de parametros **
question_body: cuerpo de la pregunta
question_title: titulo de la pregunta
answers: respuestas
cluster_number: numero de clusteres a crear para clasificar las respuestas

**Return**
Lista que contiene una lista con las respuestas clasificadas de forma global (con la puntuacion obtenida a traves de la 
clasificacion de clusteres), otra lista con las respuestas ordenadas por cluster de mayor puntuacion a menor y otra lista 
con las mejores respuestas candidatas, que se corresponden con la mejor respuesta dentro de cada cluster.
returned list([answer, punctuation], [final_result_group_by_cluster] [best_cluster_answer, punctuation])
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def K_means_clustering(question_body, question_title, answers, cluster_number):
    start_time = time.time()
    title = str(question_title.encode("utf-8"))
    body = str(question_body.encode("utf-8"))
    answers_document = []
    for answer in answers:
        answer_body = str(answer["answer_body"].encode("utf-8"))
        answers_document.append(answer_body)

    tfidf_answer_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                    min_df=0.2, stop_words='english',
                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

    vectoriced_answers_document = tfidf_answer_vectorizer.fit_transform(answers_document)


    answer_model = KMeans(n_clusters=cluster_number, init='k-means++', max_iter=100, n_init=1)
    answer_model.fit(vectoriced_answers_document)

    #print("Terminos tomados en los clusteres:")

    '''question_order_centroids = question_model.cluster_centers_.argsort()[:, ::-1]
    question_terms = tfidf_question_vectorizer.get_feature_names()'''

    answer_terms = tfidf_answer_vectorizer.get_feature_names()
    #print answer_terms


    clusters = answer_model.labels_.tolist()

    answer_data = {'answers': answers_document, 'cluster': clusters}
    frame = pd.DataFrame(answer_data, index=[clusters], columns=['answers', 'cluster'])

    #print "Clasificacion de respuestas en clusteres:"
    #print frame

    clustered_answers_dict = {}
    for i in range(cluster_number):
        clustered_answers = []
        for n in frame.ix[i].get_values():
            clustered_answers.append(n[0])
            clustered_answers_dict[i] = clustered_answers

    #print frame.ix[0].get_values()[0][0]
    #print clustered_answers_dict[4]
    clustering_punctuation = []
    #print "Calculo de similaridad de la pregunta con cada cluster"
    for i in range(cluster_number):
        clustered_processed_answers = clustered_answers_dict[i]
        answer_set = [tokenize_text(answer.decode("utf-8", "ignore")) for answer in clustered_processed_answers]

        similarity_result = gensim_similarity_tf_idf(answer_set, question_body, False)
        punctuation = 0
        for data in similarity_result:
            punctuation += data[1]
        punctuation = punctuation/len(similarity_result[0])
        clustering_punctuation.append([i, punctuation])

    final_result = []

    '''Agregando puntuaciones a las respuestas'''
    for i in range(cluster_number):
        for n in clustered_answers_dict[i]:
            for answer in answers:
                aux_answer = answer["answer_body"]
                if aux_answer == n:
                    final_result.append([answer, str(clustering_punctuation[i][1]), i])

    clustering_punctuation = sorted(clustering_punctuation, key=lambda answer: answer[1], reverse=True)
    #print clustering_punctuation
    #print final_result

    final_result_group_by_cluster = []
    for i in clustering_punctuation:
        cluster_n = i[0]
        for result in final_result:
            if result[2] == cluster_n:
                final_result_group_by_cluster.append(result)
    #print final_result_group_by_cluster

        final_result_group_by_cluster = sorted(final_result_group_by_cluster, key=lambda answer: answer[1], reverse=True)

    best_of_cluster = []
    for cluster in range(cluster_number):
        for i in final_result:
            if i[2] == cluster:
                best_of_cluster.append(i)
                break

    best_of_cluster = sorted(best_of_cluster, key=lambda answer: answer[1], reverse=True)

    end_time = time.time()
    total_time = end_time - start_time
    #print "Tiempo de ejecucion: " , total_time
    #print
    #print
    return [final_result, final_result_group_by_cluster, best_of_cluster]


if __name__=='__main__':
    db = dbc.connection()
    question_id = 49971396

    answers = dbc.question_answer_find_by_questionId(question_id, db)['answers']
    question_body = dbc.question_answer_find_by_questionId(question_id, db)['question_body']
    question_title = dbc.question_answer_find_by_questionId(question_id, db)['question_title']
    question_code = dbc.question_answer_find_by_questionId(question_id, db)['question_code']

    processed_question_code = question_code_processing(question_code)
    gensim_similarity_tf_idf_code_result = None
    nltk_title_analyze_code_result = None

    print "***Analisis por similaridad con distancia tf-idf respecto al cuerpo de la pregunta***"
    gensim_similarity_tf_idf_body_result = gensim_similarity_tf_idf(answers, question_body)
    print gensim_similarity_tf_idf_body_result
    print " "

    print "***Analisis por similaridad con distancia tf-idf respecto al codigo de la pregunta***"
    if processed_question_code:
        gensim_similarity_tf_idf_code_result = gensim_similarity_tf_idf(answers, processed_question_code)
        print gensim_similarity_tf_idf_code_result
        print " "

    print "***Analisis por frecuencia de aparicion de palabras del titulo de la pregunta***"
    nltk_title_analyze_title_result = nltk_title_analyze(question_title, answers)
    print nltk_title_analyze_title_result
    print " "
    if processed_question_code:
        print "***Analisis por frecuencia de aparicion de palabras del codigo de la pregunta***"
        nltk_title_analyze_code_result = nltk_title_analyze(processed_question_code, answers)
        print nltk_title_analyze_code_result
        print " "

    print "********************************************************"
    print "Clasificacion agrupando los resultados cuerpo y titulo de la pregunta"
    print merge_results(gensim_similarity_tf_idf_body_result, nltk_title_analyze_title_result, answers)
    print
    if processed_question_code:
        print "Clasificacion agrupando los resultados de codigo de la pregunta"
        print merge_results(gensim_similarity_tf_idf_code_result, nltk_title_analyze_code_result, answers)
        print
    '''****** K means analysis ******'''
    print "****** K means analysis ******"
    K_means_clustering_result = K_means_clustering(question_body, question_title, answers, 4)
    print "Resultado general en bruto"
    print K_means_clustering_result
    print
    print "Resultado clasificacion de respuestas de forma global (primer valor del resultado de la ejecucion de 'K_means_clustering'"
    print K_means_clustering_result[0]
    print
    print "Resultado clasificacion por clusteres (segundo valor del resultado de la ejecucion de 'K_means_clustering'"
    print K_means_clustering_result[1]
    print
    print "Resultado clasificacion de respuestas estimada (tercer valor del resultado de la ejecucion de 'K_means_clustering'"
    print K_means_clustering_result[2]





