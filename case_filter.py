from __future__ import print_function, unicode_literals

import csv
import json
import sys

SEEN_URLS = set([])

def clean(data):
    return ' '.join(data.split()).encode('utf8')

def main():
    writer = csv.DictWriter(sys.stdout, ('url', 'title', 'head', 'desc'))
    writer.writeheader()
    for line in sys.stdin:
        row = json.loads(line)
        normalised_url = row['url'].lower()
        if normalised_url not in SEEN_URLS:
            writer.writerow({k: clean(v) for k, v in row.items()})
            SEEN_URLS.add(normalised_url)


if __name__ == '__main__':
    main()
