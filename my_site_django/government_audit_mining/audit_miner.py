import os, re
from nltk import ne_chunk, pos_tag, tree, word_tokenize


def _load_text(local_file_name):
    module_loc = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(module_loc, local_file_name)) as file:
        return file.read().split('\n')


_named_entity_excludes = set(_load_text('named_entity_excludes.txt'))
_named_entity_substring_excludes = set(_load_text('named_entity_substring_excludes.txt'))


def _is_acronym(word):
    return re.match('[A-Z][A-Z]+$', word)


def _check_substrings(ne_str):
    for substr in _named_entity_substring_excludes:
        if substr in ne_str:
            return True
    return False


def _filter_named_entity(ne):
    ne_str = ' '.join([leaf[0] for leaf in ne.leaves()]).lower()
    return (
        len(ne_str) <= 1
        or (_is_acronym(ne[0][0]) and len(ne_str) <= 2)
        or ne_str in _named_entity_excludes
        or _check_substrings(ne_str))


def get_named_entities(doc_text):
    tokens = word_tokenize(doc_text)
    pos_tagged = pos_tag(tokens)
    nes = ne_chunk(pos_tagged, binary=False)

    return (' '.join(leaf[0] for leaf in x.leaves())
            for x in nes if isinstance(x, tree.Tree) and not _filter_named_entity(x))