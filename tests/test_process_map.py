import pytest
import re
from io import StringIO
from contextlib import redirect_stdout
from Deserializer.deserializer import Deserializer

def run_process_map_and_capture(data):
    """Helper: capture stdout from process_map as a list of lines"""
    buf = StringIO()
    with redirect_stdout(buf):
        Deserializer.process_map(data)
    return buf.getvalue().strip().splitlines()

# -------------------------------------------------------------------
# Happy path tests
# -------------------------------------------------------------------

def test_flat_map_all_types():
    data = {
        "a": "1010",       # num
        "b": "abcds",      # simple-string
        "c": "ab%2Ccd"     # complex-string
    }
    out = run_process_map_and_capture(data)
    assert "a -- num -- -6" in out
    assert "b -- string -- abcd" in out
    assert "c -- string -- ab,cd" in out

def test_nested_map():
    data = {
        "root": {
            "x": "abcds",
            "y": "1001",
            "child": {
                "z": "ab%2Ccd"
            }
        }
    }
    out = run_process_map_and_capture(data)
    assert "root -- map -- " in out
    assert "begin-map" in out
    assert "x -- string -- abcd" in out
    assert "y -- num -- -7" in out
    assert "child -- map -- " in out
    assert "z -- string -- ab,cd" in out
    assert "end-map" in out

def test_empty_map():
    out = run_process_map_and_capture({})
    assert out == []  # no output for empty dict

# -------------------------------------------------------------------
# Validation / malformed input tests
# -------------------------------------------------------------------

def test_invalid_num_string():
    data = {"badnum": "102"}  # not valid binary
    with pytest.raises(ValueError):
        run_process_map_and_capture(data)

def test_invalid_simple_string_missing_s():
    data = {"simp": "abcd"}  # no trailing 's'
    with pytest.raises(ValueError):
        run_process_map_and_capture(data)

def test_invalid_complex_string_no_percent():
    data = {"comp": "abcdef"}  # no %XY
    with pytest.raises(ValueError):
        run_process_map_and_capture(data)

def test_invalid_complex_string_bad_hex():
    data = {"comp": "abc%GZdef"}  # invalid hex digits
    with pytest.raises(ValueError):
        run_process_map_and_capture(data)

# -------------------------------------------------------------------
# Key validation tests
# -------------------------------------------------------------------

def test_valid_lowercase_key():
    data = {"abc": "abcds"}
    out = run_process_map_and_capture(data)
    assert any("abc -- string -- abcd" in line for line in out)

def test_uppercase_key_rejected():
    data = {"Abc": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: Abc"):
        run_process_map_and_capture(data)

def test_mixed_case_key_rejected():
    data = {"abC": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: abC"):
        run_process_map_and_capture(data)

def test_key_with_number_rejected():
    data = {"key1": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: key1"):
        run_process_map_and_capture(data)

def test_key_with_space_rejected():
    data = {"bad key": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: bad key"):
        run_process_map_and_capture(data)

def test_key_with_special_char_rejected():
    data = {"bad-key!": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: bad-key!"):
        run_process_map_and_capture(data)

def test_empty_key_rejected():
    data = {"": "abcds"}
    with pytest.raises(ValueError, match="Invalid key format: "):
        run_process_map_and_capture(data)

def test_nested_map_with_invalid_key():
    data = {
        "outer": {
            "Inner": "abcds"  # uppercase inside nested map
        }
    }
    with pytest.raises(ValueError, match="Invalid key format: Inner"):
        run_process_map_and_capture(data)

# -------------------------------------------------------------------
# Output consistency / structural tests
# -------------------------------------------------------------------

def test_output_order_is_preserved():
    data = {"a": "abcds", "b": "1010", "c": "ab%2Ccd"}
    out = run_process_map_and_capture(data)
    assert out[0].startswith("a -- string")
    assert out[1].startswith("b -- num")
    assert out[2].startswith("c -- string")

def test_map_boundaries_match():
    data = {"outer": {"inner": {"leaf": "abcds"}}}
    out = run_process_map_and_capture(data)
    begin_count = out.count("begin-map")
    end_count = out.count("end-map")
    assert begin_count == end_count

# -------------------------------------------------------------------
# Edge case / security style tests
# -------------------------------------------------------------------

def test_nested_maps_deep():
    # Create 1000 levels of nesting (stress test recursion depth)
    data = current = {}
    for i in range(1000):
        current["k"] = {}
        current = current["k"]
    with pytest.raises(RecursionError):
        run_process_map_and_capture(data)

def test_large_input_size_invalid_keys():
    big_map = {f"k{i}": "1010" for i in range(1000)}  # invalid keys
    with pytest.raises(ValueError):
        run_process_map_and_capture(big_map)

