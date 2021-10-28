import copy

DATASET_DIRPATH='./dataset/'
Cantemist_FILE_PREFIX='cc_onco_'
Cantemist_FILE_SUFFIX='.PubTator.txt'

#corpus_pubtator_pmids_trng.txt
from_cantemist_2_common = {
    "dev1": "dev1",
    "dev2": "dev2",
    "test": "test",
    "train": "trng"
}
PMID_FILE_PREFIX='corpus_pubtator_pmids_'
PMID_FILE_SUFFIX='.txt'

def trn_dev_test_pmidsets_maker():
    all_pmids = []
    for cantemist_file, pmid_file_symbol in from_cantemist_2_common.items():
        source_file = DATASET_DIRPATH + Cantemist_FILE_PREFIX + cantemist_file + Cantemist_FILE_SUFFIX
        dest_file = DATASET_DIRPATH + PMID_FILE_PREFIX + pmid_file_symbol + PMID_FILE_SUFFIX

        pmids = []
        with open(source_file, 'r', encoding="utf8") as f:
            for line in f:
                if '|t|' in line:
                    l = line.strip().split('|')
                    pmid = l[0]
                    pmids.append(pmid)
                    all_pmids.append(pmid)

        with open(dest_file, 'w', encoding="utf8") as g:
            for idx, pmid in enumerate(pmids):
                if idx != len(pmids) -1:
                    g.write(pmid+'\n')
                else:
                    g.write(pmid)

    with open(DATASET_DIRPATH + 'corpus_pubtator_pmids_all.txt', 'w', encoding="utf8") as h:
        for idx, pmid in enumerate(all_pmids):
            if idx != len(all_pmids) - 1:
                h.write(pmid + '\n')
            else:
                h.write(pmid)


def corpus_pubtator_maker():
    entire_file = ''
    one_title_and_abst = ''
    dest_file = DATASET_DIRPATH + 'corpus_pubtator.txt'

    for cantemist_file, pmid_file_symbol in from_cantemist_2_common.items():
        source_file = DATASET_DIRPATH + Cantemist_FILE_PREFIX + cantemist_file + Cantemist_FILE_SUFFIX

        with open(source_file, 'r', encoding="utf8") as f:
            tit_id = ''
            for line in f:
                if line.strip() == "":
                    entire_file += one_title_and_abst + '\n'
                    one_title_and_abst = copy.copy('')
                else:
                    if '|t|' in line:
                        one_title_and_abst += line
                        tit_id = line.split('|')[0]
                    else:
                        if line.find(tit_id) != -1:
                            if line.strip().split('\t')[5] == '-1':
                                continue
                            if len(line.strip().split('\t')[5].split('|')) != 1:
                                continue

                        one_title_and_abst += line

    with open(dest_file, 'w', encoding="utf8") as g:
        g.write(entire_file)


if __name__ == '__main__':
    trn_dev_test_pmidsets_maker()
    corpus_pubtator_maker()
