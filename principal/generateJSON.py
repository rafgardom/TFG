import getAnswer, getQuestion
import json

def generate_question_answer_json(url):
    question_answer_dic = getQuestion.get_question(url)
    answer_dic = getAnswer.get_answer(url)
    question_answer_dic['answers'] = answer_dic

    with open('question_answer_json.json', 'w') as outfile:
        json.dump(question_answer_dic, outfile)

#generate_question_answer_json(
#    "https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-an-object-in-javascript?page=1&tab=votes#tab-top")