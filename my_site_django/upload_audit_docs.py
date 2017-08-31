#!/usr/bin/env python3
"""
Quickly Consume files from https://archive.org/details/us-inspectors-general.bulk and save as AuditDocuments

Create a file pointing to .json text paths
'find <absolute base url such as /home/user/us-inspectors-general.bulk> -name *report.json > reports.txt'
Then feed that file to this script
'./upload_audit_docs.py reports.txt'
"""
import os, django, fileinput, json

if __name__ == "__main__":
    # enter django shell
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site_django.settings")
    django.setup()

    from government_audit.models import AuditDocument
    from django.db import connection

    existing_titles = set([x[0] for x in AuditDocument.objects.values_list('title')])

    for path in fileinput.input():
        meta_path = path.strip('\n')

        if not os.path.exists(meta_path):
            print('Input path ' + meta_path + ' not found - Skipping')
            continue

        with open(meta_path) as meta_file:
            meta = json.loads(meta_file.read())

            if meta['title'] in existing_titles:
                print('Skipping as title exists in DB ' + meta['title'])
                continue

            doc = AuditDocument()
            doc.title = meta['title']
            doc.publication_date = meta['published_on']
            doc.source = 'AO'
            doc.external_identifier = meta['report_id']

            text_path = meta_path.replace('report.json', 'report.txt')
            if os.path.exists(text_path):
                with open(text_path) as text_file:
                    doc.text = text_file.read()
            else:
                print('No file for entry ' + text_path)

            try:
                doc.save()
                print("Saved " + meta_path)
            except BaseException as e:
                print("Failed to save " + meta_path + " : " + str(e))

    with connection.cursor() as cursor:
        cursor.execute("DROP INDEX IF EXISTS textsearch_idx")
        cursor.execute("CREATE INDEX textsearch_idx ON government_audit_auditdocument USING GIN(lexemes)")
