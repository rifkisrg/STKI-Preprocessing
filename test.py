from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from bs4 import BeautifulSoup
import preprocessing as pp
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

print("Program start at = ", datetime.now().time())

factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Korpus dokumen
f = open("corpus.txt", 'r', encoding='ansi')
f2 = open("corpus.txt", 'r', encoding='ansi')

# Korpus Pak Putra Pandu Adikara yang dijadikan acuan dalam beberapa proses di program ini
with open("new-kata-dasar.txt", 'r') as kata:
    katdas = kata.read()

# Memparsing file corpus dokumen agar dapat diproses
soup = BeautifulSoup(f, 'html.parser')

filtered = soup.find_all("doc")
filtered2 = f2.read()
list_of_title = [] #List untuk menyimpan teks dari tag title
list_of_text = [] #List untuk menyimpan teks dari tag text
list_of_sentence = []
words_with_ber = [] #List untuk menyimpan kata dengan 3 huruf awal berupa "ber"
separator = " "

for docs in filtered:
    docs_title = docs.find("title").text
    docs_text = docs.find("text").text
    title_docs_pp = pp.preprocessing(docs_title)
    docs_token = pp.preprocessing(docs_text)
    list_of_title.append(title_docs_pp)
    list_of_text.append(docs_token)

all_words = sum(list_of_title+list_of_text, []) #Menyatukan list yang berisi teks title dan teks tag

def cariKalimat(corpus):
    kalimat = []
    tes = pp.preprocessingKalimat(corpus)
    for i in range(len(tes)):
        for j in range(len(tes[i])):
            if len(tes[i][j]) > 3:
                kalimat.append(tes[i][j])
            else: pass
    print(f"Banyak kalimat dalam corpus adalah: {len(kalimat)}")

cariKalimat(filtered2)
# print(len(list_of_sentence))

# Mencari kata dasar dari kata yang memiliki imbuhan ber-
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

def calculate_all_words(array_of_words):
    jlh_kata = 0
    for x in array_of_words:
        jlh_kata += len(x)
    return jlh_kata

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

def ngrams(array_of_text, n):
    x = []
    for y in array_of_text:
        ngrams = lambda a, n: zip(*[a[i:] for i in range(n)])
        z = ngrams(y, n)
        x.append(list(z))

    res = sum(x, [])
    return res

# Mengambil 20 kata dengan kemunculan yang paling banyak
print(Counter(all_words).most_common(20))

# Mengambil kata dengan kemunculan kurang dari 10 kali
temp_list = [val for val in Counter(all_words).values() if val < 10]
# for x in Counter(all_words).items():
#     if x[1] < 10:
#         temp_list.append(x[0])

print("Banyak kata yang frekuensinya kurang dari 10 adalah : ",len(temp_list), " kata")

# Memanggil fungsi untuk mencari jumlah dokumen yang mengandung suatu kata tertentu
docs_freq = find_doc_freq(list_of_title, list_of_text)
# # Kata yang muncul di seluruh dokumen
print("Kata yang muncul di setiap dokumen : ", docs_freq[1])
# # 10 Kata yang muncul pada 50 dokumen
print("10 Kata yang hanya muncul di 50 dokumen : ", docs_freq[0][:10])

# Mencari kata dasar dari imbuhan ber-
kata_dasar = find_kata_dasar(list_of_title + list_of_text)
print("Jumlah kata unik yang berimbuhan ber- : ",kata_dasar)

# Mencari kata dasar dari imbuhan -kan
words_with_an = cari_imbuhan_kan(sum(list_of_title + list_of_text, []))
print("Jumlah kata unik yang berimbuhan -an : ", words_with_an)

# Mencari jumlah dokumen dari korpus
print("Banyak dokumen dalam korpus adalah ", len(list_of_title), "dokumen")

# Mencari jumlah seluruh kata dari korpus
print("Banyak seluruh kata dalam korpus adalah ", calculate_all_words(list_of_title + list_of_text), " Kata")


# Grafik distribusi Zipf dengan mengambil sebanyak 50 kata yang paling sering muncul
counter_gambar = dict(Counter(all_words).most_common(50))

x = [token for token in counter_gambar.keys()]
y = [jumlah for jumlah in counter_gambar.values()]

plt.plot(x,y)
plt.xlabel('Token')
plt.ylabel('Jumlah')
plt.title('Distribusi Zipf')
plt.show()

# Mencari frase bigram dari setiap title dan text
bigram_from_title = ngrams(list_of_title, 2)
bigram_from_text = ngrams(list_of_text, 2)

# Mencari frase trigram dari setiap title dan text
trigram_from_title = ngrams(list_of_title, 3)
trigram_from_text = ngrams(list_of_text, 3)

# Mengambil 20 frase bigram dan trigram dengan kemunculan yang paling banyak
print("Frekuensi 20 frase Bigram yang paling sering muncul: ", Counter(bigram_from_title + bigram_from_text).most_common(20))
print("Frekuensi 20 frase Trigram yang paling sering muncul: ",Counter(trigram_from_title + trigram_from_text).most_common(20))

print("Program end at = ", datetime.now().time())