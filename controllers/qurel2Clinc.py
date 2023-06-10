import ir_datasets

import re
dataset = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")
# for qrel in dataset.queries_iter():
# print(qrel)
# rint('/n')
from controllers.nltkController import tokenize, stopWords, stemmer, lemitizer, strip, spellChecker, convert_numbers,punctution,covid,preprocess_dates

# عمليات تنظيف الداتا
def preprocess_text(text):
    processed_text = re.sub(r"\n", "", text).split()
    processed_text = re.sub("\\n", "", text).split()
    processed_text = re.sub(" ", "", text).split()
    processed_text = ' '.join(processed_text)
    processed_text = processed_text.replace(" ", "")
    processed_text = punctution(processed_text)
    processed_text = strip(processed_text)
    return processed_text

def get_query_id(query):
    qd = -1
    query = preprocess_text(query)
    for i in dataset.queries_iter():
        query2 = preprocess_text(i.text)
        if (set(query) == set(query2)):
            qd = i.query_id
            break
    print(qd)
    return qd



def getRelevantQueries(query_id):
    qrels = get_all_qrels()
    if (query_id in qrels):
        relevants_queries = []
        for qrel in dataset.qrels_iter():
            if (qrel.query_id == query_id and qrel.relevance != 0):
                relevants_queries.append(qrel.doc_id)
        return relevants_queries


def precision(query_id, retrived_docs, num_of_retrived_doc):
    qrels = get_all_qrels()
    if (query_id in qrels):
        num_of_relvant_document = []
        relevant_queries = getRelevantQueries(query_id)
        for i in retrived_docs:
            if (i in relevant_queries):
                num_of_relvant_document.append(i)
        pr = len(num_of_relvant_document)/num_of_retrived_doc
        return pr
    return 0


def get_avp(index, doc_id, query_id, avp):
    qrels = get_all_qrels()
    if (query_id in qrels):
        relevant_queries = getRelevantQueries(query_id)
        if (doc_id in relevant_queries):
            avp += 1
            avp += avp/index
        return avp
    return 0


def recall(query_id, retrived_docs):
    qrels = get_all_qrels()
    if (query_id in qrels):
        num_of_relvant_document = []
        relevants_score = []
        relevant_queries = getRelevantQueries(query_id)
        for i in retrived_docs:
            if (i in relevant_queries):
                num_of_relvant_document.append(i)
                relevants_score.append(1)
            else:
                relevants_score.append(0)
        rec = len(num_of_relvant_document)/len(relevant_queries)
        return [rec, relevants_score]
    return [0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def calculate_map(precision_values):
    num_queries = len(precision_values)
    avg_precision = sum(precision_values) / num_queries
    map_score = avg_precision / num_queries
    return map_score


def get_all_qrels():
    qrels = set()
    for qrel in dataset.qrels_iter():
        query_id = qrel.query_id
        if query_id not in qrels:
            qrels.add(query_id)
    return qrels


'''
def get_all_queries():
    qrels = get_all_qrels()
    queries = set()
    for query in dataset.queries_iter():
        query_id = query.query_id
        if query_id not in queries:
            if (query_id in qrels):
                queries.add(query.text)
    return queries

'''


def get_all_queries():
    queries = []
    for i in dataset.queries_iter():
        queries.append(i.text)
    return queries


def Add_to_Precessions(precision, value):
    precision.append(value)
    return precision


def calculateMrr(relevance_scores):
    reciprocal_ranks = []
    for scores in relevance_scores:
        relevant_index = scores.index(1) if 1 in scores else -1
        reciprocal_rank = 1 / \
            (relevant_index + 1) if relevant_index != -1 else 0
        reciprocal_ranks.append(reciprocal_rank)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    return mrr
