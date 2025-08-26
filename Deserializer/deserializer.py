import re


class Deserializer:





    @staticmethod
    def decode_num(bstr: str) -> int:
        n = len(bstr)               # number of bits
        val = int(bstr, 2)          # unsigned int value
        if val & (1 << (n - 1)):    # check sign bit
            val -= (1 << n)         # subtract 2^n if negative
        return val
    
    
    @staticmethod
    def process_num(val: str) -> int:
        if re.match(r"^[01]+$", val) is None:
            raise ValueError("Input string must be a binary string")
        
        return Deserializer.decode_num(val)
        
    
    
    
        


