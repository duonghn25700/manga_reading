import numpy as np
import pandas as pd
import spacy
import re
import pickle
from sentence_transformers import SentenceTransformer
import faiss


def preprocess2(text):
    doc = nlp(text)
    filter_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
           continue
        filter_tokens.append(token.lemma_)
    return " ".join(filter_tokens)


def preprocess(text):
    text = re.sub(r'[^\w\s]',' ',text)
    text = re.sub("[ \n\r]+"," ", text)
    return text.strip().lower()
