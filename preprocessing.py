import re

def preprocessing(docs):
    # CLEANING WORDS FROM NON-ALPHANUMERICAL
    cleaned = re.sub("[^a-zA-Z\s]+", " ", docs)
    # FOLDING WORDS
    folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("[^\s0-9][A-Za-z]+", folded)
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
    # TOKENIZING
    token = re.findall("(.*?)(\. |\n)", cleaned)
    return token