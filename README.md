# keyring-pybridge

[![CI](https://github.com/clinicalgraphics/keyring-pybridge/actions/workflows/ci.yml/badge.svg)](https://github.com/clinicalgraphics/keyring-pybridge/actions/workflows/ci.yml)
[![PyPI version ](https://badge.fury.io/py/keyring-pybridge.svg)
](https://badge.fury.io/py/keyring-pybridge)

If you're using [`keyring`](https://github.com/jaraco/keyring/) in WSL, you'll run into a wall when you first try to use it. That's because keyring is attempting to connect to your linux distro's (probably Ubuntu) keyring background service, which by default isn't actually running in a WSL environment. 😱

This library exists to resolve that issue. `keyring-pybridge` is a custom keyring backend that calls a windows python binary via a subprocess, which facilitates the WSL context switch to Windows. That allows `keyring` to communicate with the Windows Credential Manager. 🚀

> **Note**
> If you did actually set up your linux distro's keyring background service, that's fine, you can continue using it and don't need this library.

## Installation

### Step 1: Windows setup

First, we have to do some work in Windows.

keyring-pybridge relies on the existence of a python environment on Windows that has keyring available. To create one, you can run the following commands in powershell:

```pwsh
# if you're using cmd instead of powershell, substitute %USERPROFILE% for $env:USERPROFILE
mkdir $env:USERPROFILE\.keyring-pybridge
cd $env:USERPROFILE\.keyring-pybridge
py -3 -m venv .
Scripts\pip install keyring
echo $env:USERPROFILE\.keyring-pybridge\Scripts\python.exe
```

The last line will print the path to your `python.exe`. You'll need to remember this path for the next step.

> **Note**
> You're free to use any other location or method to create a virtual environment on Windows, as long as you end up with a path to a `python.exe` that has keyring installed.

You can confirm if the virtual environment is suitable with the following command in powershell:

```pwsh
& $env:USERPROFILE\.keyring-pybridge\Scripts\python.exe -c 'import keyring'
```

Or in good old cmd:

```pwsh
%USERPROFILE%\.keyring-pybridge\Scripts\python.exe -c 'import keyring'
```

Of course, if you used a different location for the virtual environment, substitute the path accordingly in the commands.

### Step 2: WSL keyring setup

The rest of the installation process is performed in your shell of choice in WSL.

Set the following environment variables in your `~/.bashrc` or whatever shell profile file you prefer. 

> **Note**
> You have to populate the second variable with **your path to python.exe**, which you created in step 1.
>
> You can't just paste the path to `python.exe` directly. You have to **convert it to a path that resolves to the same location in WSL**. I'll show you my path so you can see how the conversion works and apply the same conversion to your path:
> 
> * Windows: `C:\Users\kvang\.keyring-pybridge\Scripts\python.exe`
> * WSL: `/mnt/c/Users/kvang/.keyring-pybridge/Scripts/python.exe`

So for my personal setup, I added the following two lines to the end of my `~/.bashrc` file:

```sh
export PYTHON_KEYRING_BACKEND="keyring_pybridge.PyBridgeKeyring"
export KEYRING_PROPERTY_PYTHON="/mnt/c/Users/kvang/.keyring-pybridge/Scripts/python.exe"
```

You have to reload your profile (`source ~/.bashrc` for bash) or you can just launch a new shell for the changes to take effect.

Run the following two commands in your shell to check the variables are configured correctly. The output should match what is shown here.

```shell
$ $KEYRING_PROPERTY_PYTHON -c 'import keyring; print("✅")'
✅
$ echo $PYTHON_KEYRING_BACKEND
keyring_pybridge.PyBridgeKeyring
```

### Step 3: WSL keyring-pybridge installation

We're almost there! 💪

Finally, you have to `pip install keyring-pybridge` into **each python environment in WSL that uses keyring**. Of course you can use alternative package managers, such as poetry, to install as well.

Examples of tools which use keyring are [poetry](https://python-poetry.org/) and [keycmd](https://github.com/ClinicalGraphics/keycmd). You can install into each of their environments to enable WSL support for those tools.

#### Example: poetry installation

```sh
poetryBinDir=$(dirname $(readlink -f $(which poetry)))
$poetryBinDir/pip install keyring-pybridge
```

Now you can use Poetry's built-in credential management commands in WSL with Windows Credential Manager! 🙌

#### Example: keycmd installation

Assuming you've installed keycmd globally, just `pip install keyring-pybridge` should be sufficient.

If you're using pyenv, you should first `pyenv activate keycmd`, before running `pip`. Don't forget to `pyenv deactivate` when you're done.

Now you can use keycmd in WSL with Windows Credential Manager! 🏎️
