from setuptools import setup
import re


requirements = [
    'tornado',
    'SQLAlchemy'
]

versionf_content = open("streammania/__init__.py").read()
version_rex = r'^__version__ = [\'"]([^\'"]*)[\'"]$'
m = re.search(version_rex, versionf_content, re.M)
if m:
    version = m.group(1)
else:
    raise RuntimeError('Unable to find version string')

setup(
    name='streammania',
    version=version,
    install_requires=requirements,
    extras_require={
        'test': ['crate [test]',
                 'requests']
    },
    entry_points={
        'console_scripts': ['app=streammania.app:main']
    }
)
