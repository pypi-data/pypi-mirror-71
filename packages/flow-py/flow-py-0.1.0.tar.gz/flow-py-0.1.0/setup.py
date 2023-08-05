# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flow-py',
    'version': '0.1.0',
    'description': 'Placeholder',
    'long_description': None,
    'author': 'arranhs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
