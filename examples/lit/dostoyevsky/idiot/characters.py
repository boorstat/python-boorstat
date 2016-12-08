# coding: utf-8

import re
from pprint import pprint

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

from boorstat.lit.dostoyevsky.idiot import idiot


CHARACTERS = {
    'Prince Myshkin': ['Lev Nikolayevich', 'Lef Nicolayevitch', 'Myshkin', r'prince(?! S\.)'],
    'Nastasya Philipovna': ['Nastasia Philipovna', 'Barashkova'],
    'Parfyon Semyonovich Rogozhin': ['Parfyon', 'Rogozhin', 'Rogojin'],
    'General Ivan Fyodorovich Yepanchin': ['general', 'Ivan Fyodorovich'],
    'Elizaveta Prokofyevna': ['Elizabetha', 'Prokofievna', r'Mrs\. Epanchin'],
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
    'Evgeny Pavlovich Radomsky': ['Pavlovitch', 'Radomski'],
    'Prince S.': ['prince S.'],
    'Afanasy Ivanovich Totsky': ['Afanasy Ivanovitch', 'Totski'],
    'Ferdyshchenko': ['Ferdishenko'],
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
    data = data

    traces = []

    for character in reversed(sorted(data[0]['rates'])):
        traces.append(go.Scatter(
            x=[],
            y=[],
            text=[],
            # fill='tozeroy' if not traces else 'tonexty',
            fill='tonexty',
            mode='none',
            line={'shape': 'spline'},
            hoverinfo='text',
            name=character))

    sums = {}
    for trace in traces:
        for chapter in data:
            sums[chapter['chapter']] = sums.get(chapter['chapter'], 0) + chapter['rates'][trace['name']]
            trace['x'].append(chapter['chapter'])
            trace['y'].append(sums[chapter['chapter']])
            # trace['text'].append(trace['name'][:5])
            trace['text'].append(
                '{} - {}'.format(chapter['rates'][trace['name']], trace['name'])
                if chapter['rates'][trace['name']] else '')

    traces_with_liners = []
    for trace in traces:
        traces_with_liners.append(trace)
        traces_with_liners.append(go.Scatter(
            x=trace['x'],
            y=trace['y'],
            # y=[y + 5 for y in trace['y']],
            # text=[''] * len(trace['x']),
            fill='tonexty',
            showlegend=False,
            line={'shape': 'spline'},
            hoverinfo='none',
            mode='none',
            fillcolor='#ffffff'
        ))

    return traces_with_liners


def plot(traces):
    # layout = go.Layout(title='Idiot Characters', width=800, height=640)
    layout = go.Layout(title='Idiot Characters')
    fig = go.Figure(data=traces, layout=layout)

    # py.plot(fig, image='svg')
    plotly.offline.plot(fig)
    # py.image.save_as(fig, filename='idiot-characters.png')


def main():
    roman = idiot.from_json()

    data = parse_parts(roman)
    traces = prepare_data(data)
    plot(traces)


if __name__ == '__main__':
    main()