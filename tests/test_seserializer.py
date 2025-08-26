import Deserializer.deserializer as deserializer




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

    
    
    
    