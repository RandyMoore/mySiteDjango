import django
from django.db import transaction
import aiohttp
import asyncio
import os
import random
import re

domains_to_ignore = set()
domains_record = {}


async def check_url(doc, session):
    print('Checking ', doc['url'])
    domain = doc['domain']
    if domain not in domains_record:
        domains_record[domain] = [0, 0]

    try:
        async with session.head(doc['url'], allow_redirects=True, timeout=5) as url_head_response:
            url_active = url_head_response.status == 200
            doc['url_active'] = url_active
            if url_active:
                doc['url'] = url_head_response.url

    except (asyncio.TimeoutError, aiohttp.client_exceptions.ClientConnectorError) as e:
        print(f"Received exception for {doc['url']}")
        domains_to_ignore.add(domain)
        domains_record[domain][0] += 1

    domains_record[domain][1] += 1

    return doc # doc without updates returned in case of exception


async def update_doc_url_stati():
    from government_audit.models import AuditDocument
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    docs_by_domain = {}
    for audit_doc in AuditDocument.objects.filter(url_active__isnull=True).values('id', 'url', 'url_active'):
        domain = re.search('^https?://(?:www\.)?([^/^?]+)', audit_doc['url']).group(1)
        audit_doc['domain'] = domain
        if domain in docs_by_domain:
            docs_by_domain[domain].append(audit_doc)
        else:
            docs_by_domain[domain] = [audit_doc]

    while True:
        docs_to_fetch = [doc_list.pop() for doc_list in docs_by_domain.values() if doc_list]
        if not docs_to_fetch:
            print("no more urls to check")
            break

        print("Fetching ", len(docs_to_fetch), " urls")

        domains_to_restore = set()
        for domain in domains_to_ignore:
            print("Considering domain ", domain, " with record ", domains_record[domain])
            if random.randint(0, domains_record[domain][1] + 1) > domains_record[domain][0]:
                domains_to_restore.add(domain)
        print("Restoring domains ", domains_to_restore)
        domains_to_ignore.difference_update(domains_to_restore)
        print(f"Ignoring {str(domains_to_ignore)}")

        checked_urls = await asyncio.gather(*[check_url(doc, session) for doc in docs_to_fetch if doc['domain'] not in domains_to_ignore])

        with transaction.atomic():
            for doc in checked_urls:
                if 'url_active' in doc:
                    AuditDocument.objects.filter(id=doc['id']).update(url_active=doc['url_active'],
                                                                      url=doc['url'])
        await asyncio.sleep(1)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site_django.settings")
    django.setup()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(update_doc_url_stati())
