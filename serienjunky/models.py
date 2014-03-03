
from __future__ import absolute_import

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from serienjunky.config import sqla_uri, sqla_params

engine = sa.create_engine(sqla_uri, **sqla_params)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Unicode(80), nullable=False)
    last_name = sa.Column(sa.Unicode(80), nullable=False)
    email = sa.Column(sa.Unicode(300), nullable=False)
    openid = sa.Column(sa.Unicode(300), nullable=False)


class Show(Base):
    __tablename__ = 'shows'

    id = sa.Column(sa.Integer, primary_key=True)
