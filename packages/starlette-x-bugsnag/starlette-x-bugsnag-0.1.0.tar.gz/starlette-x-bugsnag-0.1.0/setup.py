# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_x_bugsnag']

package_data = \
{'': ['*']}

install_requires = \
['bugsnag>=3.6.1,<4.0.0',
 'importlib-metadata>=1.6.1,<2.0.0',
 'starlette>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'starlette-x-bugsnag',
    'version': '0.1.0',
    'description': 'Bugsnag integration for Starlette ASGI framework.',
    'long_description': None,
    'author': 'Vlad Dmitrievich',
    'author_email': 'me@2tunnels.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
