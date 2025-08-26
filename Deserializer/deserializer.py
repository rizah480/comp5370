class Deserializer:





    @staticmethod
    def decode_num(bstr: str) -> int:
        n = len(bstr)               # number of bits
        val = int(bstr, 2)          # unsigned int value
        if val & (1 << (n - 1)):    # check sign bit
            val -= (1 << n)         # subtract 2^n if negative
        return val
    
    
    
        


