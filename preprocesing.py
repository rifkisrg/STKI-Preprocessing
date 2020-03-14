from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

factory = StemmerFactory()
stemmer = factory.create_stemmer()


def preprocessing(docs):
    # CLEANING WORDS FROM NON-ALPHANUMERICAL
    cleaned = re.sub("[^a-zA-Z\s]+", " ", docs)
    # FOLDING WORDS
    folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("[^\s0-9][A-Za-z]+", folded)
    # STEMMING
    # belum berhasil, masih makan waktu lama

    # separator = " "
    # token_as_string = separator.join(token)
    # stemmed = re.findall("[^\s0-9][A-Za-z]+", stemmer.stem(token_as_string))
    return token


def preprocessing_title(docs):
    cleaned = re.sub("[^a-zA-Z\s]+", " ", docs)
    # FOLDING WORDS
    folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("[^\s0-9][A-Za-z]+", folded)

    separator = " "
    token_as_string = separator.join(token)

    return token_as_string


def preprocessingKalimat(docs):
    # CLEANING WORDS FROM NON-ALPHANUMERICAL
    cleaned = re.sub("<.*?>(\w+-[0-9]{0,90}|\d{2,90})?", " ", docs)
    # FOLDING WORDS
    # folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("(.*?)(\. |\n)", cleaned)
    return token