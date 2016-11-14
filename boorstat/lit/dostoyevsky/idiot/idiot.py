# coding: utf-8

import tempfile
import os
import re

import requests
from cached_property import cached_property


class Idiot(object):
    url = 'https://github.com/boorstat/boorstat.github.io/raw/master/files/dostoevsky/The_Idiot.txt'

    def __init__(self, use_cached=True):
        self.use_cached = use_cached

    def parts(self):
        pass
        # re.split(self.raw.split)

    @cached_property
    def copyright(self):
        pass

    def download(self):
        with open(self.cached_filename, 'w') as f:
            f.write(requests.get(self.url).text)

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
        return os.path.join(tempfile.gettempdir(), self.url.split('/')[-2])