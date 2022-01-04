import json, pickle, pdb
from parameteres import Biencoder_params

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
        mention2candidate_duis = {}
        for mention, its_candidates in zip(c['mentions'], c['candidates']):
            mention2candidate_duis.update({mention: [dui for (dui, prior) in its_candidates]})
            
        return mention2candidate_duis

if __name__ == '__main__':
    config = Biencoder_params()
    params = config.opts
    cg = CandidateReaderForTestDataset(config=params)
    cg._dui2candidate_duis_returner()