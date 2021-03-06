import spacy
import glob
import json
import os
from multiprocessing import Pool
import multiprocessing as multi
import pickle
import scispacy
from scispacy.linking import EntityLinker
from spacy.symbols import ORTH
import time
import re
from spacy.language import Language
import pdb
import copy
from tqdm import tqdm
from scispacy.candidate_generation import CandidateGenerator
import candidates_cantemist
import generator_cantemist
import generator_bc5cdr
from sklearn.feature_extraction.text import TfidfVectorizer

mentions = list()
with open('./dataset/bc5cdr_mentions.txt', 'r') as f:
    for line in f:
        mention = line.strip()
        mentions.append(mention)

def tfidf(mention_strings):
    vectorizer = TfidfVectorizer(analyzer='char_wb', min_df=10, ngram_range=(3, 3)).fit(mention_strings)

    return vectorizer

vector = tfidf(mentions)
#KB_C = candidates_cantemist.createCandidateCantemist()
MeshCandidateGenrator = generator_bc5cdr.CandidateGenerator(name = 'mesh')
#CanteCandidateGenrator = generator_cantemist.CandidateGenerator(kb = KB_C, tfidf_vectorizer = vector)
KB=MeshCandidateGenrator.kb
K=200
Resolve_abbreviations = True
Threshold = 0.1
No_definition_threshold = 0.95
Filter_for_definitions = True
Max_entities_per_mention  = 200

def candidate_dui_generator(mention_strings):
    batch_candidates = MeshCandidateGenrator(mention_strings, K)
    batched_sorted_candidates = list()
    for candidates in batch_candidates:
        predicted = []
        for cand in candidates:
            score = max(cand.similarities)
            if (
                    Filter_for_definitions
                    and KB.cui_to_entity[cand.concept_id].definition is None
                    and score < No_definition_threshold
            ):
                continue
            if score > Threshold:
                predicted.append((cand.concept_id, score))
        sorted_predicted = sorted(predicted, reverse=True, key=lambda x: x[1])
        sorted_predicted = sorted_predicted[: Max_entities_per_mention]
        batched_sorted_candidates.append(sorted_predicted)

    return batched_sorted_candidates

def batcher(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]