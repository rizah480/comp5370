import Deserializer.deserializer as deserializer
import pytest




import pytest
from Deserializer.deserializer import Deserializer   # ✅ updated import

# -------------------------------------------------------------------
# Tests for decode_simple_str
# -------------------------------------------------------------------

def test_decode_simple_str_basic():
    assert Deserializer.decode_simple_str("abcds") == "abcd"

def test_decode_simple_str_with_space():
    assert Deserializer.decode_simple_str("ef ghs") == "ef gh"

def test_decode_simple_str_with_tab():
    assert Deserializer.decode_simple_str("abc\tdefs") == "abc\tdef"

def test_decode_simple_str_single_char():
    assert Deserializer.decode_simple_str("as") == "a"

def test_decode_simple_str_only_digit():
    assert Deserializer.decode_simple_str("123s") == "123"

def test_decode_simple_str_rejects_missing_s():
    with pytest.raises(ValueError):
        Deserializer.decode_simple_str("abcd")  # no trailing 's'

def test_decode_simple_str_rejects_invalid_char():
    with pytest.raises(ValueError):
        Deserializer.decode_simple_str("abc!s")  # ! not allowed

def test_decode_simple_str_rejects_empty_string():
    with pytest.raises(ValueError):
        Deserializer.decode_simple_str("")

def test_decode_simple_str_rejects_just_s():
    with pytest.raises(ValueError):
        Deserializer.decode_simple_str("s")  # nothing before 's'

# -------------------------------------------------------------------
# Tests for process_simple_str
# -------------------------------------------------------------------

def test_process_simple_str_valid():
    result = Deserializer.process_simple_str("x", "abcds")
    assert result == "x -- string -- abcd"

def test_process_simple_str_with_space():
    result = Deserializer.process_simple_str("y", "ef ghs")
    assert result == "y -- string -- ef gh"

def test_process_simple_str_with_tab():
    result = Deserializer.process_simple_str("z", "ab\tcs")
    assert result == "z -- string -- ab\tc"

def test_process_simple_str_empty_value():
    result = Deserializer.process_simple_str("k", "")
    assert result == "k -- string -- "

def test_process_simple_str_none_value():
    result = Deserializer.process_simple_str("k", None)
    assert result == "k -- string -- "

def test_process_simple_str_invalid_value_raises():
    with pytest.raises(ValueError):
        Deserializer.process_simple_str("bad", "abc!s")




