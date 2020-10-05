import json
import urllib.request
import os

KEYWORDS = [
    'covid+tested',
    'covid+test'
]

BASE_URL = 'http://api.pushshift.io/reddit/search/comment/?q={}&after=300d&aggs=created_utc&frequency=day&size=0&sort=asc'

def get_data(base_url, keyword):
    url = base_url.format(keyword)
    data = urllib.request.urlopen(url).read()
    record = data.decode('UTF-8')
    result = json.loads(record)
    result = result.get('aggs').get('created_utc')

    if '+' in keyword:
        file_to_write = keyword.replace('+', '-')
        col_name = keyword.replace('+', '_')

    with open(file_to_write + '.csv', 'w+') as f:
        f.write('date,{}\n'.format(col_name + '_count'))
        for line in result:
            f.write(','.join([str(line.get('key')), str(line.get('doc_count'))]))
            f.write('\n')

for keyword in KEYWORDS:
    get_data(BASE_URL, keyword)
