import numpy as np
import textdistance
from fuzzywuzzy import fuzz, process

def takeSecond(elem):
    return elem[1]

def text_similarity(s, texts, threshold, limit, choose_library = 'fuzz'):
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
    if choose_library != 'fuzz':
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
            data = (str(t).capitalize(), Ratio*100)
            codes.append(data)

        codes.sort(key = takeSecond)
        codes.reverse()        
        if len(codes) < limit:
            limit = len(codes)
        for i in range(0, limit):
            selected_codes.append(codes[i])


    else: #fuzz library
        selected_codes = process.extract(s, texts, scorer=fuzz.token_sort_ratio, limit=limit) #normal_text or entity_text , scorer=fuzz.token_sort_ratio or partial_token_sort_ratio
    
    return selected_codes

