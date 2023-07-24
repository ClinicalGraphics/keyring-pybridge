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

Finally, you have to point the backend to the secondary python executable that you want to connect to. The keyring package must be installed in that python executable's environment.

```
KEYRING_PROPERTY_PYTHON=/path/to/python
```

## WSL

The most useful application of this backend is when you are using keyring in a WSL environment, and would like to connect it to the host machine's Windows Credential Manager.

On the host machine, you need to create a python environment and install keyring in it.

Then, in WSL, configure the environment variable `KEYRING_PROPERTY_PYTHON` to point to the python executable with keyring installed:

```
KEYRING_PROPERTY_PYTHON=C:\path\to\the\right\python.exe
```

Since this library calls the windows binary via a subprocess, this facilitates the context switch to windows that allows keyring to communicate with the Windows Credential Manager. 🎉
