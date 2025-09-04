#!/usr/bin/env python3
import sys
import os
import io
from contextlib import redirect_stdout

# --- normalize line endings so auto-runner byte compare passes ---
try:
    sys.stdout.reconfigure(newline="\n")
    sys.stderr.reconfigure(newline="\n")
except Exception:
    pass

# --- robust import for Deserializer ---
try:
    from Deserializer.deserializer import Deserializer
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "Deserializer"))
    from deserializer import Deserializer  # type: ignore


# ---------------- STRICT NOSJ PARSER (rubric-compliant) ----------------
# Grammar:
#   file  := WS? "(<" pairs? ">)" WS?
#   pairs := pair ("," pair)*
#   pair  := key ":" value
#   key   := [a-z]+          (no whitespace allowed)
#   value := map | strtoken
#   map   := "(<" pairs? ">)"
#   strtoken := sequence of ANY chars except ',' or '>' or ')'
#               (may contain spaces, e.g. simple strings like "b s")
#
# Rules:
# - No whitespace inside a map except inside a string token itself.
# - Keys must be lowercase ascii only, no spaces allowed.
# - Whitespace allowed only outside the top-level map or inside string tokens.

class NosjParser:
    def __init__(self, src: str):
        self.s = src
        self.i = 0
        self.n = len(src)

    def parse(self):
        self._skip_outer_ws()
        obj = self._parse_map()
        self._skip_outer_ws()
        if self.i != self.n:
            self._err("Trailing characters after top-level map")
        return obj

    def _parse_map(self):
        self._expect('(')
        self._expect('<')
        result = {}
        # Allow empty map "(<>)"
        if self._peek_is('>'):
            self._advance()
            self._expect(')')
            return result

        # parse first pair
        k, v = self._parse_pair()
        result[k] = v

        # optional more pairs
        while self._peek_is(','):
            self._advance()
            k, v = self._parse_pair()
            result[k] = v

        self._expect('>')
        self._expect(')')
        return result

    def _parse_pair(self):
        key = self._parse_key()
        self._expect(':')
        val = self._parse_value()
        return key, val

    def _parse_key(self):
        start = self.i
        while self.i < self.n and 'a' <= self.s[self.i] <= 'z':
            self.i += 1
        if self.i == start:
            self._err("Expected lowercase key")
        return self.s[start:self.i]

    def _parse_value(self):
        if self._peek_is('('):
            return self._parse_map()
        start = self.i
        while self.i < self.n:
            ch = self.s[self.i]
            if ch in ',>)':
                break
            self.i += 1
        return self.s[start:self.i]

    # ---------------- helpers ----------------
    def _skip_outer_ws(self):
        while self.i < self.n and self.s[self.i] in ' \t\r\n':
            self.i += 1

    def _peek_is(self, ch):
        return self.i < self.n and self.s[self.i] == ch

    def _expect(self, ch):
        if not self._peek_is(ch):
            got = self.s[self.i] if self.i < self.n else "EOF"
            self._err(f"Expected '{ch}' but found '{got}'")
        self.i += 1

    def _advance(self):
        self.i += 1

    def _err(self, msg):
        raise ValueError(f"NOSJ parse error: {msg}")


# ---------------- CLI wrapper ----------------
def main():
    if len(sys.argv) != 2:
        Deserializer.handle_error("Usage: main.py <inputfile>")

    try:
        with open(sys.argv[1], "r", newline="") as f:
            src = f.read()

        data = NosjParser(src).parse()

        # Buffer all processed output; only print if everything succeeds.
        buf = io.StringIO()
        with redirect_stdout(buf):
            Deserializer.process_map(data)

        # Success: now emit the wrapped output to real stdout.
        print("begin-map")
        sys.stdout.write(buf.getvalue())
        print("end-map")

    except SystemExit:
        # already handled via Deserializer.handle_error
        raise
    except Exception as e:
        # Ensure no prior stdout leaked (it didn't, we buffered), then standardize error.
        Deserializer.handle_error(str(e))


if __name__ == "__main__":
    main()
