import numpy as np
import pandas as pd
import spacy
import re
import json
import pickle
from sentence_transformers import SentenceTransformer
import faiss
from utils.manga_db import *
from src.preprocess import *

model = SentenceTransformer('bert-base-nli-mean-tokens')

mangas = session.query(Manga).all()
base_sentences = list()
list_manga_name = list()
for manga in mangas:
    base_sentences.append(preprocess(manga.description))
    list_manga_name.append(manga.manga_name)

df = pd.DataFrame(base_sentences, columns=["description"])
df['name'] = [str(name) for name in list_manga_name]
df['length'] = [len(i) for i in df['description']]
df = df[df['length']>50]

sentences = df['description'].to_list()
base_names = df['name'].to_list()

sentence_embeddings = model.encode(sentences)

alldata = list()
for i in range(len(sentences)):
    data = dict()
    data['name']=base_names[i]
    data['description']=sentences[i]
    alldata.append(data)

with open("D:/DevSenior_Training/crawl_beetoon/restapi/sentences.json", "w", encoding="utf-8") as f:
    json.dump(alldata, f, indent=4)

with open(f'D:/DevSenior_Training/crawl_beetoon/restapi/sim_sentences/embeddings.npy', 'wb') as fp:
    np.save(fp, sentence_embeddings)