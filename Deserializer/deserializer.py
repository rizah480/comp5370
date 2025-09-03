import sys
import re
import urllib.parse


class Deserializer:
    """
    Deserializer utilities with standardized error handling.

    On any processing error:
      - prints:  'ERROR -- <message>\\n'  to stderr
      - exits:   status code 66
    """

    # ---------------------------
    # Unified error handler
    # ---------------------------
    @staticmethod
    def handle_error(msg: str) -> "NoReturn":  # type: ignore[name-defined]
        """
        Print a single-line error to stderr and exit(66).
        Required format: starts with 'ERROR -- ' and ends with one newline.
        """
        sys.stderr.write(f"ERROR -- {msg}\n")
        sys.exit(66)

    # ---------------------------
    # Data-Type: num
    # ---------------------------
    @staticmethod
    def decode_num(bstr: str) -> int:
        n = len(bstr)               # number of bits
        val = int(bstr, 2)          # unsigned int value
        if val & (1 << (n - 1)):    # check sign bit
            val -= (1 << n)         # subtract 2^n if negative
        return val

    @staticmethod
    def process_num(key: str, val: str) -> str:
        if re.match(r"^[01]+$", val) is None:
            raise ValueError("Input string must be a binary string")
        return f"{key} -- num -- {Deserializer.decode_num(val)}"

    # ---------------------------
    # Data-Type: string (simple)
    # ---------------------------
    @staticmethod
    def decode_simple_str(bstr: str) -> str:
        SIMPLE_STRING_PATTERN = re.compile(r"^[a-zA-Z0-9 \t]+s$")
        raw = bstr
        if not SIMPLE_STRING_PATTERN.match(raw):
            raise ValueError(f"Invalid simple string: {raw}")
        return raw[:-1]

    @staticmethod
    def process_simple_str(key: str, val: str) -> str:
        if val is not None and len(val) > 0:
            decoded = Deserializer.decode_simple_str(val)
            return f"{key} -- string -- {decoded}"
        return f"{key} -- string -- "

    # ---------------------------
    # Data-Type: string (complex)
    # ---------------------------
    @staticmethod
    def decode_complex_str(bstr: str) -> str:
        COMPLEX_STRING_PATTERN = re.compile(r'^(?:%[0-9A-Fa-f]{2}|.)*$')

        # Step 1: Validate structure
        if not COMPLEX_STRING_PATTERN.match(bstr):
            raise ValueError(f"Invalid complex string format: {bstr}")

        # Step 2: Ensure at least one percent-encoded sequence
        if not re.search(r"%[0-9A-Fa-f]{2}", bstr):
            raise ValueError(
                f"Complex string must contain at least one %XY sequence: {bstr}"
            )

        # Step 3: Decode (URL percent-decoding)
        return urllib.parse.unquote(bstr)

    @staticmethod
    def process_complex_str(key: str, val: str) -> str:
        if val is not None and len(val) > 0:
            decoded = Deserializer.decode_complex_str(val)
            return f"{key} -- string -- {decoded}"
        return f"{key} -- string -- "

    # ---------------------------
    # Maps
    # ---------------------------
    @staticmethod
    def process_map(map_data: dict) -> None:
        """
        Process a nested nosj map and print lines to stdout.
        Any exception is converted into the required stderr + exit(66).
        """
        try:
            for key, val in map_data.items():
                if not re.match(r"^[a-z]+$", key):
                    raise ValueError(f"Invalid key format: {key}")

                if isinstance(val, str):
                    if re.match(r"^[01]+$", val):
                        print(Deserializer.process_num(key, val))
                    elif re.match(r"^[a-zA-Z0-9 \t]+s$", val):
                        print(Deserializer.process_simple_str(key, val))
                    else:
                        print(Deserializer.process_complex_str(key, val))

                elif isinstance(val, dict):
                    # Map header for this key
                    print(f"{key} -- map -- ")
                    print("begin-map")
                    Deserializer.process_map(val)   # recurse
                    print("end-map")

                else:
                    # Unknown type in the input structure
                    raise ValueError(f"Unsupported value type for key '{key}': {type(val).__name__}")

        except Exception as e:
            # Convert *any* error into the professor-mandated format
            Deserializer.handle_error(str(e))
