import json
import pdb
import os
cieo_PATH = './cieo/cie_o3.jsonl'
cieo_DIRPATH = './cieo/'

def cieo_loader():
    concepts = list()
    with open(cieo_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            dui_one_concept = json.loads(line.strip())
            # dict_keys(['concept_id', 'aliases', 'canonical_name', 'definition'])
            concepts.append(dui_one_concept)
    duis = [concept['concept_id'] for concept in concepts]

    dui2idx, idx2dui = {}, {}
    for idx, dui in enumerate(duis):
        dui2idx.update({dui: idx})
        idx2dui.update({idx: dui})

    dui2canonical, dui2definition = {}, {}
    for concept in concepts:
        dui2canonical.update({concept['concept_id']: concept['canonical_name']})
        if 'definition' in concept:
            dui2definition.update({concept['concept_id']: concept['definition']})
        else:
            dui2definition.update({concept['concept_id']: concept['canonical_name']})

    return dui2idx, idx2dui, dui2canonical, dui2definition

def kb_dumper():
    dui2idx, idx2dui, dui2canonical, dui2definition = cieo_loader()
    dui2idx_path = cieo_DIRPATH + 'dui2idx.json'
    idx2dui_path = cieo_DIRPATH + 'idx2dui.json'
    dui2canonical_path = cieo_DIRPATH + 'dui2canonical.json'
    dui2definition_path = cieo_DIRPATH + 'dui2definition.json'

    with open(dui2idx_path, 'w', encoding='utf-8') as dui2idx_f:
        json.dump(dui2idx, dui2idx_f, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))

    with open(idx2dui_path, 'w', encoding='utf-8') as idx2dui_f:
        json.dump(idx2dui, idx2dui_f, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))

    with open(dui2canonical_path, 'w', encoding='utf-8') as dui2canonical_f:
        json.dump(dui2canonical, dui2canonical_f, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))

    with open(dui2definition_path, 'w', encoding='utf-8') as dui2definition_f:
        json.dump(dui2definition, dui2definition_f, ensure_ascii=True, indent=4, sort_keys=False,
                  separators=(',', ': '))


if __name__ == '__main__':
    if not os.path.exists(cieo_DIRPATH):
        os.mkdir(cieo_DIRPATH)
    kb_dumper()
