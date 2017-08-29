#!/usr/bin/env python3
"""
Consume files from https://archive.org/details/us-inspectors-general.bulk and save as AuditDocuments

This is slow since it goes over HTTP and invokes the web server.
Consider using my_site_django/upload_audit_docs.py to populate the database locally

Create a file pointing to .json text paths
'find <absolute base url such as /home/user/us-inspectors-general.bulk> -name *report.json > reports.txt'
Then feed that file to this script
'./upload_audit_docs_rest.py reports.txt'
"""
import fileinput, json, os, requests

for path in fileinput.input():
    meta_path = path.strip('\n')

    if not os.path.exists(meta_path):
        print('Input path ' + meta_path + ' not found - Skipping')
        continue

    with open(meta_path) as meta_file:
        meta = json.loads(meta_file.read())

        doc = {
            "publication_date": meta['published_on'] + "T00:00",
            "title": meta['title'],
            "source": "AO",
            "external_identifier": meta['report_id'],
        }

        text_path = meta_path.replace('report.json', 'report.txt')
        if os.path.exists(text_path):
            with open(text_path) as text_file:
                doc['text'] = text_file.read()
        else:
            print('No file for entry ' + text_path)

        post_response = requests.post("http://localhost:8000/audits/", data=doc)

        if post_response.status_code == 201:
            print('Created entry for ' + meta_path)
        else:
            print('Failed entry ' + meta_path + ' ' + post_response.text)