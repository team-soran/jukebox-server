import re
import pathlib
import types
from setuptools import find_packages, setup

from jukebox import __version__


PWD = pathlib.Path('.')


def readme() -> str:
    with open(str(PWD / 'README.rst'), 'r') as readme:
        return readme.read()


def get_requirements(filename: str) -> types.GeneratorType:
    with open(str(PWD / filename), 'r') as requirements:
        for requirement in requirements:
            if not re.match('^--?[a-zA-Z]+', requirement):
                continue
            yield requirement


install_requires = [
    'toml >= 0.9.1, < 1.0.0',
    'flask >= 0.10.1',
]
dev_requires = [
    'pytest >= 2.8.3, < 3.0.0',
    'pytest-sugar >= 0.5.1, < 0.6',
    'pytest-cov >= 2.2.0, < 2.3.0',
]


setup(
    name='jukebox-server',
    version=__version__,
    url='http://github.com/team-soran/jukebox-server',
    author='Kang Hyojun',
    author_email='iam.kanghyojun' '@' 'gmail.com',
    description='local server',
    long_description=readme(),
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        'dev': dev_requires
    },
    entry_points={
        'console_scripts': [
            'jukebox-serve = jukebox.runserver:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
