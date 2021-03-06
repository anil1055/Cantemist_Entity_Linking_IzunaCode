'''
Seq2VecEncoders for encoding mentions and entities.
'''
import torch.nn as nn
from allennlp.modules.seq2vec_encoders import Seq2VecEncoder, PytorchSeq2VecWrapper, BagOfEmbeddingsEncoder
from allennlp.modules.seq2vec_encoders import BertPooler
from overrides import overrides
from allennlp.nn.util import get_text_field_mask

class Pooler_for_cano_and_def(Seq2VecEncoder):
    def __init__(self, args, word_embedder):
        super(Pooler_for_cano_and_def, self).__init__()
        self.args = args
        self.huggingface_nameloader()
        self.bertpooler_sec2vec = BertPooler(pretrained_model=self.bert_weight_filepath)
        self.word_embedder = word_embedder
        self.word_embedding_dropout = nn.Dropout(self.args.word_embedding_dropout)

    def huggingface_nameloader(self):
        if self.args.bert_name == 'bert-base-uncased':
            self.bert_weight_filepath = 'bert-base-uncased'
        elif self.args.bert_name == 'biobert':
            self.bert_weight_filepath = 'dmis-lab/biobert-base-cased-v1.2'
        elif self.args.bert_name == 'sapbert':
            self.bert_weight_filepath = 'cambridgeltl/SapBERT-from-PubMedBERT-fulltext'
        elif self.args.bert_name == 'roberta-base-biomedical-es':
            self.bert_weight_filepath = 'PlanTL-GOB-ES/roberta-base-biomedical-es'
        elif self.args.bert_name == 'roberta-base-biomedical-clinical-es':
            self.bert_weight_filepath =  'PlanTL-GOB-ES/roberta-base-biomedical-clinical-es'
        elif self.args.bert_name == 'bio-bert-base-spanish-wwm-uncased':
            self.bert_weight_filepath =  'fvillena/bio-bert-base-spanish-wwm-uncased'
        else:
            self.bert_weight_filepath = 'dummy'
            print('Currently not supported', self.args.bert_name)
            exit()

    def forward(self, cano_and_def_concatnated_text):
        mask_sent = get_text_field_mask(cano_and_def_concatnated_text)
        entity_emb = self.word_embedder(cano_and_def_concatnated_text)
        entity_emb = self.word_embedding_dropout(entity_emb)
        entity_emb = self.bertpooler_sec2vec(entity_emb, mask_sent)

        return entity_emb


class Pooler_for_mention(Seq2VecEncoder):
    def __init__(self, args, word_embedder):
        super(Pooler_for_mention, self).__init__()
        self.args = args
        self.huggingface_nameloader()
        self.bertpooler_sec2vec = BertPooler(pretrained_model=self.bert_weight_filepath)
        self.word_embedder = word_embedder
        self.word_embedding_dropout = nn.Dropout(self.args.word_embedding_dropout)

    def huggingface_nameloader(self):
        if self.args.bert_name == 'bert-base-uncased':
            self.bert_weight_filepath = 'bert-base-uncased'
        elif self.args.bert_name == 'biobert':
            self.bert_weight_filepath = 'dmis-lab/biobert-base-cased-v1.2'
        elif self.args.bert_name == 'sapbert':
            self.bert_weight_filepath = 'cambridgeltl/SapBERT-from-PubMedBERT-fulltext'
        elif self.args.bert_name == 'roberta-base-biomedical-es':
            self.bert_weight_filepath = 'PlanTL-GOB-ES/roberta-base-biomedical-es'
        elif self.args.bert_name == 'roberta-base-biomedical-clinical-es':
            self.bert_weight_filepath =  'PlanTL-GOB-ES/roberta-base-biomedical-clinical-es'
        elif self.args.bert_name == 'bio-bert-base-spanish-wwm-uncased':
            self.bert_weight_filepath =  'fvillena/bio-bert-base-spanish-wwm-uncased'
        else:
            self.bert_weight_filepath = 'dummy'
            print('Currently not supported', self.args.bert_name)
            exit()

    def forward(self, contextualized_mention):
        mask_sent = get_text_field_mask(contextualized_mention)
        mention_emb = self.word_embedder(contextualized_mention)
        mention_emb = self.word_embedding_dropout(mention_emb)
        mention_emb = self.bertpooler_sec2vec(mention_emb, mask_sent)

        return mention_emb

    @overrides
    def get_output_dim(self):
        return 768
