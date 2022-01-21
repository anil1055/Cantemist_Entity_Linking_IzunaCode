import json, pickle, pdb
from parameteres import Biencoder_params
from convert_cantemist import fileBC5CDR
from annotations import parse_ner_output
from cieo3 import load_cieo3
from pre_process_norm import build_entity_candidate_dict
from collections import OrderedDict

class CandidateReaderForTestDataset:
    def __init__(self, config):
        self.config = config
        self.mention2candidate_duis = self._dui2candidate_duis_returner()

    def _dui2candidate_duis_returner(self):
        with open(self.config.candidates_dataset, 'rb') as f:
            c = pickle.load(f)

        ontology_graph, name_to_id, synonym_to_id  = load_cieo3() 
        annotations = parse_ner_output(True)
        mention_list = []
        if str(self.config.candidates_dataset).find('ecie03') != -1:            
            candidates_list = []            
            for ment in c:
                mention_list.append(ment)
                cnd = []
                value = []
                for i, scr in c[ment]:
                    tpl = (str(i) , float(scr/100))
                    cnd.append(tpl)
                candidates_list.append(cnd)
            c['mentions'] = mention_list
            c['candidates'] = candidates_list
        elif str(self.config.candidates_dataset).find('candidates') != -1:
            candidates_list = []            
            for ment in c:
                mention_list.append(ment)
                cnd = []
                for i, scr in c[ment]:
                    tpl = (str(i) , float(scr))
                    cnd.append(tpl)
                candidates_list.append(cnd)
            c['mentions'] = mention_list
            c['candidates'] = candidates_list

        mention_ = list(OrderedDict.fromkeys(mention_list)) 
        mention2candidate_duis = {}
        url_true = 0  
        mention_ind = 0
        for mention, its_candidates in zip(c['mentions'], c['candidates']):            
            mention = str(mention).replace('_', ' ')
            for document in annotations.keys(): 
                annotate_text = ''
                control_2 = False
                for annotation in annotations[document]: 
                    control = False
                    if annotation[0].isnumeric() == False:
                        annotate_text = str(annotation[0]) 
                    if annotation[0].isnumeric() == True and str(annotation).find('/') != -1:
                        if annotate_text.lower() == str(mention).lower():  
                            for code, rate in its_candidates:                                
                                if str(code) == str(annotation):
                                    url_true += 1  
                                    control = True
                                    control_2 = True
                                    break
                            if control: break                        
                if control_2: break
            mention_ind += 1
        print('Access rate: ' + str(url_true/len(mention_list)*100))
        return url_true
    

    def BC5CDRstats(self):
        with open(self.config.candidates_dataset, 'rb') as f:
            c = pickle.load(f)
        mention_list = []
        candidates_list = []            
        for ment in c:
            mention_list.append(ment)
            cnd = []
            for i, scr in c[ment]:
                tpl = (str(i) , float(scr))
                cnd.append(tpl)
            candidates_list.append(cnd)
        c['mentions'] = mention_list
        c['candidates'] = candidates_list
        annotators = fileBC5CDR()
        acc_5 = 0
        acc_10 = 0
        acc_50 = 0
        acc_100 = 0
        total = 0
        for mention, its_candidates in zip(c['mentions'], c['candidates']):
            for text, code in annotators:
                control = False
                if mention == text:
                    ind = 0                  
                    for cnd, rate in its_candidates:
                        if cnd == code:
                            if ind < 5:
                                acc_5 += 1
                                acc_10 += 1
                                acc_50 += 1 
                                acc_100 += 1
                            elif ind >= 5 and ind < 10:
                                acc_10 += 1
                                acc_50 += 1
                                acc_100 += 1
                            elif ind >= 10 and ind < 50:
                                acc_50 += 1
                                acc_100 += 1
                            elif ind >= 50 and ind < 100:
                                acc_100 += 1
                            control = True
                            break
                        ind += 1
                if control:
                    break
            total += 1
        print("Stats")
        

if __name__ == '__main__':
    config = Biencoder_params()
    params = config.opts
    cg = CandidateReaderForTestDataset(config=params)
    #cg.BC5CDRstats()
    cg._dui2candidate_duis_returner()