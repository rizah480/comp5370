import Deserializer.deserializer as deserializer




def test_add_two_numbers():
    val : str = '110'
    assert deserializer.Deserializer.decode_num(val) == -2
    
    