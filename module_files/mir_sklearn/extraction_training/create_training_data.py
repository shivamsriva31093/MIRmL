import csv
from collections import defaultdict

import itertools

from .Fetch_from_lastfm import FetchData

ob = FetchData()
tag_track_matrix = defaultdict(list)
with open('vocabulary.csv', 'r', newline='') as in_file:
    in_csv = csv.reader(in_file)
    in_header = next(in_csv)
    i = 0
    for row in in_csv:
        if i == 3:
            break
        i += 1
        mood_tag = row[0]
        tag_list = row[1].split()
        print('Working on tag: %s' % mood_tag)
        tag_track_matrix[mood_tag].append(
            list(itertools.chain.from_iterable([ob.populate_data(tag) for tag in tag_list])))
