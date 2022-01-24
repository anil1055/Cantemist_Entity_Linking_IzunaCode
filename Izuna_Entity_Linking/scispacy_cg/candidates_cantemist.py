from builtins import property as _property, tuple as _tuple
from operator import itemgetter as _itemgetter
from collections import OrderedDict
import json

class Entity(tuple):
    'Entity(concept_id, canonical_name, aliases, types, definition)'

    __slots__ = ()

    _fields = ('concept_id', 'canonical_name', 'aliases', 'types', 'definition')

    def __new__(_cls, concept_id, canonical_name, aliases, types, definition):
        'Create new instance of Entity(concept_id, canonical_name, aliases, types, definition)'
        return _tuple.__new__(_cls, (concept_id, canonical_name, aliases, types, definition))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new Entity object from a sequence or iterable'
        result = new(cls, iterable)
        if len(result) != 5:
            raise TypeError('Expected 5 arguments, got %d' % len(result))
        return result

    def _replace(_self, **kwds):
        'Return a new Entity object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, ('concept_id', 'canonical_name', 'aliases', 'types', 'definition'), _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % list(kwds))
        return result

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(concept_id=%r, canonical_name=%r, aliases=%r, types=%r, definition=%r)' % self

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values.'
        return OrderedDict(zip(self._fields, self))

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    concept_id = _property(_itemgetter(0), doc='Alias for field number 0')
    canonical_name = _property(_itemgetter(1), doc='Alias for field number 1')
    aliases = _property(_itemgetter(2), doc='Alias for field number 2')
    types = _property(_itemgetter(3), doc='Alias for field number 3')
    definition = _property(_itemgetter(4), doc='Alias for field number 4')

class cante:
  def __init__(self, alias_to_cuis, cui_to_entity):
    self.alias_to_cuis = alias_to_cuis
    self.cui_to_entity = cui_to_entity

def createCandidateCantemist():
    cieo_PATH = './cieo/cie_o3.jsonl'
    concepts = list()
    alias_to_cuis = {}
    cui_to_entity = {}
    aliases = '['
    with open(cieo_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            dui_one = json.loads(line.strip())
            # dict_keys(['concept_id', 'aliases', 'canonical_name', 'definition'])
            concepts.append(dui_one)
            for alias in dui_one['aliases']:
                alias_to_cuis[str(alias)] = str(dui_one['concept_id'])
                aliases += '"' + alias + '",'
            cui_to_entity[str(dui_one['concept_id'])] = Entity(str(dui_one['concept_id']),str(dui_one['aliases']),str(dui_one['canonical_name']),[],str(dui_one['definition']))
        with open('concept_aliases.json', 'w', encoding='utf-8') as dui2idx_f:
            json.dump(aliases[:-1] + ']', dui2idx_f)
    
    kb = cante(alias_to_cuis, cui_to_entity)
    return kb


