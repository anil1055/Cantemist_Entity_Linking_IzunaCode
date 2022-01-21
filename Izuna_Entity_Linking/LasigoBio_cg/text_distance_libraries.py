import numpy as np
import textdistance
from fuzzywuzzy import fuzz, process
import difflib
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords
import string
import spacy

model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
STOPWORDS = set(stopwords.words('spanish'))
#model_es = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
#nlp = spacy.load('es_core_news_md', disable=['ner'])

def takeSecond(elem):
    return elem[1]

def text_similarity(s, texts, threshold, limit, choose_library = 'sbert'):
    """ text_similarity:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    codes = []
    selected_codes = []
    s = s.lower()
    if choose_library == 'distance':
        for t in texts:
            t = t.lower()
            Ratio = 0
            if choose_library == 'levenshtein':
                Ratio = textdistance.levenshtein.normalized_similarity(s, t)
            elif choose_library == 'jaccard':
                Ratio = textdistance.jaccard.normalized_similarity(s, t)
            elif choose_library == 'cos':
                Ratio = textdistance.cosine.normalized_similarity(s, t)
            elif choose_library == 'ratcliff':
                Ratio = textdistance.ratcliff_obershelp.normalized_similarity(s, t)
            elif choose_library == 'difflib':
                Ratio = difflib.SequenceMatcher(None, s, t).ratio()
            data = (str(t).capitalize(), Ratio*100)
            codes.append(data)

        codes.sort(key = takeSecond)
        codes.reverse()        
        if len(codes) < limit:
            limit = len(codes)
        for i in range(0, limit):
            selected_codes.append(codes[i])

    if choose_library == 'sbert':   
        desc = [x.lower() for x in texts]
        texts = [x for x in texts]
        #Compute embedding for both lists
        embeddings1 = model.encode(s, convert_to_tensor=True)
        embeddings2 = model.encode(desc[:10], convert_to_tensor=True)
        ratios = util.cos_sim(embeddings1, embeddings2)

        for i in range(0, len(desc[:10])):
            #value = str(ratios[0][i]).split(',')  #for GPU
            #ratio = str(value[0])[7:-1]
            ratio = str(ratios[0][i])[7:-1]
            data = (str(texts[i]), float(ratio)*100)
            codes.append(data)            
        codes.sort(key = takeSecond)
        codes.reverse()        
        if len(codes) < limit:
            limit = len(codes)
        for i in range(0, limit):
            selected_codes.append(codes[i])

    if choose_library == 'fuzz': #fuzz library
        selected_codes = process.extract(s, texts, scorer=fuzz.token_sort_ratio, limit=limit) #normal_text or entity_text , scorer=fuzz.token_sort_ratio or partial_token_sort_ratio

    if choose_library == 'fuzz_pre': #fuzz library
        out = str(s).maketrans('','', string.punctuation)
        s = str(s).translate(out)
        sent = ' '.join(word for word in str(s).split() if word not in STOPWORDS)
        sent = sent.strip()
        texts = [x for x in texts]
        ind = 0
        txt = []
        fake_real = []
        for tx in texts:
            t = tx.lower()
            out = str(t).maketrans('','', string.punctuation)
            t = str(t).translate(out)
            text = ' '.join(word for word in str(t).split() if word not in STOPWORDS)
            txt.append(text.strip())
            data = (str(text), str(tx))
            fake_real.append(data)
        selected = process.extract(sent, txt, scorer=fuzz.token_sort_ratio, limit=limit) #normal_text or entity_text , scorer=fuzz.token_sort_ratio or partial_token_sort_ratio
        selected_codes = []
        for t1, c1 in selected:
            for s1, s2 in fake_real:
                if t1 == s1:
                    data = (str(s2), float(c1))
                    selected_codes.append(data)
                    break

    if choose_library == 'spacy':
        out = str(s).maketrans('','', string.punctuation)
        result_s = str(s).translate(out)
        sent = nlp(result_s)
        texts = [x for x in texts]
        ind = 0
        for t in texts:
            t = t.lower()
            out = str(t).maketrans('','', string.punctuation)
            result_t = str(t).translate(out)
            tokens = nlp(result_t)

            ratio = sent.similarity(tokens)
            data = (str(texts[ind]), float(ratio)*100)
            codes.append(data)
            ind += 1

        codes.sort(key = takeSecond)
        codes.reverse()        
        if len(codes) < limit:
            limit = len(codes)
        for i in range(0, limit):
            selected_codes.append(codes[i])

    return selected_codes

