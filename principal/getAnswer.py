from bs4 import BeautifulSoup
import urllib2
from bs4.element import Comment
import json

def get_answer(url, answer_list = None, recursive = False):
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

        if len(raw_comments.get_text()) > 1:
            answer_comments = [get_html_text(ac) for ac in raw_comments.find_all('div', attrs={'class':'comment-body'})]

        answer_dict = {'answer_body':answer_body, 'answer_comments': answer_comments, 'answer_votes':answer_votes}
        answer_list.append(answer_dict)

    if next_page:
        get_answer(next_page, answer_list, recursive=True)

    return answer_list


def clear_html_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'grid']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_html_text(soup):
    text = soup.findAll(text=True)
    visible_text = filter(clear_html_tag, text)
    return u" ".join(t.strip() for t in visible_text)

def p():
    r = get_answer(
        "https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-an-object-in-javascript?page=1&tab=votes#tab-top")
    print len(r)
    with open('answer.json', 'w') as outfile:
        json.dump(r, outfile)

p()