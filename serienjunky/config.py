
import os

sqla_uri = os.environ.get('DATABASE_URL', 'sqlite:///serienjunky.db')
sqla_params = {
    'echo': False,
    'encoding': 'utf-8'
}
cookie_secret = 'change_this_for_production'
