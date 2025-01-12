#!/usr/bin/env python3
import csv, json
from bs4 import BeautifulSoup

tables_to_apply = {'1': {'L': [], 'R': []}, '2': {'L': [], 'R': []},'3': {'L': [], 'R': []},}
with open('invitees.csv') as istream:
    reader = csv.DictReader(istream)
    for row in reader:
        print(row)
        for key, person_name in row.items():
            # if not person_name:
            #     continue
            table_n, side = key.split(' ')
            tables_to_apply[table_n][side].append(person_name)
print(json.dumps(tables_to_apply, indent=2))

soup = BeautifulSoup(open('seating3.svg').read(), features='xml')
groups = soup.find('g', {'id': 'layer1'}).find('g')

ts = groups.find_all('g')

t = {
    '1': ts[0],
    '2': ts[1],
    '3': ts[2],
}

n_seats = 13
for table_n, table_group in t.items():
    side, idx = 'L', 0
    for seat_n, seat in enumerate(table_group.findChildren('text')):
        if idx >= len(tables_to_apply[table_n][side])-1:
            table_len = len(tables_to_apply[table_n][side])-1
            print(f'{side=}, idx > {table_len=}, setting to empty inc {idx=} > {idx+1}')
            seat.string = ''
        else:
            seat.string = tables_to_apply[table_n][side][idx]
            print('<< ', side, seat_n, idx, seat.string)

        idx += 1

        if idx == n_seats-1 and side == 'L':
            print(side, idx, '', 'changing side to R')
            idx = 0
            side = 'R'

print(soup.prettify(), file=open('steating_modified.svg', 'w'))