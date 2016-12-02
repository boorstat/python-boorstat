# coding: utf-8

import tempfile
import os
import re
import roman
import json

import requests

TEXT_URL = 'https://github.com/boorstat/boorstat-files/raw/master/lit/dostoevsky/The_Idiot.txt'
JSON_URL = 'https://github.com/boorstat/boorstat-files/raw/master/lit/dostoevsky/idiot.json'


def objectify_paragraph(paragraph_text):
    paragraph = {
        'text': paragraph_text
    }

    sentences = re.split('(?:"|(?<!St)\.)+', paragraph_text)
    sentences = [s.strip() for s in sentences]
    sentences = list(filter(None, sentences))

    paragraph['sentences'] = sentences

    return paragraph


def objectify_chapter(chapter_text, chapter_num):
    chapter = {
        'title': '{}.'.format(roman.toRoman(chapter_num)),
        'text': chapter_text
    }

    paragraphs = re.split(r'^ {3}', chapter_text, flags=re.M)
    paragraphs = [p.strip() for p in paragraphs][1:]

    chapter['paragraphs'] = [objectify_paragraph(p) for p in paragraphs]

    return chapter


def objectify_part(part_text, part_num):
    part_text = re.sub(r'\n(?! {3})', '', part_text)

    part = {
        'title': 'PART {}'.format(roman.toRoman(part_num)),
        'text': part_text
    }

    chapters = re.split(r'^[ IVX]+\.?$', part_text, flags=re.M)
    chapters = [c.strip() for c in chapters][1:]

    part['chapters'] = [objectify_chapter(c, n + 1) for n, c in enumerate(chapters)]

    return part


def objectify_idiot(url=TEXT_URL):
    text = requests.get(url).text

    idiot = {
        'title': 'The Idiot',
        'author': 'Fyodor Dostoyevsky',
        'text': text}

    part_seps = ['PART {}'.format(roman.toRoman(i)) for i in range(4, 0, -1)]
    part_seps.append('Copyright')

    parts = re.split('|'.join(part_seps), text)
    idiot['copyright'] = parts[-1].strip()

    parts = [p.strip() for p in parts[1:-1]]

    idiot['parts'] = [objectify_part(p, n + 1) for n, p in enumerate(parts)]

    return idiot


def from_json(url=JSON_URL):
    cached_file = os.path.join(tempfile.gettempdir(), TEXT_URL.split('/')[-1])

    if not os.path.exists(cached_file):
        with open(cached_file, 'w') as f:
            f.write(requests.get(url).text)

    with open(cached_file, 'r') as f:
        return json.load(f)