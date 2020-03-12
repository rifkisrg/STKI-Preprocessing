from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from bs4 import BeautifulSoup
import preprocessing as pp
import re
from datetime import datetime
from collections import Counter

print("Program start at = ", datetime.now().time())

factory = StemmerFactory()
stemmer = factory.create_stemmer()

f = open("corpus1.txt", 'r', encoding='utf8')
with open("new-kata-dasar.txt", 'r') as kata:
    katdas = kata.read()

soup = BeautifulSoup(f, 'html.parser')

filtered = soup.find_all("doc")
# jumlah_docs = count(filtered)
id_docs = []
kosong = []
# jumlah_kata = 0
words_with_ber = []
separator = " "
dict_kosong = {}

for docs in filtered:
    docs_id = docs.find("id").text
    id_docs.append(docs_id)
    docs_title = docs.find("title").text
    docs_text = docs.find("text").text
    title_docs_pp = pp.preprocessing_title(docs_title)
    docs_token = pp.preprocessing(docs_text)
    kosong.append(title_docs_pp)
    kosong.append(docs_token)

    dict_kosong.update({title_docs_pp: docs_token})

def find_kata_dasar(array_kata):
    jumlah_kata = 0
    kata_dasar = []
    for doc_words in array_kata:
        words_length = len(doc_words)
        jumlah_kata += words_length
        words_as_string = separator.join(doc_words)
        reg = re.findall(r"\bber[A-Za-z]+", words_as_string)
        for words in reg:
            if words in katdas:
                reg.remove(words)
            else:
                if words == re.search(r"\Ber", words):
                    new_words = re.sub(r"\bbe", "", words)
                    if new_words in katdas:
                        kata_dasar.append(new_words)
                else:
                    new_words = re.sub(r"\bber", "", words)
                    if new_words in katdas:
                        kata_dasar.append(new_words)
    return kata_dasar

def calculate_all_words(array_of_words):
    jlh_kata = 0
    for x in array_of_words:
        jlh_kata += len(x)
    return jlh_kata

# print(Counter(dict_kosong.values()))
kata_dasar = find_kata_dasar(kosong)

print(len(list(set(kata_dasar))))
# x = list(set(kata_dasar))
# print(len(x))
# print(len(kosong))
# print(len(stemmed))
# print(words_with_ber)
print(calculate_all_words(kosong))
# for title in kosong.keys():
#     print(title)

print("Program end at = ", datetime.now().time())