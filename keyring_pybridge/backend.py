import json
from subprocess import run

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


def format_args(*args):
    return ', '.join(map(repr, args))


class PyBridgeKeyring(KeyringBackend):
    priority = 1
    python = "python"

    def set_password(self, servicename, username, password):
        call_python_keyring(
            self.python,
            f"keyring.set_password({format_args(servicename, username, password)})",
        )

    def get_password(self, servicename, username):
        return json.loads(call_python_keyring(
            self.python, f"import json; print(json.dumps(keyring.get_password({format_args(servicename, username)})))"
        ))

    def delete_password(self, servicename, username):
        call_python_keyring(
            self.python, f"keyring.delete_password({format_args(servicename, username)})"
        )
