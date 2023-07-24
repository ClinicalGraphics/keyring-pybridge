from functools import cache
import json
from pathlib import Path
from shutil import which
from subprocess import run
from sys import executable

from keyring.backend import KeyringBackend


def call_python_keyring(python, command):
    p = run(
        [python, "-c", f"import keyring; {command}"], shell=False, capture_output=True
    )
    stdout, stderr = p.stdout.decode("utf-8").strip(), p.stderr.decode("utf-8").strip()
    if p.returncode != 0:
        raise RuntimeError(
            f"call to WSL host keyring failed (python path: {python}): {stderr}"
        )
    return stdout


@cache
def check_python(python):
    if not python:
        raise ValueError("please configure KEYRING_PROPERTY_PYTHON")
    py_self = Path(executable).resolve()
    py_bridge = Path(python).resolve()
    if not py_bridge.is_file():
        py_bridge = Path(which(python) or "").resolve()
    if not py_bridge.is_file():
        raise ValueError(f"{python} is not a file")
    if py_self == py_bridge:
        raise ValueError(
            "please configure KEYRING_PROPERTY_PYTHON to a python"
            f" executable other than {executable}"
        )
    call_python_keyring(python, "")


def format_args(*args):
    return ", ".join(map(repr, args))


class PyBridgeKeyring(KeyringBackend):
    priority = 1
    python = ""

    def set_password(self, servicename, username, password):
        check_python(self.python)
        call_python_keyring(
            self.python,
            f"keyring.set_password({format_args(servicename, username, password)})",
        )

    def get_password(self, servicename, username):
        check_python(self.python)
        args = format_args(servicename, username)
        return json.loads(
            call_python_keyring(
                self.python,
                f"import json; print(json.dumps(keyring.get_password({args})))",
            )
        )

    def delete_password(self, servicename, username):
        check_python(self.python)
        call_python_keyring(
            self.python,
            f"keyring.delete_password({format_args(servicename, username)})",
        )
