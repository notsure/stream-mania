import os

sqla_uri = os.environ.get('DATABASE_URL', 'sqlite:///streammania.db')
sqla_params = {
    'echo': False,
    'encoding': 'utf-8'
}
cookie_secret = 'change_this_for_production'

tvdb_api_key = 'tvdb_api_key'
