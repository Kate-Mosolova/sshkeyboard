from contextlib import contextmanager

import sshkeyboard

i = -1
return_chars = ("a", "a", "b", "")


def setup_testing():
    @contextmanager
    def _raw(stream):
        yield

    @contextmanager
    def _nonblocking(stream):
        yield

    def _read_chars(amount):
        global i
        i += 1
        return return_chars[i % len(return_chars)]

    sshkeyboard._raw = _raw
    sshkeyboard._nonblocking = _nonblocking
    sshkeyboard._read_chars = _read_chars


setup_testing()


def empty(key):
    pass


def returns_char(key):
    if key not in return_chars:
        raise RuntimeError(f"Not correct char {key}")
    sshkeyboard.stop_listening()


def press_listen(key):
    try:
        sshkeyboard.listen_keyboard(empty, empty)
        raise RuntimeError("Error not raised")
    except AssertionError:
        pass
    sshkeyboard.stop_listening()


def press_listen_async(key):
    try:
        sshkeyboard.listen_keyboard_async(empty, empty)
        raise RuntimeError("Error not raised")
    except AssertionError:
        pass
    sshkeyboard.stop_listening()


def test_listen_returns_char():
    # listen_keyboard press
    sshkeyboard.listen_keyboard(returns_char, empty)
    # listen_keyboard release
    sshkeyboard.listen_keyboard(empty, returns_char)
    # listen_keyboard press
    sshkeyboard.listen_keyboard_async(returns_char, empty)
    # listen_keyboard release
    sshkeyboard.listen_keyboard_async(empty, returns_char)


def test_multiple_listens_raises_error():
    # listen_keyboard inside listen_keyboard fails
    sshkeyboard.listen_keyboard(press_listen, empty)
    # listen_keyboard_async inside listen_keyboard fails
    sshkeyboard.listen_keyboard(press_listen_async, empty)
    # listen_keyboard inside listen_keyboard_async fails
    sshkeyboard.listen_keyboard_async(press_listen, empty)
    # listen_keyboard_async inside listen_keyboard_async fails
    sshkeyboard.listen_keyboard_async(press_listen_async, empty)


# TODO, assert async fails listen, test sleeps,
# schedule orders, throwing errors etc.
