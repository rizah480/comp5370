import pytest
from Deserializer.deserializer import Deserializer

# -------------------------------------------------------------------
# Tests for decode_complex_str
# -------------------------------------------------------------------

def test_decode_complex_str_basic_comma():
    assert Deserializer.decode_complex_str("ab%2Ccd") == "ab,cd"

def test_decode_complex_str_null_byte():
    result = Deserializer.decode_complex_str("ef%00gh")
    assert result == "ef\x00gh"   # contains actual null byte

def test_decode_complex_str_space():
    assert Deserializer.decode_complex_str("hi%20there") == "hi there"

def test_decode_complex_str_multiple_encodings():
    assert Deserializer.decode_complex_str("path%2Fto%2Ffile") == "path/to/file"

def test_decode_complex_str_mixed_with_literals():
    assert Deserializer.decode_complex_str("abc%21def") == "abc!def"

def test_decode_complex_str_requires_percent_sequence():
    with pytest.raises(ValueError):
        Deserializer.decode_complex_str("abcdef")   # no %XY

def test_decode_complex_str_invalid_hex():
    with pytest.raises(ValueError):
        Deserializer.decode_complex_str("abc%GZdef")  # G/Z not valid hex

def test_decode_complex_str_truncated_percent():
    with pytest.raises(ValueError):
        Deserializer.decode_complex_str("abc%2")   # incomplete %XY

def test_decode_complex_str_empty_string():
    with pytest.raises(ValueError):
        Deserializer.decode_complex_str("")
# -------------------------------------------------------------------
# Tests for process_complex_str
# -------------------------------------------------------------------

def test_process_complex_str_valid():
    result = Deserializer.process_complex_str("x", "ab%2Ccd")
    assert result == "x -- string -- ab,cd"

def test_process_complex_str_null_byte():
    result = Deserializer.process_complex_str("y", "ef%00gh")
    assert result == "y -- string -- ef\x00gh"

def test_process_complex_str_empty_value():
    result = Deserializer.process_complex_str("z", "")
    assert result == "z -- string -- "

def test_process_complex_str_none_value():
    result = Deserializer.process_complex_str("k", None)
    assert result == "k -- string -- "

def test_process_complex_str_invalid_value_raises():
    with pytest.raises(ValueError):
        Deserializer.process_complex_str("bad", "abc%GZdef")  # invalid % sequence
