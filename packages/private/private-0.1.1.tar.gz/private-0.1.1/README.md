
# Private

Encryption tool for python files and packages.

# Features

* Encrypting python scripts and packages so they can be used as drop-in replacements.
* Loading key from environment variable
* Validating decrypted module against SHA256 signature

# Usage

### Encryption:

    $ private [--key <key>] [--output <directory>] file.py [<path>...]

### Execution:

    $ export PRIVATE_KEY=1234567890abcdef1234567890abcdef
    $ python encrypted.py
    $ pip install encrypted-0.0-py2-none-any.whl
    # Use installed package as usual

The key must be hexadecimal string of length 32.
The file type is recognized by extension, Currently only .py and .whl files are supported.

# Limitations

Private is not fully tested and is a hobby project in alpha stage, Use it at your own risk.

# Future plans

* Python 3 support
* sdist distribution support
* encrypt with faster crypto libraries
* Full coverage and functionality testing
* Adding documentation


