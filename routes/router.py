from flask import Blueprint
from controllers.nltkController import normalization, strip, tokenize, sen_tokenizetion, word_tokenizetion, stopWords, stemmer, lemitizer
# from controllers.data_set import Evaluation
from controllers.send_search_results import search, get_map, ClincSearch, Clinc_get_map, spellCheck
blueprint = Blueprint('blueprint', __name__)

blueprint.route('/map', methods=['GET'])(get_map)
blueprint.route('/search', methods=['GET'])(search)

blueprint.route('/Clincmap', methods=['GET'])(Clinc_get_map)
blueprint.route('/Clincsearch', methods=['GET'])(ClincSearch)

blueprint.route('/spellCheck', methods=['GET'])(spellCheck)
