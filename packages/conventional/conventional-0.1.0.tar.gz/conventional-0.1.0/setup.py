# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conventional', 'conventional.commands', 'conventional.parser']

package_data = \
{'': ['*'], 'conventional': ['templates/*']}

install_requires = \
['aiocache>=0.11.1,<0.12.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'confuse>=1.1.0,<2.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'pytest-asyncio>=0.12.0,<0.13.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'conventional',
    'version': '0.1.0',
    'description': 'No frills processor for Conventional Commits (https://www.conventionalcommits.org/)',
    'long_description': None,
    'author': 'David Symons',
    'author_email': 'david.symons@onemodel.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
