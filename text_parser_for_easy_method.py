import os
import pickle
import numpy as np
from text_processor import clear_ending
import sqlite3
base = sqlite3.connect("example.db")
cursor = base.cursor()

with open(os.path.join("dictionaries", "word_to_id"), "rb") as f:
    word_to_id = pickle.load(f)


with open(os.path.join("dictionaries", "words_in_chunks"), "rb") as f:
    words_in_chunks = pickle.load(f)  

with open(os.path.join("dictionaries", "data_for_words"), "r", encoding="utf-8") as f:
    words_in_text, chunks_avg = [int(i.strip()) for i in f]
matrix = np.load("matrix.npy")
request = "как найти площадь под графиком функции"
vector = np.zeros(len(word_to_id))
for i in request.split(" "):
    i = clear_ending(i.lower())
    if i in word_to_id:
        vector[word_to_id[i]] = 1
dl = np.linalg.norm(vector)
if dl!= 0:
    vector/= dl
    res = matrix@vector.T
    
    ans = np.argmax(res)
    cursor.execute("SELECT * FROM nodes WHERE vector_id=(?)", (int(ans), ))
    row = cursor.fetchone()
    if row:
        print(row[1], row[2])
base.close()
    
