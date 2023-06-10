import ir_datasets
import json
import os


dataset = ir_datasets.load("cord19/trec-covid/round1")

filename_3 = "CovidSuggesstions.json"
if os.path.exists(filename_3):
    with open(filename_3, "r") as file:
        my_dictonery = json.load(file)
        print("File loaded successfully")
        CovidSuggesstions = my_dictonery
else:
    queries = {
        "query": {},
        "suggestions": {}
    }
    for query in dataset.queries_iter():
        query_title = query.title
        suggestions = query.description
        sug = []
        sug.append(suggestions)
        if 'queries' not in queries:
            queries['queries'] = []
        queries['queries'].append({
            "query": query_title,
            "suggestions": sug,
        })
        queries['queries'].append({
            "query": suggestions,
            "suggestions": sug,
        })
    with open(filename_3, "w") as file:
        json.dump(queries, file)
