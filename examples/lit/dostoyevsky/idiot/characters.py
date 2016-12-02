# coding: utf-8

import re
from pprint import pprint

from boorstat.lit.dostoyevsky.idiot import idiot


CHARACTERS = {
    'Prince Myshkin': ['Lev Nikolayevich', 'Lef Nicolayevitch', 'Myshkin', 'prince(?! S\.)'],
    'Nastasya Philipovna': ['Nastasia Philipovna', 'Barashkova'],
    'Parfyon Semyonovich Rogozhin': ['Parfyon', 'Rogozhin', 'Rogojin'],
    'General Ivan Fyodorovich Yepanchin': ['general', 'Ivan Fyodorovich'],
    'Elizaveta Prokofyevna': ['Elizaveta', 'Lizaveta', 'Prokofyevna'],
    'Alexandra Ivanovna': ['Alexandra'],
    'Adelaida Ivanovna': ['Adelaida'],
    'Aglaya Ivanovna': ['Aglaya'],
    'General Ardalion Alexandrovich Ivolgin': ['general', 'Ivolgin', 'Ardalion'],
    'Nina Alexandrovna': ['Nina'],
    'Gavrila Ardalionovich': ['Gavrila', 'Ganya', 'Ganechka', 'Ganka'],
    'Varvara Ardalionovna': ['Varvara'],
    'Lukyan Timofeevich Lebedev': ['Lukyan', 'Lebedeff'],
    'Vera Lukyanovna': ['Vera'],
    'Ippolit Terentyev': ['Ippolit'],
    'Ivan Petrovich Ptitsyn': ['Ivan Petrovich', 'Ptitsin'],
    'Evgeny Pavlovich Radomsky': ['Pavlovich', 'Radomsky'],
    'Prince S.': ['prince S.'],
    'Afanasy Ivanovich Totsky': ['Afanasy Ivanovich', 'Totsky'],
    'Ferdyshchenko': ['Ferdyshchenko'],
    'Keller': ['Keller'],
    'Antip Burdovsky': ['Antip', 'Burdovsky']
}


def rate_characters(chapter):
    characters = {}

    for char, regexps in CHARACTERS.items():
        characters[char] = sum([len(re.findall(regex, chapter['text'], re.U)) for regex in regexps])

    return characters


def parse_parts(roman):
    characters = {}

    for part in roman['parts']:
        for chapter in part['chapters']:
            characters['{} - {}'.format(part['title'], chapter['title'])] = rate_characters(chapter)

    pprint(characters)


def main():
    roman = idiot.from_json()

    parse_parts(roman)


if __name__ == '__main__':
    main()