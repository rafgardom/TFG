# -*- coding: utf-8 -*-
import requests
import json
import ijson

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
search_advanced_filter(page, page_size, from_date, to_date, order, sort, q, accepted, answers, body, closed, notice,
                           not_tagged, tagged, title, user, url, views, wiki)

** Descripcion del metodo **

Recoge los datos de los hilos proporcionados por la llamada a la API de StackOverFlow

**Descripcion de parametros**
page: numero de paginas. Nulo por defecto
page_size: tamanio pagina. Nulo por defecto
from_date: fecha inicial para el filtro. Nulo por defecto
to_date: fecha final para el filtro. Nulo por defecto
order: orden de hilos por fecha; ascendente (asc) o descendente (desc).Por defecto es descencente (desc)
sort: orden de hilos por parametro; actividad (activity), votos (votes), creacion (creation), relevancia (relevance). Por defecto es actividad (activity)
q: texto libre que comparara lo introducido con las propiedades de la pregunta. Nulo por defecto
accepted: filtro de respuestas aceptadas. En caso que se quiera activar esta opcion: Verdadero (True) o falso (False). Nulo por defecto
answers: numero mínimo de respuestas que tiene una pregunta. Nulo por defecto
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

**Return**
El metodo la url que da habilita la llamada a la API de StackOverFlow

**Nota** por razones de rendimiento si el parametro "nottagged" esta activado se debe filtrar tambien con otro parametro distinto. De cualquier
otra forma se lanzara una excepcion que impedira la ejecucion del metodo.
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def search_advanced_filter(page = None, page_size = None, from_date = None, to_date = None, order = "desc", sort = "activity",
                           q = None, accepted = None, answers = None, body = None, closed = None, notice = None,
                           not_tagged = None, tagged = None, title = None, user = None, url = None, views = None, wiki = None):

    raw_url = "https://api.stackexchange.com/2.2/search/advanced?"
    param_cont = 0

    if page != None and isinstance(page, int):
        raw_url += "page=" + str(page)
        param_cont += 1

    if page_size != None and isinstance(page_size, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "pagesize=" + str(page_size)
        param_cont += 1

    if from_date != None and isinstance(page, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "fromdate=" + str(from_date)
        param_cont += 1

    if to_date != None and isinstance(page, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "todate=" + str(to_date)
        param_cont += 1

    if order == "desc" or order == "asc":
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "order=" + order
        param_cont += 1

    if sort == "activity" or sort == "votes" or sort == "creation" or sort == "relevance":
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "sort=" + sort
        param_cont += 1

    if q != None and isinstance(q, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "q=" + q
        param_cont += 1

    if accepted != None and (accepted == True or accepted == False):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "accepted=" + str(accepted)
        param_cont += 1

    if answers != None and isinstance(answers, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "answers=" + str(answers)
        param_cont += 1

    if body != None and isinstance(body, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "body=" + body
        param_cont += 1

    if closed != None and (closed == True or closed == False):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "closed=" + str(closed)
        param_cont += 1

    if notice != None and (notice == True or notice == False):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "notice=" + str(notice)
        param_cont += 1

    if not_tagged != None and isinstance(not_tagged, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "nottagged=" + not_tagged
        param_cont += 1

    if tagged != None and isinstance(tagged, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "tagged=" + tagged
        param_cont += 1

    if title != None and isinstance(title, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "title=" + title
        param_cont += 1

    if user != None and isinstance(user, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "user=" + str(user)
        param_cont += 1

    if url != None and isinstance(url, str):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "url=" + url
        param_cont += 1

    if views != None and isinstance(views, int):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "views=" + str(views)
        param_cont += 1

    if wiki != None and (wiki == True or wiki == False):
        raw_url = add_aux_param(param_cont, raw_url)
        raw_url += "wiki=" + str(wiki)
        param_cont += 1

    raw_url += "&site=stackoverflow"
    return raw_url

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
add_aux_param(cont, url)

** Descripcion del metodo **
Adhiere el caracter "&" a la url, necesario para crear un filtro con varios parametros valido para la llamada a la API de 
StackOverFlow.

** Descripcion de parametros **
cont: contador de parametros agregados al filtro
url: url resultante de la llamada a la API

**Return**
El metodo devuelve la url introducida adheriendo el caracter '&'
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def add_aux_param(cont, url):
    if cont > 0:
        url += "&"
    return url


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
get_threads(page, page_size, from_date, to_date, order, sort, q, accepted, answers, body, closed, notice,
                           not_tagged, tagged, title, user, url, views, wiki)

** Descripcion del metodo **
Genera el archivo en formato JSON con la informacion sin tratar extraida de la API para insertarla en la base de datos

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
Lista de diccionarios con datos interesantes que ofrece la API
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def get_threads(page = None, page_size = None, from_date = None, to_date = None, order = "desc", sort = "activity",
                           q = None, accepted = None, answers = None, body = None, closed = None, notice = None,
                           not_tagged = None, tagged = None, title = None, user = None, url = None, views = None, wiki = None):

    url = search_advanced_filter(page, page_size, from_date, to_date, order, sort, q, accepted, answers, body, closed, notice,
                           not_tagged, tagged, title, user, url, views, wiki)

    r = requests.get(url)
    parse =  r.json()
    #print parse
    with open('principal/raw_api_data.json', 'w') as outfile:
        json.dump(parse, outfile)


    #Devuelve los links de los hilos leidos del documento
    filename = "principal/raw_api_data.json"
    items_info = []
    with open(filename, 'r') as f:
        objects = ijson.items(f, 'items')
        columns = list(objects)
        for col in columns[0]:
            #items_info.append([col["link"], col["tags"], col["answer_count"], col["score"], col["title"], col["question_id"]])
            dic = {'link': col["link"], 'tags': col["tags"], 'answer_count': col["answer_count"], 'score': col["score"],
                                                'question_id': col["question_id"]}
            items_info.append(dic)

    return items_info

