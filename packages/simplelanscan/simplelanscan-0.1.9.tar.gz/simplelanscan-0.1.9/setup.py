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
    'version': '0.1.9',
    'description': 'Python Script to scan the local lan, report back the clients currently connected, and push to ElasticSearch.',
    'long_description': '# simplelanscan\n\nRun a simple arp scan of the network and push the results to ElasticSearch.\n\n\n```\npip install simplelanscan\n```\n\n\n\n## Systemd Hack\ncp /usr/local/lib/python3.7/dist-packages/scan_lan_clients.service /etc/systemd/system/.\ncp /usr/local/lib/python3.7/dist-packages/simplelanscan/config.ini to /usr/local/bin/config.ini\ncp /usr/local/lib/python3.7/dist-packages/simplelanscan/index.json to /usr/local/bin/index.json',
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
