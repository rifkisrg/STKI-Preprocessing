from bs4 import BeautifulSoup
import preprocessing as pp
import numpy as np
import re
import collections

#B,F,K

f = open("corpus_tri.txt", 'r', encoding='ansi')

soup = BeautifulSoup(f, 'html.parser')
filtered = soup.find_all("doc")
# jumlah_docs = count(filtered)
jumlah_kata = 0

def cariFrekuensiKata():
    corpus = []
    kata = {}
    filtered = soup.find_all("doc")
    for docs in filtered:
        regex = r"[^_0-9\W]+"
        docs_title = docs.find("title").text
        docs_title = re.findall(regex,docs_title.lower())
        docs_text = docs.find("text").text
        docs_token = pp.preprocessing(docs_text)
        corpus += docs_title
        corpus = docs_token + corpus

    for words in corpus:
        count = 0
        if words not in kata:
            kata[words]=0
        kata[words] +=1

    return kata

def frekuensibanyak20(kata):
    corpus={k: v for k, v in sorted(kata.items(), key= lambda  item:(-item[1],item[0]))}
    # print(corpus)
    # print(" \n\n")
    tes = dict(list(collections.Counter.most_common(corpus))[:20])
    print(tes)
    len(tes)
    print(" \n\n")
    #mendapatkan 20 peringkat frekuensi kata terbanyak
    out = dict(list(corpus.items())[:20])
    print(out)
    print(len(out))

kata = cariFrekuensiKata()
frekuensibanyak20(kata)