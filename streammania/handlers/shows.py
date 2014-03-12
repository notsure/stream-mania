from pytvdbapi.api import TVDB

from streammania.base import BaseHandler
from streammania.config import tvdb_api_key


def show_to_dict(show):
    return {
        'network': show.Network,
        'name': show.SeriesName,
        'language': show.lang
    }


class ShowsHandler(BaseHandler):
    def get(self, language, name):
        db = TVDB(tvdb_api_key)
        shows = db.search(name, language)
        shows = [show_to_dict(show) for show in shows]
        data = {
            'status': 'success',
            'data': shows
        }
        self.write(data)
