from controllers.data_set import get_result, Evaluation
from controllers.data_set_2 import get_result_clinc,Evaluation_clinc
from flask import request
from spellchecker import SpellChecker

def search():
    query = request.args.get('q')
    return get_result(query)


def spellCheck():
    
    query = request.args.get('q')
    corrected_list = []
    spell = SpellChecker()
    for text in query.split():
        corrected_word = spell.correction(text)
        corrected_list.append(corrected_word) 
    
    return {"correctedText" : corrected_list}

def get_map():
    return Evaluation()


def ClincSearch():
    query = request.args.get('q')
    return get_result_clinc(query)


def Clinc_get_map():
    return Evaluation_clinc()
