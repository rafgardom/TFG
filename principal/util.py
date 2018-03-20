import nltk
import databaseConnection as dbc
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from nltk.text import Text

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
    tokens = nltk.word_tokenize(text)
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
    return [tokenize_text(answer["answer_body"]) for answer in answers]



'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
gensim_similarity_tf_idf(answers, question_body)

** Descripcion del metodo **
Analiza la similaridad de las respuestas respecto a la pregunta pasada como parametro

** Descripcion de parametros **
answers: lista de cuerpos de respuestas a analizar
question_body: cuerpo de la pregunta a analizar

**Return**
Lista de respuestas ordenadas segun su indice de similaridad respecto a la pregunta.
La lista es una lista de listas de respuestas con su puntuacion de similaridad: [[answer, punctuation]]
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def gensim_similarity_tf_idf(answers, question_body):
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
    query_question = tokenize_text(question_body)
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

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
gensim_similarity_tf_idf(answers, question_body)

** Descripcion del metodo **
Analiza las palabras del titulo de la pregunta y clasifica las respuestas segun el numero de apariciones que tengan las palabras
del titulo de la pregunta.
A mayor numero de aparicion tenga la palabra en el titulo de la pregunta mayor peso tiene esa palabra a la hora de calcular
la puntuacion.

** Descripcion de parametros **
question_title: titulo de la pregunta
answers: respuestas

**Return**
Lista de respuestas ordenadas segun su puntuacion de frecuencia de palabras respecto al titulo de la pregunta.
La lista es una lista de listas de respuestas con su puntuacion de frecuencia: [[answer, punctuation]]
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def nltk_title_analyze(question_title, answers):
    token_question_title = tokenize_text(question_title)
    text = Text(token_question_title)

    title_frequence_dist = nltk.FreqDist(text)
    first_title_frequence_dist = title_frequence_dist.most_common(5)
    print "Frecuencia de las palabras del titulo de la pregunta:"
    print first_title_frequence_dist
    #text.common_contexts("How")

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

    return freq_dist_puntuation_list


if __name__=='__main__':
    db = dbc.connection()
    answers = dbc.question_answer_find_by_questionId(950087, db)['answers']
    question_body = dbc.question_answer_find_by_questionId(950087, db)['question_body']
    question_title = dbc.question_answer_find_by_questionId(950087, db)['question_title']

    print gensim_similarity_tf_idf(answers, question_body)
    print nltk_title_analyze(question_title, answers)


