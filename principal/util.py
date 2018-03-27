import nltk
import databaseConnection as dbc
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from nltk.text import Text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

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
def gensim_similarity_tf_idf(answers, question):
    if question != None:
        result = []

        token_answers_body = tokenize_answers_body(answers)
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
        print "Similaridad de las respuestas en base a la pregunta:"
        print sorted_similarity_answers

        '''Ahora devolvemos las respuestas segun su orden de aparicion'''
        for i in sorted_similarity_answers:
            result.append([answers[i[0]], i[1]])

        return result
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
            index_processed_list.append([index, i[1]])

        print "Posicion de los resultados vs puntuacion:"
        print index_processed_list
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
Agrupa los terminos de las pregunta y las respuestas en clusters identificando las palabras claves sobre lo que se
pregunta y responde

** Descripcion de parametros **
question_body: cuerpo de la pregunta
question_title: titulo de la pregunta
answers: respuestas
cluster_number: numero de clusteres a crear para clasificar las respuestas

**Return**
Lista con los terminos de los clusteres de la pregunta y las respuestas.
returned list([clustered_question_term][clustered_answer_terms])
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def K_means_clustering(question_body, question_title, answers, cluster_number):
    title = str(question_title.encode("utf-8"))
    body = str(question_body.encode("utf-8"))
    answers_document = []
    for answer in answers:
        answer_body = str(answer["answer_body"].encode("utf-8"))
        answers_document.append(answer_body)
    question_documents = [title, body]
    question_vectorizer = TfidfVectorizer(stop_words='english')
    answer_vectorizer = TfidfVectorizer(stop_words='english')
    vectoriced_question_document = question_vectorizer.fit_transform(question_documents)
    vectoriced_answers_document = answer_vectorizer.fit_transform(answers_document)

    question_model = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1)
    question_model.fit(vectoriced_question_document)

    answer_model = KMeans(n_clusters=cluster_number, init='k-means++', max_iter=100, n_init=1)
    answer_model.fit(vectoriced_answers_document)

    print("Top terms per question_clusters:")
    question_order_centroids = question_model.cluster_centers_.argsort()[:, ::-1]
    question_terms = question_vectorizer.get_feature_names()

    answer_order_centroids = answer_model.cluster_centers_.argsort()[:, ::-1]
    answer_terms = answer_vectorizer.get_feature_names()

    resulting_question_term = []
    resulting_answer_term = []

    for cluster in range(2):
        [resulting_question_term.append(question_terms[i]) for i in question_order_centroids[cluster][:5]]

    for cluster in range(cluster_number):
        [resulting_answer_term.append(answer_terms[i]) for i in answer_order_centroids[cluster][:10]]

    print "Question terms"
    print resulting_question_term
    print "Answer terms"
    print resulting_answer_term

    return [resulting_question_term, resulting_answer_term]


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
matching_clustering(K_means_clustering_result)

** Descripcion del metodo **
Compara los terminos iguales en los clusteres 

** Descripcion de parametros **
K_means_clustering_result: resultado de la ejecucion del metodo "K_means_clustering"

**Return**
Lista con los terminos que aparecen en ambos conjuntos de clusteres
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def matching_clustering(K_means_clustering_result):
    result = []
    question_cluster = K_means_clustering_result[0]
    answer_cluster = K_means_clustering_result[1]

    for i in question_cluster:
        if i in answer_cluster:
            result.append(i)

    print result
    return result


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
ranking_K_means(matching, answers)

** Descripcion del metodo **
Elabora un ranking de respuestas segun los terminos clusterizados mediante el algoritmo de K_means

** Descripcion de parametros **
matching: resultado de la ejecucion del metodo "matching_clustering"
answers: respuestas a clasificar

**Return**
Lista con las respuestas ordenadas segun su clasificacion con la puntuacion que han obtenido
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def ranking_K_means(matching, answers):
    result = []
    for answer in answers:
        answer_punctuation = 0
        for term in matching:
            if term in answer["answer_body"]:
                answer_punctuation += 1

        result.append([answer, answer_punctuation])

    result = sorted(result, key=lambda answer: answer[1], reverse=True)
    index_processed_list = []
    for i in result:
        index = answers.index(i[0])
        index_processed_list.append([index, i[1]])
    print index_processed_list
    print result[2]


if __name__=='__main__':
    db = dbc.connection()
    answers = dbc.question_answer_find_by_questionId(17421104, db)['answers']
    question_body = dbc.question_answer_find_by_questionId(17421104, db)['question_body']
    question_title = dbc.question_answer_find_by_questionId(17421104, db)['question_title']
    question_code = dbc.question_answer_find_by_questionId(17421104, db)['question_code']

    processed_question_code = question_code_processing(question_code)

    print "***Analisis por similaridad con distancia tf-idf respecto al cuerpo de la pregunta***"
    gensim_similarity_tf_idf_body_result = gensim_similarity_tf_idf(answers, question_body)
    print gensim_similarity_tf_idf_body_result
    print " "
    print "***Analisis por similaridad con distancia tf-idf respecto al codigo de la pregunta***"
    gensim_similarity_tf_idf_code_result = gensim_similarity_tf_idf(answers, processed_question_code)
    print gensim_similarity_tf_idf_code_result
    print " "
    print "***Analisis por frecuencia de aparicion de palabras del titulo de la pregunta***"
    nltk_title_analyze_title_result = nltk_title_analyze(question_title, answers)
    print nltk_title_analyze_title_result
    print " "
    print "***Analisis por frecuencia de aparicion de palabras del codigo de la pregunta***"
    nltk_title_analyze_code_result = nltk_title_analyze(processed_question_code, answers)
    print nltk_title_analyze_code_result

    print "********************************************************"
    print "Clasificacion agrupando los resultados cuerpo y titulo de la pregunta"
    print merge_results(gensim_similarity_tf_idf_body_result, nltk_title_analyze_title_result, answers)
    print " "
    print "Clasificacion agrupando los resultados de codigo de la pregunta"
    print merge_results(gensim_similarity_tf_idf_code_result, nltk_title_analyze_code_result, answers)

    '''****** K means analysis ******'''
    print "****** K means analysis ******"
    resulting = K_means_clustering(question_body, question_title, answers, 2)
    print "Matching cluster terms:"
    matching = matching_clustering(resulting)
    print "Ranking result"
    ranking_K_means(matching, answers)





