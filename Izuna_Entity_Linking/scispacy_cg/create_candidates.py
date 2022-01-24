from scg_candidate_generator import candidate_dui_generator, batcher, tfidf
from tqdm import tqdm
import atexit
import logging
import networkx as nx
import os
import pickle
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import scg_candidate_generator
sys.path.append("./")
bc5cdr_cache_file = "./tmp/bc5cdr_cache100.pkl"

if os.path.isfile(bc5cdr_cache_file):
    logging.info("loading bc5cdr dictionary...")
    bc5cdr_cache = pickle.load(open(bc5cdr_cache_file, "rb"))
    loadedbc5cdr = True
    logging.info("loaded bc5cdr dictionary with %s entries", str(len(bc5cdr_cache)))
else:
    bc5cdr_cache = {}
    loadedbc5cdr = False
    logging.info("new bc5cdr dictionary")

def exit_handler():
    print('Saving bc5cdr dictionary...!')
    pickle.dump(bc5cdr_cache, open(bc5cdr_cache_file, "wb"))

atexit.register(exit_handler)


if __name__ == '__main__':
    mentions = list()
    with open('./dataset/bc5cdr_mentions.txt', 'r') as f:
        for line in f:
            mention = line.strip()
            mentions.append(mention)
    entire_candidates = list()
    scg_candidate_generator.vector = tfidf(mentions)
    for batch in tqdm(batcher(mentions, 64)):
        batch_candidates = candidate_dui_generator(batch)
        #bc5cdr_cache[batch] = batch_candidates
        entire_candidates += batch_candidates
    print(len(entire_candidates))
    ind = 0
    for cand in entire_candidates:
        bc5cdr_cache[mentions[ind]] = cand
        ind += 1