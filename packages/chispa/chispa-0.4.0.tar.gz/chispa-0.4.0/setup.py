# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chispa']

package_data = \
{'': ['*']}

install_requires = \
['PrettyTable>=0.7.2,<0.8.0', 'pyspark>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'chispa',
    'version': '0.4.0',
    'description': 'Pyspark test helper library',
    'long_description': None,
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
