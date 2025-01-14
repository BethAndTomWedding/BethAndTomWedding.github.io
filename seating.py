#!/usr/bin/env python3
import csv, json, sys
from bs4 import BeautifulSoup

ifpath, ofpath = sys.argv[1], sys.argv[2]

print(f'{ifpath=} > {ofpath=}')

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

soup = BeautifulSoup(open(ifpath).read(), features='xml')

print(soup.prettify())

tables_in_svg = {
    '1': {
        'L': soup.find('g', {'id': 'table1LHS'}),
        'R': soup.find('g', {'id': 'table1RHS'}),
    },
    '2': {
        'L': soup.find('g', {'id': 'table2LHS'}),
        'R': soup.find('g', {'id': 'table2RHS'}),
    },
    '3': {
        'L': soup.find('g', {'id': 'table3LHS'}),
        'R': soup.find('g', {'id': 'table3RHS'}),
    },
}

print(tables_in_svg)

# take the seats from the "tables_to_apply" and apply them to the svg
for table_n in list(map(str, range(1,4))):
    for side in ['L', 'R']:
        table_in_svg = tables_in_svg[table_n][side]
        table_to_apply = tables_to_apply[table_n][side]

        for seat_in_svg, seat_to_apply in zip(table_in_svg.find_all('text'), table_to_apply):
            print(f'{seat_in_svg=} {seat_to_apply=}')
            text_in_svg = seat_in_svg.find('tspan')
            text_in_svg.string = seat_to_apply
            print(f'{seat_in_svg=}\n')

# print(soup.prettify(), file=open('steating_modified.svg', 'w'))
print(soup, file=open(ofpath, 'w'))
