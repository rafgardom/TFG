from bs4 import BeautifulSoup
import urllib2
from bs4.element import Comment
import json


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
get_answer(url, answer_list, recursive)

** Descripcion del metodo **
A partir de la url de un hilo de StackOverFlow accede a los datos referentes a las respuestas formulada, necesarias para el analisis de la
informacion.

**Descripcion de parametros**
url: direccion del hilo de StackOverFlow a analizar
question_id: identificador de la pregunta
answer_list: lista de respuestas ya recopiladas
recursive: flag que indica si es llamada recursiva

**Return**
El metodo devuelve un diccionario con los datos obtenidos para su conversion a formato JSON e insercion en la base de datos
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def get_answer(url, question_id, answer_list=None, recursive = False):
    if not recursive:
        answer_list = []

    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page, 'html.parser')

    raw_answers = soup.find('div', attrs={'id': 'answers'}).find_all('div', attrs={'class': 'answer'})

    pages = soup.find('div', attrs={'class':'pager-answers'})
    next_page = None

    if pages:
        pages = pages.find_all('a')
        if pages and ("next" in pages[-1].get_text()):
            next_page = "https://stackoverflow.com/" + pages[-1].get('href')


    for raw_answer in raw_answers:
        raw_answer_body = raw_answer.find('div', attrs={'class': 'post-text'})
        answer_comments = None
        answer_votes = raw_answer.find('span', attrs={'class':'vote-count-post'}).get_text()

        answer_body = get_html_text(raw_answer_body)
        raw_comments = raw_answer.find('ul', attrs={'class': 'comments-list js-comments-list'})

        if raw_comments:
            if len(raw_comments.get_text()) > 1:
                answer_comments = [get_html_text(ac) for ac in raw_comments.find_all('div', attrs={'class':'comment-body'})]

        answer_dict = {'answer_body':answer_body, 'answer_comments': answer_comments, 'answer_votes':answer_votes, 'question_id' : question_id}

        answer_list.append(answer_dict)

    if next_page:
        get_answer(next_page, question_id, answer_list, recursive=True)

    return answer_list


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
clear_html_tag(element)

** Descripcion del metodo **
Limpia cualquier tipo de dato contenido en las etiquetas 'style', 'script', 'head', 'title', 'meta', '[document]' y 
'grid' que haya en una cadena de texto. 

**Descripcion de parametros**
element: componente del arbol de HTML. Por defecto vacio para que filtre cualquier elemento del arbol 

**Return**
El metodo devuelve un booleano indicando si el elemento a filtrar no contiene a etiqueta (True) o contiene la etiqueta (False)
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def clear_html_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'grid']:
        return False
    if isinstance(element, Comment):
        return False
    return True


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
get_html_text(soup)

** Descripcion del metodo **
Extrae la informacion obtenida mediante un scraping previo en forma de cadena de texto, filtrando las etiquetas 'style', 
'script', 'head', 'title', 'meta', '[document]' y 'grid'

**Descripcion de parametros**
soup: variable de tipo bs4 (beautifulSoup) que se quiere convertir en cadena de texto. 

**Return**
El metodo devuelve una cadena de texto en formato unicode
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def get_html_text(soup):
    text = soup.findAll(text=True)
    visible_text = filter(clear_html_tag, text)
    return u" ".join(t.strip() for t in visible_text)


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
generate_answer_json()

** Descripcion del metodo **
Genera un archivo JSON con la informacion extraida de las respuestas

**Return**
None
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def generate_answer_json():
    r = get_answer(
        "https://stackoverflow.com/questions/950087/how-do-i-include-a-javascript-file-in-another-javascript-file", 950087)
    print len(r)
    with open('answer.json', 'w') as outfile:
        json.dump(r, outfile)


if __name__ == '__main__':
    generate_answer_json()