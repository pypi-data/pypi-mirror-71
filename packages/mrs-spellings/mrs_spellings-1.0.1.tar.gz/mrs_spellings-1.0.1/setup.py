# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrs_spellings', 'mrs_spellings.qwerty_caches']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mrs-spellings',
    'version': '1.0.1',
    'description': 'a micro utility for generating plausible misspellings',
    'long_description': None,
    'author': 'CircArgs',
    'author_email': 'quebecname@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
