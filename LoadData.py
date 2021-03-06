import sqlite3
import re
from spacy.en.language_data import STOP_WORDS
from spacy.en import English
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import spacy
import time
import csv
from bs4 import BeautifulSoup

def create_connection(db_file):
    # create a database connection to the SQLite database
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def load_data(conn):
	cursor = conn.cursor()
	SQL = "Select * from sm_post;"
	# SQL = "Select * from sm_post where serial='4';"
	cursor.execute(SQL)
	title = list()

	return cursor
	
def clean_data(text, stop_words, nlp):
	clean_text = re.sub(r'[^a-zA-Z ]', ' ', text).lower()
	# print("***************")
	# print("TEXT WITH STOP WORDS:")
	# print(clean_text)
	text_without_stop_words = remove_stopwords_lemmatize(clean_text, stop_words, nlp)
	return text_without_stop_words

def remove_stopwords_lemmatize(clean_text, stop_words, nlp):
	stop_words_removed = ' '.join(filter(lambda x: x.lower() not in stop_words,  clean_text.split()))
	doc = nlp(stop_words_removed)
	lemmatized_sentence = ' '.join([x.lemma_ for x in doc])
	return lemmatized_sentence

def open_csv(file):
	return csv.writer(open(file,'w'), doublequote=False, escapechar='\\')

def body_split(body):
	# print(body)
	soup = BeautifulSoup(body, "html5lib")
	t2_soup=soup.find_all('code')
	code_text = ""
	text_without_code = re.sub(r'<code>.*?</code>', ' ', body)
	soup2 = BeautifulSoup(text_without_code, "html5lib")
	text_without_code_tags = soup2.get_text()

	for item in t2_soup:
		code_text = code_text + str(item.text) + "\n"

	return text_without_code_tags, code_text

def main():
	en_stopwords = stopwords.words('english')
	stop_words = list(STOP_WORDS) + list(ENGLISH_STOP_WORDS) + list(en_stopwords)
	
	nlp = spacy.load('en')
	
	conn   = create_connection("Sotags.db")
	cursor = load_data(conn)

	title_csv = open_csv('title.csv')
	title_csv.writerow(['serial','title','tag'])

	body_csv = open_csv('body.csv')
	body_csv.writerow(['serial','body','tag'])

	code_csv = open_csv('code.csv')
	code_csv.writerow(['serial','code','tag'])


	start_time = time.time()
	
	for data in cursor:
		title = clean_data(data[2], stop_words, nlp)
		body_text, body_code = body_split(data[3])
		body  = clean_data(body_text, stop_words, nlp)
		
		title_csv.writerow([data[0],title,data[4]])
		body_csv.writerow([data[0],body,data[4]])
		code_csv.writerow([data[0],body_code,data[4]])
	print("--- %s seconds ---" % (time.time() - start_time))


main()

