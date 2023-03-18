import numpy as np
import pandas as pd
import spacy
import re
import pickle
from sentence_transformers import SentenceTransformer
import faiss
from utils.manga_db import *
from src.preprocess import *

model = SentenceTransformer('bert-base-nli-mean-tokens')
with open(r"./sentences.json", "r", encoding="utf-8") as f:
    df = pd.read_json(f)

base_sentences = df['description'].to_list()
base_names = df['name'].to_list()

i_path = r'./embeddings.npy'
with open(i_path, 'rb') as pickle_file:
    sentences_embedding = np.load(pickle_file)

d = sentences_embedding.shape[1]
index = faiss.IndexFlatL2(d)
index.add(sentences_embedding)

def get_similar_manga(desc ,k):
    k = 5
    xq = model.encode([preprocess(desc)])
    D, I = index.search(xq, k)
    return [f'{i}: {base_names[i]}' for i in I[0]]