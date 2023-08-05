# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cadence',
 'django_cadence.management',
 'django_cadence.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.6.0,<4.0.0', 'django>=2.2.0,<3.2']

extras_require = \
{'celery': ['celery>=4.4.0,<5.0.0'],
 'dramatiq': ['django_dramatiq>=0.8.0,<1.0.0']}

setup_kwargs = {
    'name': 'django-cadence',
    'version': '0.1.2',
    'description': 'A package to provide periodic scheduled task support in Django',
    'long_description': '# django_cadence\n\nA reusable Django app that provides scheduling of asynchronous tasks (optionally as asynchronous tasks via Dramatiq or Celery)\n\n![Latest GitHub Release](https://img.shields.io/github/v/release/LucidDan/django-cadence?sort=semver&style=plastic)\n![Latest Pypi Release](https://img.shields.io/pypi/v/django-cadence.svg?style=plastic)\n![License](https://img.shields.io/github/license/LucidDan/django-cadence?style=plastic)\n![Build](https://img.shields.io/travis/:LucidDan/django-cadence?style=plastic)\n\n![Photo of a calendar on a wall](https://unsplash.com/photos/PypjzKTUqLo "Photo by Roman Bozhko")\n\n## Introduction\n\nThis is a simple package, so far at least, that provides some scheduling capabilities in Django.\nIt can do this standalone, or in cooperation with [Dramatiq] or [Celery].\n\n\n## Links and References\n\n* [Releases - PyPI](https://pypi.org/django-cadence)\n* [Releases - GitHub](https://github.com/LucidDan/django-cadence/releases)\n* [GitHub Issues]\n* [Source](https://github.com/LucidDan/django-cadence/)\n* [ChangeLog](CHANGELOG.md)\n* [License](LICENSE.md)\n* [Contributing](CONTRIBUTING.md)\n\n## What\'s New\n\nCurrent version: 0.1.2\n\nTesting travis deployment, and updating documentation.\n\nSee the [changelog](CHANGELOG.md) for more information on recent changes.\n\n## Supported Releases\n\nSee [SECURITY.md] for releases which are currently supported for security updates.\n\nIn general, the current major release is supported for all bug and security fixes, and the previous major release is supported for security fixes only.\n\n## Dependencies\n\nRequired:\n * [Python]() v3.6.x - v3.8.x\n * [Django]() v2.2.x - v3.0.x\n * [APScheduler]() v3.6.x\n \nRecommended:\n * [Dramatiq]() v1.8.x - v1.9.x\n  (or)\n * [Celery]() v4.4.x\n\n\n## Installing\n\nUse pip or another pip-based tool in combination with PyPI to install this package.\n\n\n## Getting Support\n\nFirst, unless it is extremely urgent, please check the FAQ, Known Issues section, and general documentation before looking for help.\n\nThere are a few avenues available for support. In general, if you\'re really confident you\'ve found a bug, log an issue directly via GitHub.\n\n* [Log an issue via GitHub][GitHub Issues]\n\n\n## FAQ\n\nThis section contains some frequent questions and answers, be aware that if you did not read this section and ask one of these questions on the forum or chat server, you might get redirected back to read this with varying levels of politeness or irritation. ;-)\n\n### When will the mod be updated for Django version X, Python version Y, etc?\n\nWhen it is done. Pull requests are welcome.\n\n\n## Known Issues\n\nThis section attempts to sum up known issues in a easier-to-consume way. For the most up-to-date information on this, it might be worth checking [GitHub Issues]\n\n* There are currently no known issues.\n\n\n## Contributing\n\nSee [CONTRIBUTING.md] for information on how you can help contribute to this project.\n\n\n## Special Thanks\n\nHere is a non-exhaustive list of sources, people, etc that deserve some thanks for bringing this project into existence:\n\n* []()\n\n\n\n[GitHub Issues]: https://github.com/LucidDan/django-cadence/issues\n[Dramatiq]: https://dramatiq.io/\n[Celery]: https://docs.celeryproject.org/\n\n',
    'author': 'Dan Sloan',
    'author_email': 'dan@luciddan.com',
    'maintainer': 'Dan Sloan',
    'maintainer_email': 'dan@luciddan.com',
    'url': 'https://luciddan.github.io/django-cadence/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
