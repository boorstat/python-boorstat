# coding: utf-8

import re
from pprint import pprint

import plotly.plotly as py
import plotly.graph_objs as go

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
    data = []

    for part in roman['parts']:
        for chapter in part['chapters']:
            data.append({
                'chapter': '{} - {}'.format(part['title'], chapter['title']),
                'rates': rate_characters(chapter)})

    return data


def prepare_data(data):
    traces = []

    for character in data[0]['rates']:
        traces.append(go.Scatter(
            x=[],
            y=[],
            fill='tozeroy' if not traces else 'tonexty',
            mode='none',
            name=character))

    for trace in traces:
        for chapter in data:
            trace['x'].append(chapter['chapter'])
            trace['y'].append(chapter['rates'][trace['name']])

    return traces


def plot(traces):
    layout = go.Layout(title='Idiot Characters', width=800, height=640)
    fig = go.Figure(data=traces, layout=layout)

    py.image.save_as(fig, filename='idiot-characters.png')


def main():
    roman = idiot.from_json()

    data = parse_parts(roman)
    traces = prepare_data(data)
    plot(traces)


if __name__ == '__main__':
    main()