# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twinthread']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.3.1,<13.0.0',
 'pandas>=1.0.4,<2.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'twinthread',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
