import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from num2words import num2words

EXAMPLE_TEXT = "Hello 3/3/2022  Mr. 200 Smith, how are you doing today? The weather is great, and pythonly while you are pythoning with python is awesome. The sky is pinkish-blue. You shouldn't eat cardboard for better results calls us and what is your moneaay."
boolean_operators = {'AND', 'OR', 'NOT'}


def normalization():
    Data = EXAMPLE_TEXT
    text = strip(Data)
    text = preprocess_dates(text)
    text_list = tokenize(text)
    text_list = convert_numbers(text_list)
    # print("1 \n" + text)
    text_list_tokenized = tokenize(text)
    # print("2 \n")
    # print(text_list_tokenized)
    text_list_stop = stopWords(text_list)
    text_list = text_list_stop
    # print("3 \n")
    # print(text_list_stop)

    text_list_lemitized = lemitizer(text_list)
    text_list = text_list_lemitized

    # print("4 \n")
    # print(text_list_stemmed)
    text_list_stemmed = stemmer(text_list)
    text_list = text_list_stemmed
    print("5 \n")
    print(text_list)
    text_list_spelled = spellChecker(text_list)
    text_list = text_list_spelled
    print("6 \n")
    print(text_list)

    return {"text": text, "token": text_list_tokenized,
            "stopWords": text_list_stop,
            "stem": text_list_stemmed,
            "lemitized": text_list_lemitized,
            "spelled": text_list_spelled}

def preprocess_dates(text):
    # Define regex patterns for different date formats
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',             # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',             # MM/DD/YYYY
        r'\d{2}-\d{2}-\d{4}',             # MM-DD-YYYY
        r'\d{2}/\d{2}/\d{2}',             # MM/DD/YY
        r'\d{2}-\d{2}-\d{2}',             # MM-DD-YY
        # 2
        r'\d{4}-\d{1}-\d{1}',             # YYYY-M-D
        r'\d{1}/\d{1}/\d{4}',             # M/D/YYYY
        r'\d{1}-\d{1}-\d{4}',             # M-D-YYYY
        r'\d{1}/\d{1}/\d{2}',             # M/D/YY
        r'\d{1}-\d{1}-\d{2}',             # M-D-YY
        # 3
        r'\d{2}\s[A-Za-z]{3}\s\d{4}',      # DD Mon YYYY (e.g., 01 Jan 2022)
        r'\d{2}\s[A-Za-z]{3}\.\s\d{4}',    # DD Mon. YYYY (e.g., 01 Jan. 2022)
        # Add more patterns as per your data's date formats
    ]
    
    # Replace date patterns with a placeholder
    placeholder = 'DATE_TOKEN'
    for pattern in date_patterns:
        text = re.sub(pattern, placeholder, text)
    
    return text


def covid(data_list) :
    filtered_text = []
    for i in range(len(data_list)):
        data_list[i] = data_list[i].replace("covid", "coronavirus")
        data_list[i] = data_list[i].replace("sarscov", "coronavirus")
        data_list[i] = data_list[i].replace("cov", "coronavirus")
        data_list[i] = data_list[i].replace("die", "death")
        data_list[i] = data_list[i].replace("respond", "respon")
        data_list[i] = data_list[i].replace("respons", "respon")

    return data_list



def strip(Data):
    text = Data.strip().lower()
    text = re.sub(r'.\n+', '. ', text)  # replace multiple newlines with period
    text = re.sub(r'\n+', '', text)  # replace multiple newlines with period
    text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
    text = re.sub(' +', ' ', text)
    text = re.sub(',', ' ', text)
    text = re.sub(r'\([^()]*\)', '', text)
    text = re.sub(r'https?:\S+\sdoi', '', text)
    text = re.sub(r'biorxiv', '', text)
    text = re.sub(r'preprint', '', text)
    text = re.sub(r':', ' ', text)
    return text

 #Punctuation is the set of unnecessary symbols that are in our corpus documents.
    #  We should be a little careful with what we are doing with this,
    #  there might be few problems such as U.S — us “United Stated” being converted to “us” after the preprocessing.
    #  hyphen and should usually be dealt with little care. But for this problem statement,
    #  we are just going to remove these

def punctution (text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text  


def tokenize(text):
    tokenList = []
    for i, w in enumerate(text.split(" ")):
        tokenList.insert(i, w)
    return tokenList


def sen_tokenizetion(text):
    return sent_tokenize(text)


def word_tokenizetion(text):
    word_token_list = []
    word_token_list = word_tokenize(text)
    return word_token_list


def convert_numbers(data_list):
    processed_text=[]
    for term in data_list:
        if term.isdigit():
            term_is_number = num2words(int(term))
            processed_text.append(term_is_number)
        else:
            processed_text.append(term)
    return processed_text        

def stopWords(text_list):
    stop_words = set(stopwords.words('english'))
    filtered_text = []
    for w in text_list:
        if w not in stop_words:
            if w != '':
                filtered_text.append(w)
    return filtered_text


def stemmer(text_list):
    ps = PorterStemmer()
    stemmed_text = []
    for w in text_list:
        stemmed_text.append(ps.stem(w))
    return stemmed_text


def lemitizer(text_list):
    lemmatizer = WordNetLemmatizer()
    lemitized_text = []
    for w in text_list:
        lemitized_text.append(lemmatizer.lemmatize(w))
    return lemitized_text


def spellChecker(text_list):
    corrected_list = []
    spell = SpellChecker()
    for text in text_list:
        old_word = text
        new_word = spell.correction(text)
        if new_word is not None:
            corrected_list.append(new_word)
        else:
            corrected_list.append(old_word)    

    return corrected_list


#normalization(EXAMPLE_TEXT)
