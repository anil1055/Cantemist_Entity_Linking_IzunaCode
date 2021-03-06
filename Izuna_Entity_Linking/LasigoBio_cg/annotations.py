import os
import xml.etree.ElementTree as ET
import sys

sys.path.append("./")


def parse_ner_output(ic=False):
    """Get the annotations in the NER output files (ic=False) or in the CANTEMIST dataset (ic=True)."""

    filenames = list()
    evaluation = False

    if ic:
        filenames_1 = ["./dataset/cantemist/train/"+input_file for input_file in os.listdir("./dataset/cantemist/train/") if input_file[-3:] == "ann"]
        filenames_2 = ["./dataset/cantemist/dev1/"+input_file for input_file in os.listdir("./dataset/cantemist/dev1/") if input_file[-3:] == "ann"]
        filenames_3 = ["./dataset/cantemist/dev2/"+input_file for input_file in os.listdir("./dataset/cantemist/dev2/") if input_file[-3:] == "ann"]
        filenames_4 = ["./dataset/cantemist/test/"+input_file for input_file in os.listdir("./dataset/cantemist/test/") if input_file[-3:] == "ann"]
        filenames =  filenames_1 + filenames_2 + filenames_3 + filenames_4

    else:
        filenames = ["./evaluation/NER/"+ input_file for input_file in os.listdir("./evaluation/NER/")]
        evaluation = True
    
    annotations = dict()
    

    for filename in filenames:
        
        with open(filename , 'r', encoding='utf-8') as doc_file:
            ner_output = doc_file.readlines()
            doc_file.close()

            doc_name = str()
                
            if evaluation:
                doc_name = filename.split("evaluation/NER/")[1]
            else:
                doc_name = filename.split("/")[4]
                
            for annotation in ner_output:
                line_data = annotation.split("\t")
                    
                if len(line_data) == 3:
                        
                    if ic: # The annotation ID is needed to further calculation of the information content
                        
                        if line_data[0][0] == "#":
                            annotation_id = line_data[2].strip("\n")
                            
                            if doc_name in annotations.keys():
                                current_values = annotations[doc_name]
                                current_values.append(annotation_id)
                                annotations[doc_name] = current_values
                                            
                            else:
                                annotations[doc_name] = [annotation_id]

                        else: # The annotation text is needed for candidate retrieval
                            #if doc_name == "S1130-01082005001000015-1.ann":
                                annotation_text = line_data[2].strip("\n")
                                term_number = line_data[0]
                                annotation_type = line_data[1].split(" ")[0]
                                annotation_begin = line_data[1].split(" ")[1]
                                annotation_end = line_data[1].split(" ")[2]
                                annotation_data = (annotation_text, term_number, annotation_type, annotation_begin, annotation_end)

                                if doc_name in annotations.keys():
                                    current_values = annotations[doc_name]
                                    current_values.append(annotation_data)
                                    annotations[doc_name] = current_values
                                                
                                else:
                                    annotations[doc_name] = [annotation_data]
                
    return annotations






