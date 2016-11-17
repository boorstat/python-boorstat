# coding: utf-8

import tempfile
import os
import re
import roman
# from itertools import

import requests
from cached_property import cached_property

TEXT_URL = 'https://github.com/boorstat/boorstat-files/raw/master/lit/dostoevsky/The_Idiot.txt'


def objectify_paragraph(paragraph_text, paragraph_num):
    pass


def objectify_chapter(chapter_text, chapter_num):
    chapter = {
        'title': '{}.'.format(roman.toRoman(chapter_num)),
        'text': chapter_text
    }

    return chapter


def objectify_part(part_text, part_num):
    part = {
        'title': 'PART {}'.format(roman.toRoman(part_num)),
        'text': part_text
    }

    # chapter_seps = ['{}\\.$'.format(roman.toRoman(i)) for i in range(17, 0, -1)]
    # print('|'.join(chapter_seps))
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

    parts = [p.strip() for p in parts[1:]]

    idiot['parts'] = [objectify_part(p, n + 1) for n, p in enumerate(parts)]

    return idiot


idiot = objectify_idiot()


quit()


class ClumsyIdiot(object):
    def __init__(self, use_cached=True):
        self.use_cached = use_cached

    def part(self, part_num):
        return self.raw_parts[1:-1][part_num - 1]

    def chapters(self, part_num):
        seps = ['{}.'.format(roman.toRoman(i)) for i in range(1, 17)]
        return [c.strip() for c in re.split('|'.join(seps), self.part(part_num))]

    @cached_property
    def raw_parts(self):
        seps = ['PART {}'.format(roman.toRoman(i)) for i in range(1, 5)]
        seps.append('Copyright')
        return [p.strip() for p in re.split('|'.join(seps), self.raw)]

    @cached_property
    def copyright(self):
        return self.raw_parts[-1]

    def download(self):
        with open(self.cached_filename, 'w') as f:
            f.write(requesxts.get(TEXT_URL).text)

    @cached_property
    def json(self):
        pass

    @cached_property
    def raw(self):
        if not self.use_cached or not os.path.exists(self.cached_filename):
            self.download()

        with open(self.cached_filename) as f:
            return f.read()

    @cached_property
    def cached_filename(self):
        return os.path.join(tempfile.gettempdir(), TEXT_URL.split('/')[-2])
