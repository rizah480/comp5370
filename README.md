# NOSJ Deserializer

## Overview
This project implements a **NOSJ deserializer** that parses `.input` files and produces normalized output according to the assignment specification.

- On **success**, output is written to **stdout**:
  ```
  begin-map
  key -- type -- value
  end-map
  ```
- On **error**, the program prints exactly one line to **stderr**:
  ```
  ERROR -- <message>
  ```
  and exits with status code **66**.
- No partial output is written to stdout when errors occur.

---

## File Structure
```
submission/
├── main.py                  # CLI entrypoint (with shebang for Linux)
├── Makefile                 # Provides 'make run FILE=...' target
├── Deserializer/
│   └── deserializer.py      # Core Deserializer implementation
└── README.md                # Project documentation
```

---

## Requirements
- Python **3.10+** (tested with Python 3.12)
- No external libraries required (only Python’s standard library is used)

---

## Usage

### Run manually
```bash
python3 main.py spec-testcases/valid/0001.input
```

### Run with Makefile
```bash
make run FILE=spec-testcases/valid/0001.input
```

---

## Example

**Input** (`0001.input`):
```
(<a:1010>)
```

**Output** (`0001.output`):
```
begin-map
a -- num -- -6
end-map
```

---

## Error Handling Example

**Invalid Input**:
```
(<a :1010>)
```

**Run**:
```bash
python3 main.py spec-testcases/invalid/0001.input
```

**stderr**:
```
ERROR -- Invalid key format: a 
```

**Exit code**:
```
66
```

---

## Testing with Auto-Runner
If provided with `auto-runner.py` and `spec-testcases/`, you can verify the implementation:

```bash
python3 auto-runner.py
```

This runs all professor-supplied valid and invalid cases against your code.

---

## Notes
- Only Python’s **standard library** modules are used:  
  `sys`, `os`, `io`, `contextlib`, `re`, and `urllib.parse`.
- The `Makefile` is configured for Linux/macOS graders (using `./main.py` with shebang) and also works in Windows environments.
