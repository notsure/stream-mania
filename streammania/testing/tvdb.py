
from mock import patch


class FakeTVDB:
    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, name, lang):
        return [FakeShow()]


class FakeShow:

    Network = 'HBO'
    SeriesName = 'Game of Thrones'
    lang = 'en'


tvdb_mock = patch('streammania.handlers.shows.TVDB', FakeTVDB)
