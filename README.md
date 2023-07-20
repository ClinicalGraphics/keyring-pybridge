# keyring-pybridge

[![CI](https://github.com/clinicalgraphics/keyring-pybridge/actions/workflows/ci.yml/badge.svg)](https://github.com/clinicalgraphics/keyring-pybridge/actions/workflows/ci.yml)
[![PyPI version ](https://badge.fury.io/py/keyring-pybridge.svg)
](https://badge.fury.io/py/keyring-pybridge)

## Usage

Install `keyring-pybridge` from pypi using `pip install keyring-pybridge`, or whatever alternative python package manager you prefer.

Then set environment variables to use the backend:

```
PYTHON_KEYRING_BACKEND=keyring_pybridge.PyBridgeKeyring
```

Or use the programmatic API:

```py
import keyring
from keyring_pybridge import PyBridgeKeyring

keyring.set_keyring(PyBridgeKeyring())
```

## WSL

The most useful application of this backend is when you are using keyring in a WSL environment, and would like to connect it to the host machine's Windows Credential Manager.

On the host machine, you need to create a python environment and install keyring in it.

Then, in WSL, configure the environment variable `KEYRING_PROPERTY_PYTHON` to point to the python executable with keyring installed:

```
KEYRING_PROPERTY_PYTHON=C:\path\to\the\right\python.exe
```
