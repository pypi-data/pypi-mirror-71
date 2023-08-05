# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['augustus']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['augustus = augustus.cli:main']}

setup_kwargs = {
    'name': 'stepped-augustus',
    'version': '1.1.0',
    'description': 'A variation of the Augustus Cipher that offsets space-separated words based on the position of each character.',
    'long_description': '# stepped-augustus\n[![Current Version](https://img.shields.io/pypi/v/stepped-augustus?style=flat)](https://pypi.org/project/stepped-augustus)\n[![Python Versions](https://img.shields.io/pypi/pyversions/stepped-augustus?style=flat)](https://pypi.org/project/stepped-augustus)\n[![License](https://img.shields.io/pypi/l/stepped-augustus?style=flat)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PR\'s Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)  \n\n\nA variation of the Augustus Cipher that offsets space-separated words based on the position of each character; contrary to what Augustus had originally practiced, letters wrap around instead of presenting a special case.\n\n\n> "Whenever he wrote in cipher, he wrote B for A, C for B, and the rest of the letters on the same principle, using AA for X."\n\nSuetonius, _Life of Augustus_ 88\n\n\n# Installation\nThrough `pip`:\n```bash\n> python -m pip install stepped-augustus\n```\n\n# Usage\nAs a CLI application:\n```bash\n> augustus -h\nusage: augustus [-h] [--direction {left,right}] [--multiplier MULTIPLIER] message\n\nCiphers a given message.\n\npositional arguments:\n  message               The message to be ciphered\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --direction {left,right}\n                        The direction to cipher the message to\n  --multiplier MULTIPLIER\n                        The multiplier to be applied when ciphering a message\n\n> augustus "Hello, World" --direction right --multiplier 1\nIgopt, Xqupi\n\n> augustus "Igopt, Xqupi" --direction left --multiplier 1\nHello, World\n```\nAs a package:\n```python\n>>> from augustus import SteppedAugustus\n>>>\n>>> SteppedAugustus("Hello, World", 1).right_cipher\n\'Igopt, Xqupi\'\n>>>\n>>> SteppedAugustus("Igopt, Xqupi", 1).left_cipher\n\'Hello, World\'\n>>>\n>>> # Alternatively the _cipher method can be used for lazy\n>>> # evaluation and customizing the direction.\n>>>\n>>> for char in SteppedAugustus("Hello", 1)._cipher(1):\n...     print(char)\n```\n\n',
    'author': 'PureFunctor',
    'author_email': 'purefunctor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PureFunctor/stepped-augustus',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
