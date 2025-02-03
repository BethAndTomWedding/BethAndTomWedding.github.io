#!/usr/bin/env python3
import csv, json, sys
from bs4 import BeautifulSoup

svg_ifpath, svg_ofpath, html_ofpath = sys.argv[1:]

print(f'{svg_ifpath=} > {svg_ofpath=}')

# read the CSV of invitees ----------------------

tables_to_apply = {'1': {'L': [], 'R': []}, '2': {'L': [], 'R': []},'3': {'L': [], 'R': []},}
with open('invitees.csv') as istream:
    reader = csv.DictReader(istream)
    for row in reader:
        print(row)
        for key, person_name in row.items():
            table_n, side = key.split(' ')
            tables_to_apply[table_n][side].append(person_name)
print(json.dumps(tables_to_apply, indent=2))

# read the template SVG --------------------------

soup = BeautifulSoup(open(svg_ifpath).read(), features='xml')
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

# update the SVG with the invitees ----------------

for table_n in list(map(str, range(1,4))):
    n_seats_l, n_seats_r = map(len, tables_to_apply[table_n].values())
    n_seats_missing = {'L': n_seats_r-n_seats_l, 'R': n_seats_l-n_seats_r}

    for side in ['L', 'R']:
        seats_in_svg = tables_in_svg[table_n][side].find_all('text')
        seats_to_apply = tables_to_apply[table_n][side]

        seat_y_positions = []
        for seat in seats_in_svg:
            seat_y_positions.append(float(seat.find('tspan').attrs['y']))

        print(seat_y_positions)

        from itertools import pairwise
        differences = [0]+[y-x for (x, y) in pairwise(seat_y_positions)]

        for i, (seat_in_svg, seat_to_apply) in enumerate(zip(seats_in_svg, seats_to_apply)):
            # set the name of the seat
            tspan = seat_in_svg.find('tspan')
            tspan.string = seat_to_apply
            print(f'{seat_to_apply=} > {seat_in_svg=}\n')
            # set the position of the seat (if the sides have uneven numbers)
            tspan.attrs['y'] = str(float(tspan.attrs['y']) + differences[i] * n_seats_missing[side] / 2)

print(soup, file=open(svg_ofpath, 'w'))

# add the SVG to the HTML page ------------------

print(f'writing to {html_ofpath=}')
soup_html = BeautifulSoup(open(html_ofpath).read(), 'html.parser')
soup_html.body.clear()

soup_html.body.append(
    soup_html.new_tag(
        'object',
        type  = 'image/svg+xml',
        data  = 'seating.svg',
        style = 'margin: auto; display: block; width: 70%; padding-top: 5%;',
        img=soup_html.new_tag(
            'img',
            src = 'seating.svg',
            alt = 'Seating Chart'
        ),
    )
)

print(soup_html.prettify(), file=open(html_ofpath, 'w'))
