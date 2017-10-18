#!/usr/bin/env python3
"""
Quickly Consume files from https://archive.org/details/us-inspectors-general.bulk and save as AuditDocuments

Create a file pointing to .json text paths
'find <absolute base url such as /home/user/us-inspectors-general.bulk> -name *report.json > reports.txt'
Then feed that file to this script
'./upload_audit_docs.py reports.txt'
"""
from multiprocessing import Pool

import django
import fnmatch
import json
import multiprocessing
import os
import sys
from django.db import transaction
from government_audit_mining.audit_miner import get_named_entities
from nltk.probability import FreqDist

corpus_root = None
db_queue = None
META_FILE_NAME = 'report.json'
TEXT_FILE_NAME = 'report.txt'


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def save_to_db():
    global db_queue
    while True:
        doc_tuple = db_queue.get()

        if not doc_tuple:
            print("DB found None, exiting")
            return

        doc, named_entities = doc_tuple
        print('DB saving', doc.title)

        try:
            doc.save()
            with transaction.atomic():
                for entity in named_entities:
                    entity.document = doc
                    entity.save()
        except BaseException as e:
            print('Failed to save to DB', str(e))


def process_documents(meta_path):
    global corpus_root, db_queue
    print('Process', meta_path)

    if not os.path.exists(meta_path):
        print('Input path ' + meta_path + ' not found - Skipping')
        return

    with open(meta_path) as meta_file:
        meta = json.loads(meta_file.read())

        if not 'url' in meta or not meta['url']:
            print(f'Skipping {meta["title"]} as url is null')
            return

        doc = AuditDocument()
        doc.title = meta['title']
        doc.publication_date = meta['published_on']
        doc.source = 'AO'
        doc.url = meta['url']
        doc.path = str(meta_path)[len(corpus_root)+1:-len(META_FILE_NAME)-1]

        text_path = meta_path.replace(META_FILE_NAME, TEXT_FILE_NAME)

        if os.path.exists(text_path):
            with open(text_path) as text_file:
                doc.text = text_file.read()
        else:
            print('No file for entry ' + text_path + ' skipping file')
            return

        # Data mine the doc
        ne_fdist = FreqDist(ne for ne in get_named_entities(doc.text))
        named_entities = []
        for ne in ne_fdist.most_common():
            if ne[1] < 3:
                break
            named_entity = NamedEntity()
            named_entity.name = ne[0]
            named_entity.frequency = ne[1]
            named_entities.append(named_entity)

        db_queue.put((doc, named_entities))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site_django.settings")
    django.setup()

    from government_audit.models import AuditDocument, NamedEntity

    existing_paths = set([record[0] for record in AuditDocument.objects.values_list('path')])
    db_queue = multiprocessing.Manager().Queue()

    corpus_root = sys.argv[1]
    files = []
    for f in find(META_FILE_NAME, corpus_root):
        if str(f)[len(corpus_root)+1:-len(META_FILE_NAME)-1] not in existing_paths:
           files.append(f)
        else:
            print(f, 'already in DB, skipping.')

    multiprocessing.Process(target=save_to_db).start()

    with multiprocessing.Pool() as p: # by default creates as many processes as available cores.
        p.map(func=process_documents, iterable=files)

    db_queue.put(None)