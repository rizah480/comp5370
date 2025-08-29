import re
import urllib.parse


class Deserializer:



    # Data-Type: num
    # A nosj num represents an integer value between positive-infinity and
    # negative-infinity. A marshalled num consists of the value's two's complement
    # representation (including the sign bit) in binary format as a sequence of ascii
    # "1"s and "0"s.

    # Examples:
    #     Marshalled nosj num: 1010
    #     Numerical value: -6

    #     Marshalled nosj num: 11110110
    #     Numerical value: -10

    @staticmethod
    def decode_num(bstr: str) -> int:
        n = len(bstr)               # number of bits
        val = int(bstr, 2)          # unsigned int value
        if val & (1 << (n - 1)):    # check sign bit
            val -= (1 << n)         # subtract 2^n if negative
        return val
    
    
    @staticmethod
    def process_num(key: str , val: str) -> int:
        if re.match(r"^[01]+$", val) is None:
            raise ValueError("Input string must be a binary string")
        
        return Deserializer.decode_num(val)
    
    
    
    
    #     # Data-Type: string
    # A nosj string is a sequence of ascii bytes which can be used to represent
    # arbitrary internal data such as ascii, unicode, or raw-binary. There are two
    # distinct representations of a nosj string data-type as described below.

    # ### Representation #1: Simple-Strings
    # In the simple representation, the string is restricted to a set of
    # commonly-used ascii characters which (according to our extensive market survey)
    # are the most-liked by humans (i.e. upper and lowercase ascii letters, ascii
    # digits, spaces (" " / 0x20), and tabs ("\t" / 0x09)). Simple-strings are
    # followed by a trailing "s" which is NOT part of the data being encoded.

    # Examples:
    #     Marshalled nosj simple-string: abcds
    #     String value: "abcd"

    #     Marshalled nosj simple-string: ef ghs
    #     String value: "ef gh"
        
    @staticmethod
    def decode_simple_str(bstr: str) -> str:
        SIMPLE_STRING_PATTERN = re.compile(r"^[a-zA-Z0-9 \t]+s$")
       
        raw = bstr
        if not SIMPLE_STRING_PATTERN.match(raw):
            raise ValueError(f"Invalid simple string: {raw}")
        return raw[:-1]  
        
        
    @staticmethod
    def process_simple_str(key: str , val: str) -> str:
        if val is not None and len(val) > 0:                 
            decoded = Deserializer.decode_simple_str(val)
            return f"{key} -- string -- {decoded}"
        return f"{key} -- string -- "
    
    
    
    
        ### Representation #2: Complex-Strings
    # In the complex representation, the string is percent-encoded in order to reuse
    # pre-existing and well-tested libraries such as those used for encoding/decoding
    # URLs. Where as simple-string may only represent a restricted set of characters,
    # complex-strings can encode arbitrary bytes. While the marshalled-form can
    # contain multiple percent-encoded bytes, it MUST include at least one (1)
    # percent-encoded byte.

    # Examples:
    #     Marshalled nosj complex-string: ab%2Ccd
    #     String value: "ab,cd"

    #     Marshalled nosj complex-string: ef%00gh
    #     String value: "ef<null-byte>gh"

    
    @staticmethod
    def decode_complex_str(bstr: str) -> str:
        
        COMPLEX_STRING_PATTERN = re.compile(r'^(?:%[0-9A-Fa-f]{2}|.)*$')
        
        
        # Step 1: Validate structure
        if not COMPLEX_STRING_PATTERN.match(bstr):
            raise ValueError(f"Invalid complex string format: {bstr}")

        # Step 2: Ensure at least one percent-encoded sequence
        if not re.search(r"%[0-9A-Fa-f]{2}", bstr):
            raise ValueError(f"Complex string must contain at least one %XY sequence: {bstr}")

        # Step 3: Decode (URL percent-decoding)
        return urllib.parse.unquote(bstr)

        
        
        
    @staticmethod
    def process_complex_str(key: str, val: str) -> str:
        if val is not None and len(val) > 0:
            decoded = Deserializer.decode_complex_str(val)
            return f"{key} -- string -- {decoded}"
        return f"{key} -- string -- "


        
    
    
        


