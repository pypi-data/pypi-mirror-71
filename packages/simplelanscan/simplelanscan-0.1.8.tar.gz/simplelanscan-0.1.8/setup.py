# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplelanscan']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.0.0,<8.0.0', 'scapy==2.4.3']

entry_points = \
{'console_scripts': ['simplelanscan = simplelanscan.scan:run_scan']}

setup_kwargs = {
    'name': 'simplelanscan',
    'version': '0.1.8',
    'description': 'Python Script to scan the local lan, report back the clients currently connected, and push to ElasticSearch.',
    'long_description': '# simplelanscan\n\nRun a simple arp scan of the network and push the results to ElasticSearch.',
    'author': 'blcarlson01',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blcarlson01/simplelanscan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
