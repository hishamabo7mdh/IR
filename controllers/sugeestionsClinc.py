import ir_datasets
import json
import os


dataset = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")

filename_3 = "ClincSuggesstions.json"
if os.path.exists(filename_3):
    with open(filename_3, "r") as file:
        my_dictonery = json.load(file)
        print("File loaded successfully")
        Clincsuggesstions = my_dictonery
else:
    queries = {
        "query": {},
        "suggestions": {}
    }
    for query in dataset.queries_iter():
        query_title = query.text
        # suggestions = query.disease
        # sug = []
        titles = []
        titles.append(query_title)
        # sug.append(suggestions)
        if 'queries' not in queries:
            queries['queries'] = []
        queries['queries'].append({
            "query": query_title,
            "suggestions": titles,
        })
        '''
        queries['queries'].append({
            "query": query_title,
            "suggestions": titles,
        })

        queries['queries'].append({
            "query": suggestions,
            "suggestions": titles,
        })
        queries['queries'].append({
            "query": suggestions,
            "suggestions": sug,
        })
        '''
    with open(filename_3, "w") as file:
        json.dump(queries, file)
