# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polecat_auth', 'polecat_auth.migrations']

package_data = \
{'': ['*']}

install_requires = \
['polecat']

setup_kwargs = {
    'name': 'polecat-auth',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Luke Hodkinson',
    'author_email': 'furious.luke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
