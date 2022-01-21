import json, pickle, pdb
from parameteres import Biencoder_params
from convert_cantemist import fileBC5CDR

class CandidateReaderForTestDataset:
    def __init__(self, config):
        self.config = config
        self.mention2candidate_duis = self._dui2candidate_duis_returner()

    def _dui2candidate_duis_returner(self):
        with open(self.config.candidates_dataset, 'rb') as f:
            c = pickle.load(f)

        if str(self.config.candidates_dataset).find('ecie03') != -1:
            mention_list = []
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
        mention2candidate_duis = {}
        for mention, its_candidates in zip(c['mentions'], c['candidates']):
            mention2candidate_duis.update({mention: [dui for (dui, prior) in its_candidates]})           

        return mention2candidate_duis
    

    def BC5CDRstats(self):
        with open('candidates.pkl', 'rb') as f:
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
        acc_200 = 0
        total = 0
        for mention, its_candidates in zip(c['mentions'], c['candidates']):
            for text, code in annotators:
                control = False
                if mention.lower() == text.lower():
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
                            acc_200 += 1
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