from bs4 import BeautifulSoup
from time import time
import re
from collections import Counter
import matplotlib.pyplot as plt

current = time()

# Korpus dokumen
f = open("corpus.txt", 'r', encoding='ansi').read()
f2 = open("corpus.txt", 'r', encoding='ansi').read() #untuk menghitung jumlah kalimat

# Korpus Pak Putra Pandu Adikara yang dijadikan acuan dalam beberapa proses di program ini
with open("new-kata-dasar.txt", 'r') as kata:
    katdas = kata.read()

# Method untuk preprocessing (cleaning, folding, tokenisasi pada dokumen)
def preprocessing(docs):
    # CLEANING WORDS FROM NON-ALPHANUMERICAL
    cleaned = re.sub("[^a-zA-Z\s]+", " ", docs)
    # FOLDING WORDS
    folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("[^\s0-9][A-Za-z]+", folded)
    return token

# Method untuk preprocessing yang akan digunakan saat pada saat segmentasi kalimat
def preprocessingKalimat(docs):
    # CLEANING WORDS FROM NON-ALPHANUMERICAL
    cleaned = re.sub("<.*?>(\w+-[0-9]{0,90}|\d{2,90})?", " ", docs)
    # TOKENIZING
    token = re.findall("(.*?)(\. |\n)", cleaned)
    return token

titles = re.findall("<TITLE>(.*?)<\/TITLE>", f, re.DOTALL) #regex untuk mengambil title pada korpus
texts = re.findall("<TEXT>(.*?)<\/TEXT>", f, re.DOTALL)  #regex untuk mengambil text pada korpus

list_of_title = [] # List untuk menyimpan semua title pada korpus
list_of_text = [] # List untuk menyimpan semua text pada korpus

for title in titles:
    title = preprocessing(title)
    list_of_title.append(title)

for text in texts:
    text = preprocessing(text)
    list_of_text.append(text)

all_words = sum(list_of_title+list_of_text, []) #Menyatukan list yang berisi teks title dan teks tag

# Menghitung jumlah kalimat didalam korpus
def cariKalimat(corpus):
    kalimat = []
    tes = preprocessingKalimat(corpus)
    for i in range(len(tes)):
        for j in range(len(tes[i])):
            if len(tes[i][j]) > 3:
                kalimat.append(tes[i][j])
            else: pass
    return len(kalimat)

# Mencari kata dasar dari kata yang memiliki imbuhan ber-
def find_kata_dasar(array_kata):
    jumlah_kata = 0
    kata_dasar = []
    for doc_words in array_kata:
        words_length = len(doc_words)
        jumlah_kata += words_length
        words_as_string = " ".join(doc_words)
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
    return len(list(set(kata_dasar)))

# Mencari kata dasar dari kata yang memiliki imbuhan -kan
def cari_imbuhan_kan(array_kata):
    kata_dasar = []
    gabungan_kata_unik = " ".join(array_kata)
    reg = re.findall(r"[A-Za-z]+kan\b", gabungan_kata_unik)
    
    for word in reg:
        if word in katdas:
            reg.remove(word)
        else:
            kata_dasar.append(word)

    return len(set(kata_dasar))

# Menghitung banyak token pada korpus
def calculate_all_words(array_of_words):
    jumlah_kata = [len(x) for x in array_of_words]
    return sum(jumlah_kata)

# Menghitung frekuensi setiap token pada korpus, untuk mencari 20 kata yang muncul di seluruh dokumen dan 10 kata yang hanya muncul di 50 dokumen
def find_doc_freq(array_of_title, array_of_text):
    docs_freq = {}
    for i, j in zip(array_of_title, array_of_text):
        appended = i + j
        kata_muncul = list(set(appended))
        for x in kata_muncul:
            if x not in docs_freq.keys():
                docs_freq.update({x: 1})
            else:
                docs_freq[x] += 1

    on_50_only = [key for key, val in docs_freq.items() if val == 50]
    all_docs = [key for key, val in docs_freq.items() if val == 900]

    return [on_50_only, all_docs]

# Menghitung jumlah frasa bigram dan trigram
def ngrams(array_of_text, n):
    x = []
    for y in array_of_text:
        ngrams = lambda a, n: zip(*[a[i:] for i in range(n)])
        z = ngrams(y, n)
        x.append(list(z))

    res = sum(x, [])
    return res

# Mencari jumlah dokumen dari korpus
print("A. Banyak dokumen dalam korpus adalah ", len(list_of_title), "dokumen")

# Mengambil 20 kata dengan kemunculan yang paling banyak
print("B. 20 kata dengan kemunculan yang paling banyak : ",Counter(all_words).most_common(20))

# Memanggil fungsi untuk mencari jumlah dokumen yang mengandung suatu kata tertentu
docs_freq = find_doc_freq(list_of_title, list_of_text)
# 20 Kata yang muncul di seluruh dokumen
print("C. 20 Kata yang muncul di setiap dokumen : ", docs_freq[1])
# 10 Kata yang muncul pada 50 dokumen
print("D. 10 Kata yang hanya muncul di 50 dokumen : ", docs_freq[0][:10])

# Mengambil kata dengan kemunculan kurang dari 10 kali
temp_list = [val for val in Counter(all_words).values() if val < 10]
print("F. Banyak kata yang frekuensinya kurang dari 10 adalah : ",len(temp_list), " kata")

# Mencari jumlah seluruh kata dari korpus
print("G. Banyak seluruh kata dalam korpus adalah ", calculate_all_words(list_of_title + list_of_text), " kata")

# Jumlah kata unik pada korpus
print("H. Kata unik pada korpus berjumlah sebanyak ", len(set(all_words)), " kata")

# Mencari kata dasar dari imbuhan ber-
kata_dasar = find_kata_dasar(list_of_title + list_of_text)
print("I. Jumlah kata unik yang berimbuhan ber- : ",kata_dasar, " kata")

# Mencari kata dasar dari imbuhan -kan
words_with_an = cari_imbuhan_kan(sum(list_of_title + list_of_text, []))
print("J. Jumlah kata unik yang berimbuhan -an : ", words_with_an, " kata")

# Mencari banyak kalimat dalam korpus
print("K. Jumlah kalimat dalam korpus : ", cariKalimat(f2), " kalimat")

# Mencari frase bigram dari setiap title dan text
bigram_from_title = ngrams(list_of_title, 2)
bigram_from_text = ngrams(list_of_text, 2)
# Mencari frase trigram dari setiap title dan text
trigram_from_title = ngrams(list_of_title, 3)
trigram_from_text = ngrams(list_of_text, 3)
# Mengambil 20 frase bigram dan trigram dengan kemunculan yang paling banyak
print("L1. Frekuensi 20 frase Bigram yang paling sering muncul: \n", Counter(bigram_from_title + bigram_from_text).most_common(20))
print("L2. Frekuensi 20 frase Trigram yang paling sering muncul: \n",Counter(trigram_from_title + trigram_from_text).most_common(20))

# Grafik distribusi Zipf dengan mengambil sebanyak 50 kata yang paling sering muncul
# Menjawab soal nomor 3 poin E.
counter_gambar = dict(Counter(all_words).most_common(50))

x = [token for token in counter_gambar.keys()]
y = [jumlah for jumlah in counter_gambar.values()]

print("Gambar grafik distibusi zipf pada korpus: ")
plt.plot(x,y)
plt.xlabel('Token')
plt.ylabel('Jumlah')
plt.title('Distribusi Zipf')
plt.show()

print(time() - current, "detik")