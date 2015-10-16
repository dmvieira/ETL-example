#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2

from modules.item_properties import get_attachment_or_description

url = (
    'http://www.grants.gov/grantsws/OppsSearch?jp={'
    '"rows":1000000,'
    '"searchOnly":true,'
    '"fundingInstruments":"G",'
    '"startRecordNum":0,'
    '"oppStatuses":"open"'
    '}'
)


f = urllib2.urlopen(url)
s = f.read()
f.close()

returned_data = json.loads(s)
links = []

n = 0

for item in returned_data['oppHits']:
    # log file
    n += 1
    with open("temp_grants_gov_g.log", "a") as log:
        log.write(
                "buscando %s (%d de %d)\n" %
                (str(item['id']), n, len(returned_data['oppHits']))
        )

    (text, uri) = get_attachment_or_description('http://www.grants.gov/grantsws/OppDetails?oppId=' + item['id'])
    if not text and not uri:
        print "*** Erro em", item['id']
        continue

    link = {
        'site': 'www.grants.gov',
        'kind': 'misturado',
        'name': '({number}) {title}'.format(**item),
        # 'uri': 'http://www.grants.gov/web/grants/view-opportunity.html?oppId=' + item['id']
        'uri': uri or 'http://www.grants.gov/web/grants/view-opportunity.html?oppId=' + item['id'],
        'text': text
    }

    links.append(link)
    # with open("temp_grants_gov_g.json", "a") as out:
    #     out.write(json.dumps(link)+"\n")


# Transform temp file into one complete json
# with open("temp_grants_gov_g.json", "r") as f_in:
#     temp_lines = f_in.read().split("\n")

# for line in temp_lines:
#     if line:
#         a = json.loads(line)
#         links.append(line)

with open("grants_gov_g.json", "w") as out:
    out.write(json.dumps(links))
