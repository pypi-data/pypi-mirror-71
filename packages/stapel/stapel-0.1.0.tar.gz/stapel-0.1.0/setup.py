# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stapel']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'docutils>=0.16,<0.17', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['stapel = stapel.__main__:main']}

setup_kwargs = {
    'name': 'stapel',
    'version': '0.1.0',
    'description': 'Manage IRC logs and statistics.',
    'long_description': '.. image:: https://stapel.readthedocs.io/en/latest/_static/logo-readme.png\n    :width: 950px\n    :align: center\n\nstapel\n########\n\n.. image:: https://travis-ci.org/supakeen/stapel.svg?branch=master\n    :target: https://travis-ci.org/supakeen/stapel\n\n.. image:: https://readthedocs.org/projects/stapel/badge/?version=latest\n    :target: https://stapel.readthedocs.io/en/latest/\n\n.. image:: https://stapel.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/stapel/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://img.shields.io/pypi/v/stapel\n    :target: https://pypi.org/project/stapel\n\n.. image:: https://codecov.io/gh/supakeen/stapel/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/supakeen/stapel\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/stapel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
