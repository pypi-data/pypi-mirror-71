# stepped-augustus
[![Current Version](https://img.shields.io/pypi/v/stepped-augustus?style=flat)](https://pypi.org/project/stepped-augustus)
[![Python Versions](https://img.shields.io/pypi/pyversions/stepped-augustus?style=flat)](https://pypi.org/project/stepped-augustus)
[![License](https://img.shields.io/pypi/l/stepped-augustus?style=flat)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)  


A variation of the Augustus Cipher that offsets space-separated words based on the position of each character; contary to what Augustus had originally practiced, letters wrap around instead of presenting a special case.


"Whenever he wrote in cipher, he wrote B for A, C for B, and the rest of the letters on the same principle, using AA for X."

   — Suetonius, _Life of Augustus_ 88


# Installation
Through `pip`:
```bash
> python -m pip install stepped-augustus
```

# Usage
As a CLI application:
```bash
> augustus -h
usage: augustus [-h] [--direction {left,right}] [--multiplier MULTIPLIER] message

Ciphers a given message.

positional arguments:
  message               The message to be ciphered

optional arguments:
  -h, --help            show this help message and exit
  --direction {left,right}
                        The direction to cipher the message to
  --multiplier MULTIPLIER
                        The multiplier to be applied when ciphering a message

> augustus "Hello, World" --direction right --multiplier 1
Igopt, Xqupi

> augustus "Igopt, Xqupi" --direction left --multiplier 1
Hello, World
```
As a package:
```python
>>> from augustus import SteppedAugustus

>>> SteppedAugustus("Hello, World", 1).right_cipher
'Igopt, Xqupi'

>>> SteppedAugustus("Igopt, Xqupi", 1).left_cipher
'Hello, World'
```

# Todo
- [ ] Publish to PyPI
- [x] Command-line script
- [ ] Utilize lazy evaluation
