from controllers.nltkController import tokenize, stopWords, stemmer, lemitizer, strip, spellChecker, convert_numbers,punctution,covid,preprocess_dates
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import ir_datasets
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from controllers.qurel2Clinc import precision , get_query_id ,recall,get_all_queries,calculate_map,get_avp,calculateMrr
# عمليات تنظيف الداتا
def preprocess_text(text):
    text = strip(text)
    text = preprocess_dates(text)
    text =punctution(text)
    data_list = tokenize(text)
    data_list_stop = stopWords(data_list)
    data_list_limitzed = lemitizer(data_list_stop)
    data_list_stemmed = stemmer(data_list_limitzed)

    
    processed_text = data_list_stemmed
    
    return ' '.join(processed_text)

# تحميل الداتا سيت
dataset = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")

# انشاء متول يحمل اسم الملف
filename = "dictoneryClinc2021.json"
# في حال كان الملف موجودا قم بتحميله 
if os.path.exists(filename):
    with open(filename, "r") as file:
        my_dictonery = json.load(file)
        print("File loaded successfully")
        preprocessed_docs = my_dictonery
else:
    preprocessed_docs = {doc.doc_id:preprocess_text(doc.detailed_description)
                         for doc in dataset.docs_iter()}
    with open(filename, "w") as file:
        json.dump(preprocessed_docs, file)


# انشاء متول يحمل اسم الملف
filename_2 = "dictoneryTitleClinc2021.json"
# في حال كان الملف موجودا قم بتحميله 
if os.path.exists(filename_2):
    with open(filename_2, "r") as file:
        my_dictonery = json.load(file)
        print("File loaded successfully")
        preprocessed_title = my_dictonery
else:
    preprocessed_title = {doc.doc_id:preprocess_text(doc.title)
                         for doc in dataset.docs_iter()}
    with open(filename_2, "w") as file:
        json.dump(preprocessed_title, file)        


# Retrieve document IDs
doc_ids = list(preprocessed_docs.keys())

def calculate_tfIdf(document):
    documents = document.values()     
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents).astype('float32')
    tfidf_matrix = csr_matrix(tfidf_matrix)
    return [tfidf_matrix,vectorizer]

def retrive_simlerity(query,tfidf_matrix,vectorizer):   

    # query 
    processed_query = preprocess_text(query)

    query_vector = vectorizer.transform([processed_query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

    return cosine_similarities





filename_3 = "invertedIndexClinc2021.json"
if os.path.exists(filename_3):
    with open(filename_3, "r") as file:
        my_dictonery = json.load(file)
        print("File loaded successfully")
        inverted_index = my_dictonery
else:
 inverted_index = {
    "title": {},
    "description": {}
}
 for doc in dataset.docs_iter():
    doc_id = doc.doc_id
    title = doc.title
    description = doc.detailed_description

    inverted_index[doc_id] = {
        "title": title,
        "description": description
    }
 with open(filename_3, "w") as file:
        json.dump(inverted_index, file)

key = True
if(key is True):
  tfidf_docs = calculate_tfIdf(preprocessed_docs)[0]
  tfidf_titles = calculate_tfIdf(preprocessed_title)[0]
  vectorizer_docs = calculate_tfIdf(preprocessed_docs)[1]
  vectorizer_titles = calculate_tfIdf(preprocessed_title)[1]
  key = False


def get_result_clinc(query):
      cosine_similarities_text =retrive_simlerity(query,tfidf_docs,vectorizer_docs)
      cosine_similarities_title =retrive_simlerity(query,tfidf_titles,vectorizer_titles)
      alpha = 0.9  # Weight for the text similarity
      beta = 0.1  # Weight for the title similarity
      cosine_similarities_combined = alpha * cosine_similarities_text + beta * cosine_similarities_title
      most_similar_indices = cosine_similarities_combined.argsort()[0][::-1]
      avp = 0
      # Print the top 10 most similar documents
      retrived_docs =[]
      documents = []
      qd = get_query_id(query)
      print(qd)
      for i in range(10):
          doc_id = list(preprocessed_docs.keys())[most_similar_indices[i]]
          doc_data = inverted_index[doc_id]
          title = doc_data["title"]
          description = doc_data["description"]
          document = {
              "doc_id": doc_id,
              "title": title,
              "description": description
          }
          documents.append(document)
          print(f"Document ID: {doc_id}, Similarity Score: {cosine_similarities_combined[0][most_similar_indices[i]]}")
          #print(f"document title : {title}")
          retrived_docs.append(doc_id)
          avp = get_avp(i+1,doc_id,qd,avp)
      avp /=10
      print(f"avp is {avp}")
      if(qd != -1):
          pr = precision(qd,retrived_docs,10)
          rec = recall(qd,retrived_docs)
          print(f"from 10 queries we found {pr*10} are relevats")
          print(pr)
          print(rec[0])
          return {"precission": pr, "recall": rec[0],
            "Avp": avp,
            "documents": documents,}
      return {"documents": documents,}





def get_result_avp(query):
      cosine_similarities_text =retrive_simlerity(query,tfidf_docs,vectorizer_docs)
      cosine_similarities_title =retrive_simlerity(query,tfidf_titles,vectorizer_titles)
      alpha = 0.9  # Weight for the text similarity
      beta = 0.1  # Weight for the title similarity
      cosine_similarities_combined = alpha * cosine_similarities_text + beta * cosine_similarities_title
      most_similar_indices = cosine_similarities_combined.argsort()[0][::-1]
      # Print the top 10 most similar documents
      retrived_docs =[]
      avp = 0 
      qd = get_query_id(query)
      print(qd)
      if(qd != -1):
         for i in range(10):
            doc_id = list(preprocessed_docs.keys())[most_similar_indices[i]]
            avp = get_avp(i+1,doc_id,qd,avp)
            retrived_docs.append(doc_id)
         pr = precision(qd,retrived_docs,10)
         print(f"pr is {pr}")
         #print(pr)
         rec = recall(qd,retrived_docs)    
      avp/=10   
     
      return [avp,pr,rec[0],rec[1]]

def Evaluation_clinc():
      print("clinc-eavluation")
      queries = get_all_queries()
      avp = []
      results = []
      pr = []
      rec = []
      results_avp = [get_result_avp(i) for i in queries]
      avp = [result[0] for result in results_avp]
      results = [result[3] for result in results_avp]
      pr = [result[1] for result in results_avp]
      rec = [result[2] for result in results_avp]
      c = calculate_map(avp)
      print(f"the total map is {c}")      
      n = calculateMrr(results)
      print(f"the total mrr is {n}") 
      precision = sum(pr)
      print(f"the total precision is {precision}") 
      recall = sum(rec)
      print(f"the total recall is {recall}") 
      avpSum = sum(avp)
      return {"map" :c  ,"avp":avpSum , "mrr":n , "pr":precision ,"rec":recall }
          
          

# Create a query
#query = ''
#get_result(query)
#Evaluation_clinc()