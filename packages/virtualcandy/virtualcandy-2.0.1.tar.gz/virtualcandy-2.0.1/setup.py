# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtualcandy']

package_data = \
{'': ['*'], 'virtualcandy': ['lib/*', 'lib/tmpl/*']}

setup_kwargs = {
    'name': 'virtualcandy',
    'version': '2.0.1',
    'description': 'Virtualcandy provides Virtualenv_ integration with your Bash or Zsh shell',
    'long_description': None,
    'author': 'Jeff Buttars',
    'author_email': 'jeffbuttars@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
