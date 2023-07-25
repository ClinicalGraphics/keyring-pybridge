from functools import cache
import json
from pathlib import Path
from shutil import which
from subprocess import CalledProcessError, run
from sys import executable

from keyring.backend import KeyringBackend
from keyring.errors import *  # noqa: F403


def run_command(command, encoding="utf-8"):
    p = run(command, shell=False, capture_output=True, check=True)
    return p.stdout.decode(encoding).strip()


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
    run_command([python, "-c", "print('check')"])


@cache
def get_encoding(python):
    return run_command([python, "-c", "import sys; print(sys.stdout.encoding)"])


def call_keyring(python, command):
    check_python(python)
    encoding = get_encoding(python)
    code = """import keyring
import sys
try:
    {command}
except keyring.errors.KeyringError as err:
    print(repr(err), file=sys.stderr)
    sys.exit(100)
""".format(
        command=command
    )
    try:
        return run_command([python, "-c", code], encoding=encoding)
    except CalledProcessError as err:
        if err.returncode == 100:
            stderr = err.stderr.decode(encoding).strip()
            exc = eval(stderr)
            raise exc
        else:
            raise


def format_args(*args):
    return ", ".join(map(repr, args))


class PyBridgeKeyring(KeyringBackend):
    priority = 1
    python = ""

    def set_password(self, servicename, username, password):
        call_keyring(
            self.python,
            f"keyring.set_password({format_args(servicename, username, password)})",
        )

    def get_password(self, servicename, username):
        args = format_args(servicename, username)
        return json.loads(
            call_keyring(
                self.python,
                (
                    f"import json; print("
                    f"json.dumps(keyring.get_password({args}), ensure_ascii=False)"
                    f")"
                ),
            )
        )

    def delete_password(self, servicename, username):
        call_keyring(
            self.python,
            f"keyring.delete_password({format_args(servicename, username)})",
        )
