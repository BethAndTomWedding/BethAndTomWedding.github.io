#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json

import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter as Formatter
from pygments.styles import get_style_by_name
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta

def _json_default(obj: object):
    'Default JSON serializer, supports most main class types'
    if isinstance(obj, str):       return obj
    if is_dataclass(obj):          return asdict(obj)
    if isinstance(obj, datetime):  return obj.isoformat()
    if hasattr(obj, '__dict__'):   return obj.__dict__
    if hasattr(obj, '__name__'):   return obj.__name__
    if hasattr(obj, '__slots__'):  return {k: getattr(obj, k) for k in obj.__slots__}
    if hasattr(obj, '_asdict'):    return obj._asdict()
    return str(obj)

def ppd(d, indent=2): print(highlight(json.dumps(d, indent=indent, default=_json_default), JsonLexer(), Formatter(style=get_style_by_name('material'))).strip())
def ppj(j, indent=2): ppd(json.loads(j), indent=indent)

# url = 'https://www.youtube.com/playlist?list=PLnr0Zs4ZO3sqSJlGhWd4uqXZU10jR3mjs'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# script_element = soup.find_all(
#     'script',
#     {'nonce': 'h8cuuMGR-6XA-diPer0VmA'}
# )[-6].get_text().split(' = ')[1].removesuffix(';')


# with open('playlist/playlist.json', 'w') as ostream:
#     print(json.dumps(json.loads(script_element), indent=2), file=ostream)


with open('playlist/playlist.json', 'r') as istream:
    script_element = json.load(istream)

playlist_items = script_element['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

for playlist_item in playlist_items:
    length = '00:'+playlist_item['playlistVideoRenderer']['lengthText']['simpleText']
    title = playlist_item['playlistVideoRenderer']['title']['runs'][0]['text']
    url = 'https://www.youtube.com/watch?v=' + playlist_item['playlistVideoRenderer']['videoId']
    channel = playlist_item['playlistVideoRenderer']['shortBylineText']['runs'][0]['text']

    ppd({'length': length, 'url': url, 'title': title, 'channel': channel}, indent=None)

with open('playlist/playlist.tsv', 'w') as ostream:
    for playlist_item in playlist_items:
        length = '00:'+playlist_item['playlistVideoRenderer']['lengthText']['simpleText']
        title = playlist_item['playlistVideoRenderer']['title']['runs'][0]['text']
        url = 'https://www.youtube.com/watch?v=' + playlist_item['playlistVideoRenderer']['videoId']
        channel = playlist_item['playlistVideoRenderer']['shortBylineText']['runs'][0]['text']
        print(length, url, title, channel, sep='\t', file=ostream)
