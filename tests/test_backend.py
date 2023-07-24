from sys import executable

import pytest

import keyring_pybridge


@pytest.fixture
def backend(monkeypatch):
    # disable check_python
    monkeypatch.setattr(keyring_pybridge.backend, "check_python", lambda python: None)
    # configure current python executable for testing
    monkeypatch.setattr(keyring_pybridge.PyBridgeKeyring, "python", executable)

    yield keyring_pybridge.PyBridgeKeyring()


@pytest.fixture
def backend_misconfigured(monkeypatch):
    # configure current python executable for testing
    monkeypatch.setattr(keyring_pybridge.PyBridgeKeyring, "python", executable)

    yield keyring_pybridge.PyBridgeKeyring()


servicename = "__keyring_pybridge_test"
username = "username"
password = "password"


def test_backend(backend):
    assert backend.get_password(servicename, username) is None
    backend.set_password(servicename, username, password)
    assert backend.get_password(servicename, username) == password
    backend.delete_password(servicename, username)
    assert backend.get_password(servicename, username) is None

    with pytest.raises(RuntimeError):
        assert backend.get_password(None, None) is None


def test_backend_same_python(backend_misconfigured):
    with pytest.raises(ValueError):
        backend_misconfigured.get_password(servicename, username)


def test_format_args():
    assert keyring_pybridge.backend.format_args("foo", 1, None) == "'foo', 1, None"


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


def test_call_python_keyring():
    assert keyring_pybridge.backend.call_python_keyring(executable, "print(5)") == "5"

    with pytest.raises(FileNotFoundError):
        keyring_pybridge.backend.call_python_keyring(garble, "")

    with pytest.raises(RuntimeError, match=garble):
        keyring_pybridge.backend.call_python_keyring(executable, garble)
