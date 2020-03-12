from bs4 import BeautifulSoup
import preprocessing as pp
import numpy as np
import re
import collections

f = open("corpus.txt", 'r', encoding='ansi')
f2 = open("corpus.txt", 'r', encoding='ansi')
soup = BeautifulSoup(f, 'html.parser')
filtered = soup.find_all("doc")
filtered2 = f2.read()

def cariKalimat(corpus):
    kalimat = []
    tes = pp.preprocessingKalimat(corpus)
    for i in range(len(tes)):
        for j in range(len(tes[i])):
            if len(tes[i][j]) > 3:
                kalimat.append(tes[i][j])
            else: pass
    print(f"Banyak kalimat dalam corpus adalah: {len(kalimat)}")


#mendapatkan semua frekuensi kata yang belum diurutkan
def cariFrekuensiKata(doc):
    corpus = []
    kata = {}

    for docs in doc:
        regex = r"[^_0-9\W]+"
        docs_title = docs.find("title").text
        docs_title = re.findall(regex,docs_title.lower())
        docs_text = docs.find("text").text
        docs_token = pp.preprocessing(docs_text)
        corpus += docs_title
        corpus = docs_token + corpus

    for words in corpus:
        if words not in kata:
            kata[words]=0
        kata[words] +=1

    return kata

#mendapatkan frekuensi kata terbesar dari 20 peringkat yang sudah diurutkan
def frekuensibanyak20(kata):
    corpus={k: v for k, v in sorted(kata.items(), key=lambda item:(-item[1],item[0]))}
    #mendapatkan 20 peringkat frekuensi kata terbanyak
    out = dict(list(corpus.items())[:20])
    print(f"20 peringkat dengan frekuensi kata terbanyak:\n{out}\n")

def frekuensiKurang10(kata):
    corpus={k: v for k, v in sorted(kata.items(), key=lambda item:(-item[1],item[0]))}
    out = dict((k, v) for k, v in corpus.items() if v < 10)
    print(f"Banyak kata yang kurang dari 10 buah yaitu: {len(out)}\n")

kata = cariFrekuensiKata(filtered)
frekuensibanyak20(kata)
frekuensiKurang10(kata)
cariKalimat(filtered2)