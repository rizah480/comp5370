import Deserializer.deserializer as deserializer
import pytest




def test_add_two_numbers_negative_MSB():
    val : str = '110'
    assert deserializer.Deserializer.decode_num(val) == -2

def test_add_two_numbers_positive():
    val : str = '010'
    assert deserializer.Deserializer.decode_num(val) == 2
    
def test_add_two_numbers_negative_2():
    val : str = '11110110'
    assert deserializer.Deserializer.decode_num(val) == -10
    
def test_add_two_numbers_positive_2():
    val : str = '01110110'
    assert deserializer.Deserializer.decode_num(val) == 118
    
def test_process_num_invalid_input():
    val : str = '01201'
    try:
        deserializer.Deserializer.process_num(val)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Input string must be a binary string"
        
def test_process_num_valid_input():
    val : str = '1010'
    assert deserializer.Deserializer.process_num(val) == -6
    
# PROCESS_NUM AND DECODE_NUM COVERAGE IS 100% NOW
# ------------------------
# process_num() validation
# ------------------------

def test_process_num_valid_inputs():
    assert deserializer.Deserializer.process_num("0") == 0
    assert deserializer.Deserializer.process_num("1") == -1  # one bit, sign bit set
    assert deserializer.Deserializer.process_num("1010") == -6  # from doc example
    assert deserializer.Deserializer.process_num("11110110") == -10  # from doc example

def test_process_num_invalid_inputs():
    bad_inputs = ["", "2", "abc", "10102", " 1010", "1010 ", "\n1010", "10x01"]
    for val in bad_inputs:
        with pytest.raises(ValueError, match="Input string must be a binary string"):
            deserializer.Deserializer.process_num(val)

def test_process_num_large_input():
    # 64-bit wide binary string (positive)
    bstr = "0" + "1" * 63
    result = deserializer.Deserializer.process_num(bstr)
    assert isinstance(result, int)


# ------------------------
# decode_num() correctness
# ------------------------

@pytest.mark.parametrize("bstr, expected", [
    ("0", 0),         # zero
    ("1", -1),        # 1-bit negative
    ("10", -2),       # two-bit negative
    ("11", -1),       # two-bit: -1
    ("101", -3),       # positive 3-bit
    ("111", -1),      # negative 3-bit
    ("0111", 7),      # max positive 4-bit
    ("1000", -8),     # min negative 4-bit
    ("11110110", -10) # doc example
])
def test_decode_num_examples(bstr, expected):
    assert deserializer.Deserializer.decode_num(bstr) == expected


def test_decode_num_large_positive():
    bstr = "0" + "1" * 31  # 32-bit max positive
    val = deserializer.Deserializer.decode_num(bstr)
    assert val == int(bstr, 2)


def test_decode_num_large_negative():
    bstr = "1" + "0" * 31  # 32-bit min negative
    val = deserializer.Deserializer.decode_num(bstr)
    assert val == -(1 << 31)


# ------------------------
# integration
# ------------------------

def test_process_num_and_decode_match():
    """process_num should just wrap decode_num with validation"""
    bstr = "1110"
    assert deserializer.Deserializer.process_num(bstr) == deserializer.Deserializer.decode_num(bstr)

    
    
    
    