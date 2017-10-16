import re
from nltk import ne_chunk, pos_tag, tree, word_tokenize

named_entity_excludes = set([
    'united states',
    'state',
    'states',
    'investigation',
    'washington',
    'congress',
    'd.c.',
    'u.s.',
    'integrity',
    'commission',
    'federal',
    'office',
    'chair',
    'audit',
    'compliance',
    'agency',
    'inspection',
    'summary',
    'general',
    'report',
    'review',
    'government',
    'act',
    'table',
    'department',
    'county',
    'bureau',
    'section',
    'no',
    'oversight',
    'mr.',
    'committee',
    'subcommittee',
    'chairman',
    'independent audit',
    'director',
    'administration',
    'headquarters',
    'guidance',
    'subject',
    'case number',
    'treasurer',
    'treasury',
    'management',
    'chart',
    'oig',
    'fy',
    'cfo',
    'ceo',
    'inc.',
    'comments',
    'number',
    'grantee',
    'program',
    'programs',
    'serious',
    'board',
    'survey',
    'gao',
    'council',
    'administrative',
    'corporation',
    'more',
    'departmental',
    'total'
    ])

named_entity_substring_excludes = [
    'inspector general',
    'oig',
    'audit',
    'inspectors general',
    'inspector\'s general',
    'criminal investigation',
    'criminal investigations',
    'semiannual',
    'office of inspector',
    'date',
    ' ’',
    'schedule',
    'fy',
    'year',
    'month',
    'page',
    'appendix',
    'attachment'
]

category_excludes = set(['tim'])

def is_acronym(word):
    return re.match('[A-Z][A-Z]+$', word)

def check_substrings(ne_str):
    for substr in named_entity_substring_excludes:
        if substr in ne_str:
            return True
    return False

def filter_named_entity(ne):
    ne_str = ' '.join([leaf[0] for leaf in ne.leaves()]).lower()
    return (
        len(ne_str) <= 1
        or (is_acronym(ne[0][0]) and len(ne_str) <= 2)
        or ne_str in named_entity_excludes # Full string match named_entity_excludes
        or ne.label() in category_excludes
        or check_substrings(ne_str))


def get_named_entities(doc_text):
    tokens = word_tokenize(doc_text)
    pos_tagged = pos_tag(tokens)
    nes = ne_chunk(pos_tagged, binary=False)

    return (' '.join(leaf[0] for leaf in x.leaves())
            for x in nes if isinstance(x, tree.Tree) and not filter_named_entity(x))