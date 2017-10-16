#!/usr/bin/env python3
"""
Quickly Consume files from https://archive.org/details/us-inspectors-general.bulk and save as AuditDocuments

Create a file pointing to .json text paths
'find <absolute base url such as /home/user/us-inspectors-general.bulk> -name *report.json > reports.txt'
Then feed that file to this script
'./upload_audit_docs.py reports.txt'
"""
import os, django, fileinput, json
from government_audit_mining.audit_miner import get_named_entities
from nltk.probability import FreqDist


if __name__ == "__main__":
    # enter django shell
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site_django.settings")
    django.setup()

    from government_audit.models import AuditDocument, NamedEntity

    existing_titles = set([record[0] for record in AuditDocument.objects.values_list('title')])

    for i, path in enumerate(fileinput.input()):
        print('\n', i, path)
        meta_path = path.strip('\n')

        if not os.path.exists(meta_path):
            print('Input path ' + meta_path + ' not found - Skipping')
            continue

        with open(meta_path) as meta_file:
            meta = json.loads(meta_file.read())

            if not meta['url']:
                print(f'Skipping {meta["title"]} as url is null')
                continue

            if meta['title'] in existing_titles:
                print('Skipping as title exists in DB ' + meta['title'])
                continue

            doc = AuditDocument()
            doc.title = meta['title']
            doc.publication_date = meta['published_on']
            doc.source = 'AO'
            doc.url = meta['url']

            text_path = meta_path.replace('report.json', 'report.txt')
            text = None
            if os.path.exists(text_path):
                with open(text_path) as text_file:
                    text = text_file.read()
            else:
                print('No file for entry ' + text_path + ' skipping file')
                continue

            doc.text = text # doc.text is cleared after save, keeping text around for analysis
            try:
                doc.save()
                print("Saved " + meta_path)
            except BaseException as e:
                print("Failed to save " + meta_path + " : " + str(e))

            # Data mine the doc
            ne_fdist = FreqDist(ne for ne in get_named_entities(text))
            for ne in ne_fdist.most_common():
                if ne[1] < 3:
                    break
                named_entity = NamedEntity()
                named_entity.document = doc
                named_entity.name = ne[0]
                named_entity.frequency = ne[1]

                try:
                    named_entity.save()
                    print("Saved named entity ", named_entity.name, named_entity.frequency)
                except BaseException as e:
                    print("Failed to save named entity " + named_entity.name + " : " + str(e))
