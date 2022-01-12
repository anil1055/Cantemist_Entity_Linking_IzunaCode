
def readFile(fileName, choice = True):       
    file = open(fileName, encoding='utf-8') #, 'rb', , encoding='utf-8'
    if choice:        
        file_ = []
        lines = file.readlines()         
        for line in lines:
            file_.append(str(line).rstrip("\n"))
        file.close()
        return file_
    else:
        text = file.read()
        file.close()
        return text

from xml.etree import ElementTree
from xml.dom import minidom
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    #rough_string = rough_string.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
def GenerateXML(fileName, annotators):
      
    root = Element("collection")

    b1 = SubElement(root, "source")  
    b1.text = 'PubTator'
    b2 = SubElement(root, "date")  
    b2.text = '0/0/0'
    b3 = SubElement(root, "key")  
    b3.text = 'PubTator.key'

    for annotator in annotators:
        doc = SubElement(root ,"document")
        id = SubElement(doc, "id")  
        id.text = str(annotator[1])
        passage = SubElement(doc, "passage")  
        infon = SubElement(passage, "infon") 
        infon.set('key', 'type')
        infon.text = 'text'
        offset = SubElement(passage, "offset")
        offset.text = '0'
        txt = SubElement(passage, "text")
        txt.text = str(annotator[0])

        ind = 0
        for annotation in annotator:
            if ind > 1:
                annot = SubElement(passage, "annotation")
                annot.set('id', str(annotation[0]))
                infon1 = SubElement(annot, "infon")
                infon1.set('key','type')
                infon1.text = str(annotation[2])
                infon2 = SubElement(annot, "infon")
                infon2.set('key','ICD-O-3')
                infon2.text = str(annotation[4])
                loc = SubElement(annot, "location", {'offset':str(annotation[3]), 'length':str(len(annotation[1]))})
                txt = SubElement(annot, "text")
                txt.text = str(annotation[1])
            ind += 1
    
    #root = prettify(root)
    import xml.etree.ElementTree as ET
    tree = ET.ElementTree(root)
    tree.write(fileName, xml_declaration=True, encoding='utf-8')


def GenerateTXT(fileName, annotators):
    fileTxt = ''
    for annotator in annotators:
        id = str(annotator[1])
        fileTxt += id + '|t|' + str(annotator[0]) + '\n'
        ind = 0
        for annotation in annotator:
            if ind > 1:
                lastIndex = int(annotation[3]) + int(len(str(annotation[1])))             
                fileTxt += id + '\t' + str(annotation[3]) + '\t' + str(lastIndex) + '\t' + str(annotation[1]) + '\t' + str(annotation[2]) + '\t' + str(annotation[4]) + '\n'
            ind += 1
        fileTxt += '\n'

    with open(fileName, 'w', encoding='utf-8') as file:
        file.write(fileTxt)


from sentence_splitter import SentenceSplitter, split_text_into_sentences
import spacy
nlp = spacy.load("es_core_news_sm")
def GenerateJSON(fileName, annotator):   
    import json
    idn = 1
    pubmed_id = str(annotator[1])
    text = str(annotator[0])
    splitter = SentenceSplitter(language='es')
    split_sentences = splitter.split(text)
    split_sentences = [content for content in split_sentences if not content in '']
    ind = 0
    entities = []
    lines = []
    lemma_lines = []
    for annotation in annotator:
        if ind > 1:
            off_set = int(annotation[3])
            off_loc = int(annotation[3]) + len(str(annotation[1]))
            txt = str(annotation[1])
            lemmas = []
            chrcter = []
            for sentences in split_sentences:
                if sentences.find(txt) != -1:
                    start = sentences.index(txt)
                    end = start + len(txt) + 1
                    if start == 0:
                        sentence = annotation[4] + '\t' + annotation[2] + '\t' + annotation[1] + '\t' + '<objetivo> ' + txt + ' </objetivo> ' + sentences[end:]
                    else:
                        sentence = annotation[4] + '\t' + annotation[2] + '\t' + annotation[1] + '\t' + sentences[0:start] + ' <objetivo> ' + txt + ' </objetivo> ' + sentences[end:]
                    rmv = str(sentence).rindex('\t')
                    just_sent = sentence[rmv+1:]
                    lines.append(sentence)
                    doc = nlp(just_sent)
                    lemma_sentence = ''                    
                    for token in doc:
                        lemma_sentence += token.lemma_ + ' '
                    lemma_sentence = lemma_sentence.replace('< objetivo >', '<objetivo>')
                    lemma_sentence = lemma_sentence.replace('< /objetivo >', '</objetivo>')
                    lemma_sentence = lemma_sentence.strip()
                    lemma_lines.append(annotation[4] + '\t' + annotation[2] + '\t' + annotation[1] + '\t' + lemma_sentence)
            entities.append([int(off_set), int(off_loc), str(txt), str(annotation[2]), str(annotation[4])])
        ind += 1

    data = {"lines_lemma": lemma_lines, "lines": lines, "if_txt_length_is_changed_flag": 0, "split_sentence": split_sentences, "entities": entities,
            "pubmed_id": pubmed_id, "text": text}

    with open('preprocessed_cantemist/' + pubmed_id + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file,indent = 4, sort_keys=True, ensure_ascii=False)

              

def fileProcess():
    filenames = ['train', 'dev1', 'dev2', 'test']
    for file in filenames:
        annotators = []
        for i in range(1, 1501):
            try:
                passage = readFile('dataset/cantemist/' + file + '/cc_onco' + str(i) + '.txt', False)
                linesAnn = readFile('dataset/cantemist/' + file + '/cc_onco' + str(i) + '.ann')
                annotator = []
                annotator.append(passage)
                annotator.append('onco' + str(i))
                for line in linesAnn:
                    infos = line.split('\t')
                    icd_code = ''
                    if str(infos[0]).find('T') != -1:
                        id = infos[0]
                        text = infos[len(infos)-1]
                        others = str(infos[1]).split(' ')
                        typeMed = others[0]
                        offset = others[1]
                    else:
                        icd_code = infos[len(infos)-1]
                    if icd_code != '':
                        annotator.append([id, text, typeMed, offset, icd_code])
                GenerateJSON('cc_onco_' + file + '.xml', annotator)
                annotators.append(annotator)                
            except Exception as e:
                print(str(e))
                continue
        #GenerateXML('cc_onco_' + file + '.xml', annotators)
        #GenerateTXT('cc_onco_' + file + '.txt', annotators)


def fileBC5CDR():
    filenames = ['corpus_pubtator']
    annotator = []
    for file in filenames:      
        try:
            passage = readFile('dataset/CDR.Corpus.v010516/' + file + '.txt')
            for line in passage:
                if line.find('|a|') == -1 and line.find('|t|') == -1 and line != '':
                    infos = line.split('\t')
                    icd_code = ''
                    text = infos[3]
                    code = infos[5]
                    annotator.append([text, code])               
        except Exception as e:
            print(str(e))
            continue
    return annotator

#fileProcess()