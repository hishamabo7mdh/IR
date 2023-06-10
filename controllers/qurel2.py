import ir_datasets
dataset = ir_datasets.load("cord19/trec-covid/round1")
# for qrel in dataset.queries_iter():
# print(qrel)
# rint('/n')


def get_query_id(query):
    qd = -1
    for i in dataset.queries_iter():
        if (i.title == query or i.description == query):
            qd = i.query_id
            break
    return qd


def getRelevantQueries(query_id):
    relevants_queries = []
    for qrel in dataset.qrels_iter():
        if (qrel.query_id == query_id and qrel.relevance != 0):
            relevants_queries.append(qrel.doc_id)
    return relevants_queries


def precision(query_id, retrived_docs, num_of_retrived_doc):
    num_of_relvant_document = []
    relevant_queries = getRelevantQueries(query_id)
    for i in retrived_docs:
        if (i in relevant_queries):
            num_of_relvant_document.append(i)
    pr = len(num_of_relvant_document)/num_of_retrived_doc
    return pr


def get_avp(index, doc_id, query_id, avp):
    relevant_queries = getRelevantQueries(query_id)
    if (doc_id in relevant_queries):
        avp += 1
        avp += avp/index
    return avp


def recall(query_id, retrived_docs):
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


def calculate_map(precision_values):
    num_queries = len(precision_values)
    avg_precision = sum(precision_values) / num_queries
    map_score = avg_precision / num_queries
    return map_score


def get_all_queries():
    queries = []
    for i in dataset.queries_iter():
        queries.append(i.description)
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
