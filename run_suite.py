#!/usr/bin/env python3
import os, subprocess, sys, glob

PY = os.environ.get("PY", sys.executable)   # override with PY=... if needed
OK = True

def fwd(p: str) -> str:
    return p.replace("\\", "/")

def run_one(input_path, expected_path=None):
    env = dict(os.environ)
    env["PY"] = PY

    in_for_make = fwd(input_path)

    # -s silences make (belt & suspenders, in addition to @ in Makefile)
    p = subprocess.run(
        ["make", "-s", "run", f"FILE={in_for_make}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        env=env,
    )

    out, err, code = p.stdout, p.stderr, p.returncode
    name = os.path.relpath(input_path)

    if expected_path:
        with open(expected_path, "rb") as f:
            exp = f.read()
        if code == 0 and err == b"" and out == exp:
            print(f"OK -- {name}")
            return True
        print(f"FAIL -- {name}")
        print(f"  exit={code}")
        if err:
            print("  stderr:", err.decode("utf-8", "replace").rstrip())
        lim = min(len(out), len(exp))
        for i in range(lim):
            if out[i] != exp[i]:
                print(f"  first byte diff at {i}: got {out[i]:#04x}, exp {exp[i]:#04x}")
                break
        if len(out) != len(exp):
            print(f"  length: got {len(out)}, exp {len(exp)}")
        return False
    else:
        ok = (code != 0) and out == b"" and err.startswith(b"ERROR -- ")
        if ok:
            print(f"OK -- {name}")
        else:
            print(f"FAIL -- {name}")
            print(f"  exit={code}")
            print(f"  stdout={out!r}")
            print(f"  stderr={err!r}")
        return ok

def main():
    global OK
    # VALID
    for ip in sorted(glob.glob("spec-testcases/valid/*.input")):
        OK = run_one(ip, ip.replace(".input", ".output")) and OK
    # INVALID
    for ip in sorted(glob.glob("spec-testcases/invalid/*.input")):
        OK = run_one(ip, None) and OK
    sys.exit(0 if OK else 1)

if __name__ == "__main__":
    main()
