from bs4 import BeautifulSoup
import urllib2
from bs4.element import Comment

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
get_question(url)

** Descripcion del metodo **

A partir de la url de un hilo de StackOverFlow accede a los datos referentes a la pregunta formulada necesarios para el analisis de la
informacion de la pregunta.

**Descripcion de parametros**
url: direccion del hilo de StackOverFlow a analizar

**Return**
El metodo devuelve un diccionario con los datos obtenidos para su conversion a formato JSON e insercion en la base de datos
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def get_question(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page, 'html.parser')

    question_title = soup.find('a', attrs={'class': 'question-hyperlink'}).get_text()
    raw_question = soup.find('div', attrs={'class': 'question'})

    raw_question_body = raw_question.find('div', attrs={'class':'post-text'})

    question_body = get_html_text(raw_question_body)
    question_code = [c.get_text() for c in raw_question_body.find_all('code')]

    question_comments = None
    raw_comments = raw_question.find('ul', attrs={'class': 'comments-list js-comments-list'})

    if len(raw_comments.get_text()) > 1:
        question_comments = [get_html_text(qc) for qc in raw_comments.find_all('div', attrs={'class':'comment-body'})]

    return question_title, question_body, question_code, question_comments

'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
clear_html_tag(element)

** Descripcion del metodo **

Limpia cualquier tipo de dato contenido en las etiquetas 'style', 'script', 'head', 'title', 'meta', '[document]' y 
'code' que haya en una cadena de texto. 

**Descripcion de parametros**
element: componente del arbol de HTML. Por defecto vacio para que filtre cualquier elemento del arbol 

**Return**
El metodo devuelve un booleano indicando si el elemento a filtrar no contiene a etiqueta (True) o contiene la etiqueta (False)
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
'''
def clear_html_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'code']:
        return False
    if isinstance(element, Comment):
        return False
    return True


'''
/ ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
get_html_text(soup)

** Descripcion del metodo **

Extrae la informacion obtenida mediante un scraping previo en forma de cadena de texto, filtrando las etiquetas 'style', 
'script', 'head', 'title', 'meta', '[document]' y 'code'

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


get_question("https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-an-object-in-javascript")