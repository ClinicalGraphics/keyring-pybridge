from subprocess import CalledProcessError
from sys import executable

import pytest

from keyring.errors import PasswordDeleteError
import keyring_pybridge


@pytest.fixture
def no_check(monkeypatch):
    # disable check_python
    monkeypatch.setattr(keyring_pybridge.backend, "check_python", lambda python: None)

    yield


@pytest.fixture
def backend(monkeypatch):
    monkeypatch.setattr(keyring_pybridge.PyBridgeKeyring, "python", executable)

    yield keyring_pybridge.PyBridgeKeyring()


servicename = "__keyring_pybridge_test€€$ß"
username = "userna€€$ßme"
password = "passw€€$ßrd"


def test_backend(backend, no_check):
    try:
        backend.delete_password(servicename, username)
    except PasswordDeleteError:
        pass
    assert backend.get_password(servicename, username) is None
    backend.set_password(servicename, username, password)
    assert backend.get_password(servicename, username) == password
    backend.delete_password(servicename, username)
    assert backend.get_password(servicename, username) is None

    with pytest.raises(CalledProcessError):
        assert backend.get_password(None, None) is None


def test_backend_same_python(backend):
    with pytest.raises(ValueError):
        backend.get_password(servicename, username)


def test_format_args():
    assert keyring_pybridge.backend.format_args("fooß", 1, None) == "'fooß', 1, None"


garble = "saddfasdfasdf"


def test_check_python():
    with pytest.raises(ValueError, match="configure KEYRING_PROPERTY_PYTHON"):
        keyring_pybridge.backend.check_python("")
    with pytest.raises(
        ValueError,
        match="configure KEYRING_PROPERTY_PYTHON to a python executable other than",
    ):
        keyring_pybridge.backend.check_python(executable)
    with pytest.raises(ValueError, match="is not a file"):
        keyring_pybridge.backend.check_python(garble)


def test_call_keyring(no_check):
    assert keyring_pybridge.backend.call_keyring(executable, "print('5ß')") == "5ß"

    with pytest.raises(FileNotFoundError):
        keyring_pybridge.backend.call_keyring(garble, "")

    with pytest.raises(CalledProcessError, match=garble):
        keyring_pybridge.backend.call_keyring(executable, garble)
