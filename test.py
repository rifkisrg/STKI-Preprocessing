from bs4 import BeautifulSoup
import preprocessing as pp

f = open("corpus.txt", 'r', encoding='ansi')

soup = BeautifulSoup(f, 'html.parser')

filtered = soup.find_all("doc")
# jumlah_docs = count(filtered)
kosong = {}
jumlah_kata = 0

for docs in filtered:
    docs_title = docs.find("title").text
    docs_text = docs.find("text").text
    docs_token = pp.preprocessing(docs_text)

    kosong.update({docs_title : docs_token})

# for words in kosong.keys():
#     words_length = len(words)
#     jumlah_kata += words_length

print(kosong)
# print(jumlah_kata)