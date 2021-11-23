import transformers
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer, PretrainedTransformerIndexer
import os
from transformers import AutoTokenizer, AutoModel
import urllib.request
from parameteres import Biencoder_params
from commons import MENTION_START_TOKEN, MENTION_END_TOKEN

class CustomTokenizer:
    def __init__(self, config):
        self.config = config
        self.bert_model_and_vocab_downloader()
        self.bert_tokenizer = self.bert_tokenizer_returner()

    def huggingfacename_returner(self):
        'Return huggingface modelname and do_lower_case parameter'
        if self.config.bert_name == 'bert-base-uncased':
            return 'bert-base-uncased', True
        elif self.config.bert_name == 'biobert':
            # https://huggingface.co/monologg/biobert_v1.1_pubmed/tree/main
            return './biobert/', False
        elif self.config.bert_name == 'roberta-base-biomedical-es':
            return '.roberta-base-biomedical-es/'
        elif self.config.bert_name == 'roberta-base-biomedical-clinical-es':
            return '.roberta-base-biomedical-clinical-es/'
        elif self.config.bert_name == 'bio_bert_base_spanish_wwm_uncased':
            return '.bio_bert_base_spanish_wwm_uncased/'
        else:
            print('Currently', self.config.bert_name, 'are not supported.')
            exit()

    def token_indexer_returner(self):
        huggingface_name, do_lower_case = self.huggingfacename_returner()
        return {'tokens': PretrainedTransformerIndexer(
            model_name=huggingface_name,
            # do_lowercase=do_lower_case
        )
        }

    def bert_tokenizer_returner(self):
        if self.config.bert_name == 'bert-base-uncased':
            vocab_file = './vocab_file/bert-base-uncased-vocab.txt'
            do_lower_case = True
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_lower_case=do_lower_case,
                                              do_basic_tokenize=True,
                                              never_split=['<target>', '</target>'])
        elif self.config.bert_name == 'biobert':
            vocab_file = './vocab_file/biobert_v1.1_pubmed_vocab.txt'
            do_lower_case = False
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_lower_case=do_lower_case,
                                              do_basic_tokenize=True,
                                              never_split=['<target>', '</target>'])
        elif self.config.bert_name == 'roberta-base-biomedical-es':
            vocab_file = './vocab_file/roberta-base-biomedical-es.json'
            do_lower_case = False
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_lower_case=do_lower_case,
                                              do_basic_tokenize=True,
                                              never_split=['<objetivo>', '</objetivo>'])
        elif self.config.bert_name == 'roberta-base-biomedical-clinical-es':
            vocab_file = './vocab_file/roberta-base-biomedical-clinical-es.json'
            do_lower_case = False
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_lower_case=do_lower_case,
                                              do_basic_tokenize=True,
                                              never_split=['<objetivo>', '</objetivo>'])
        elif self.config.bert_name == 'bio_bert_base_spanish_wwm_uncased':
            vocab_file = './vocab_file/bio_bert_base_spanish_wwm_uncased.txt'
            do_lower_case = False
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_lower_case=do_lower_case,
                                              do_basic_tokenize=True,
                                              never_split=['<objetivo>', '</objetivo>'])
        else:
            print('currently not supported:', self.config.bert_name)
            raise NotImplementedError


    def tokenize(self, txt):
        target_anchors = ['<target>', '</target>']
        original_tokens = txt.split(' ')
        new_tokens = list()

        for token in original_tokens:
            if token in target_anchors:
                if token == '<target>':
                    new_tokens.append(MENTION_START_TOKEN)
                if token == '</target>':
                    new_tokens.append(MENTION_END_TOKEN)
                continue
            else:
                split_to_subwords = self.bert_tokenizer.tokenize(token)  # token is oneword, split_tokens
                if ['[CLS]'] in split_to_subwords:
                    split_to_subwords.remove('[CLS]')
                if ['[SEP]'] in split_to_subwords:
                    split_to_subwords.remove('[SEP]')
                if split_to_subwords == []:
                    new_tokens.append('[UNK]')
                else:
                    new_tokens += split_to_subwords

        return new_tokens

    def tokenize_es(self, txt):
        target_anchors = ['<objetivo>', '</objetivo>']
        original_tokens = txt.split(' ')
        new_tokens = list()

        for token in original_tokens:
            if token in target_anchors:
                if token == '<objetivo>':
                    new_tokens.append(MENTION_START_TOKEN)
                if token == '</objetivo>':
                    new_tokens.append(MENTION_END_TOKEN)
                continue
            else:
                split_to_subwords = self.bert_tokenizer.tokenize(token)  # token is oneword, split_tokens
                if ['[CLS]'] in split_to_subwords:
                    split_to_subwords.remove('[CLS]')
                if ['[SEP]'] in split_to_subwords:
                    split_to_subwords.remove('[SEP]')
                if split_to_subwords == []:
                    new_tokens.append('[UNK]')
                else:
                    new_tokens += split_to_subwords

        return new_tokens


    def bert_model_and_vocab_downloader(self):
        if self.config.bert_name == 'biobert':
            if not os.path.exists('./biobert/'):
                os.mkdir('./biobert/')
                print('=== Downloading biobert ===')
                urllib.request.urlretrieve("https://huggingface.co/monologg/biobert_v1.0_pubmed_pmc/blob/main/config.json", './biobert/config.json')
                urllib.request.urlretrieve("https://huggingface.co/monologg/biobert_v1.0_pubmed_pmc/blob/main/pytorch_model.bin", './biobert/pytorch_model.bin')
                urllib.request.urlretrieve("https://huggingface.co/monologg/biobert_v1.0_pubmed_pmc/blob/main/special_tokens_map.json", './biobert/special_tokens_map.json')
                urllib.request.urlretrieve("https://huggingface.co/monologg/biobert_v1.0_pubmed_pmc/blob/main/tokenizer_config.json", './biobert/tokenizer_config.json')

        if self.config.bert_name == 'roberta-base-biomedical-es':
            if not os.path.exists('./roberta-base-biomedical-es/'):
                os.mkdir('./roberta-base-biomedical-es/')
                print('=== Downloading roberta-base-biomedical-es ===')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/config.json", './roberta-base-biomedical-es/config.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/pytorch_model.bin", './roberta-base-biomedical-es/pytorch_model.bin')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/special_tokens_map.json", './roberta-base-biomedical-es/special_tokens_map.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/tokenizer_config.json", './roberta-base-biomedical-es/tokenizer_config.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/dict.txt", './roberta-base-biomedical-es/dict.txt')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/merges.txt", './roberta-base-biomedical-es/merges.txt')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/args.json", './roberta-base-biomedical-es/args.json')
        
        if self.config.bert_name == 'roberta-base-biomedical-clinical-es':
            if not os.path.exists('./roberta-base-biomedical-clinical-es/'):
                os.mkdir('./roberta-base-biomedical-clinical-es/')
                print('=== Downloading roberta-base-biomedical-clinical-es ===')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/config.json", './roberta-base-biomedical-clinical-es/config.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/pytorch_model.bin", './roberta-base-biomedical-clinical-es/pytorch_model.bin')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/special_tokens_map.json", './roberta-base-biomedical-clinical-es/special_tokens_map.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/main/tokenizer_config.json", './roberta-base-biomedical-clinical-es/tokenizer_config.json')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/dict.txt", './roberta-base-biomedical-clinical-es/dict.txt')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/main/merges.txt", './roberta-base-biomedical-clinical-es/merges.txt')
                urllib.request.urlretrieve("https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/args.json", './roberta-base-biomedical-clinical-es/args.json')

        if self.config.bert_name == 'bio-bert-base-spanish-wwm-uncased':
            if not os.path.exists('./bio-bert-base-spanish-wwm-uncased/'):
                os.mkdir('./bio-bert-base-spanish-wwm-uncased/')
                print('=== Downloading bio-bert-base-spanish-wwm-uncased ===')
                urllib.request.urlretrieve("https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/config.json", './bio-bert-base-spanish-wwm-uncased/config.json')
                urllib.request.urlretrieve("https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/pytorch_model.bin", './bio-bert-base-spanish-wwm-uncased/pytorch_model.bin')
                urllib.request.urlretrieve("https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/special_tokens_map.json", './bio-bert-base-spanish-wwm-uncased/special_tokens_map.json')
                urllib.request.urlretrieve("https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/tokenizer_config.json", './bio-bert-base-spanish-wwm-uncased/tokenizer_config.json')
                urllib.request.urlretrieve("https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/tokenizer.json", './bio-bert-base-spanish-wwm-uncased/tokenizer.json')
                
        if not os.path.exists('./vocab_file/'):
            os.mkdir('./vocab_file/')

        bert_base_uncased_vocab_url = "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-uncased-vocab.txt"
        bibobert_vocab_url = "https://huggingface.co/monologg/biobert_v1.1_pubmed/blob/main/vocab.txt"
        roberta_base_biomedical_es_vocab_url = "https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-es/blob/main/vocab.json"
        bio_bert_base_spanish_wwm_uncased_vocab_url = "https://huggingface.co/fvillena/bio-bert-base-spanish-wwm-uncased/blob/main/vocab.txt"
        roberta_base_biomedical_clinical_es_vocab_url = "https://huggingface.co/PlanTL-GOB-ES/roberta-base-biomedical-clinical-es/blob/main/vocab.json"
        
        urllib.request.urlretrieve(bert_base_uncased_vocab_url, './vocab_file/bert-base-uncased-vocab.txt')
        urllib.request.urlretrieve(bibobert_vocab_url, './vocab_file/biobert_v1.1_pubmed_vocab.txt')
        urllib.request.urlretrieve(roberta_base_biomedical_es_vocab_url, './vocab_file/roberta-base-biomedical-es_vocab.json')
        urllib.request.urlretrieve(bio_bert_base_spanish_wwm_uncased_vocab_url, './vocab_file/bio-bert-base-spanish-wwm-uncased_vocab.txt')
        urllib.request.urlretrieve(roberta_base_biomedical_clinical_es_vocab_url, './vocab_file/roberta-base-biomedical-clinical-es_vocab.json')

if __name__ == '__main__':
    config = Biencoder_params()
    params = config.opts
    tokenizer = CustomTokenizer(config=params)