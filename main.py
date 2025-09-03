#!/usr/bin/env python3
import sys, json
from Deserializer.deserializer import Deserializer

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR -- Usage: main.py <inputfile>\n")
        sys.exit(66)

    try:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
        Deserializer.process_map(data)
    except Exception as e:
        sys.stderr.write(f"ERROR -- {e}\n")
        sys.exit(66)

if __name__ == "__main__":
    main()
