# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contxt',
 'contxt.auth',
 'contxt.cli',
 'contxt.models',
 'contxt.services',
 'contxt.utils']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3,<4', 'pyjwt[crypto]>=1,<2', 'requests>=2,<3', 'tabulate']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

entry_points = \
{'console_scripts': ['contxt = contxt.__main__:cli']}

setup_kwargs = {
    'name': 'contxt-sdk',
    'version': '1.0.0b15',
    'description': 'Contxt SDK from </ndustrial.io>',
    'long_description': '# Contxt Python SDK\n\n[![build status](https://github.com/ndustrialio/contxt-sdk-python/workflows/build/badge.svg)](https://github.com/ndustrialio/contxt-sdk-python/actions)\n[![pypi version](https://img.shields.io/pypi/v/contxt-sdk.svg)](https://pypi.org/project/contxt-sdk/)\n![python](https://img.shields.io/badge/python-3.6+-blue.svg)\n\n## Installation\n\n```sh\npip install contxt-sdk\n```\n\n## CLI Usage\n\n```sh\ncontxt --help\n```\n\n## Documentation\n\n- [CLI](docs/cli.md)\n- [Worker](docs/worker.md)\n\n## Contributing\n\nPlease refer to [CONTRIBUTING.md](CONTRIBUTING.md).\n',
    'author': 'ndustrial.io',
    'author_email': 'dev@ndustrial.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ndustrialio/contxt-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
