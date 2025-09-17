
#!/usr/bin/env python3
"""
Partial SHA-256 collision finder (last N bytes match) with required I/O contract.

- Both inputs to SHA256 begin with the provided Auburn root email address.
- Finds a collision on the trailing N bytes of the SHA256 digest (default: 4 bytes).
- Non-deterministic: each run uses a fresh random salt so the resulting inputs differ run-to-run.
- Stdout: exactly two lines, in this format (Linux line endings):
    INPUT 1 -- <BASE64 of first input>\n
    INPUT 2 -- <BASE64 of second input>\n
- Everything else (progress, status) goes to stderr.
- Exit code: 0 on success. (Any other exit means failure.)

Recommended usage on commodity hardware:
    python3 collision_sha256.py --email aat0034@auburn.edu --threads 4

Notes:
- hashlib (C-accelerated) releases the GIL for sha256 updates, so Python threads can help here.
- Trailing-byte width is configurable via --bytes, but the assignment specifies 4 bytes.
"""

import argparse
import base64
import hashlib
import os
import queue
import random
import signal
import sys
import threading
import time
from typing import Optional, Tuple

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class CollisionFinder:
    def __init__(self, email: bytes, last_n: int = 4, threads: int = 4, progress_every: int = 200_000):
        if b'@auburn.edu' not in email:
            raise ValueError("Email must be an Auburn root email (contain '@auburn.edu').")
        if last_n < 1 or last_n > 32:
            raise ValueError("last_n must be between 1 and 32.")
        self.email = email
        self.last_n = last_n
        self.threads = max(1, threads)
        self.progress_every = progress_every

        # Non-deterministic salt unique per run to guarantee different outputs each execution.
        self.run_salt = os.urandom(16)
        # Short marker for the input layout; also ensures uniqueness across runs
        self.salt_tag = base64.urlsafe_b64encode(self.run_salt)[:10]

        # Shared state
        self.stop_evt = threading.Event()
        self.lock = threading.Lock()
        self.map = {}  # last_n_bytes -> first_input_bytes
        self.total_hashes = 0
        self.found_pair: Optional[Tuple[bytes, bytes]] = None

    def _prefix(self) -> bytes:
        # Ensure both inputs *begin with* the root email address
        # Layout: <email> | "||" | salt_tag | "|" | (variable random tail)
        return self.email + b'||' + self.salt_tag + b'|'

    def _worker(self, tid: int):
        prefix = self._prefix()
        rng = random.Random(os.urandom(16))
        local_count = 0
        try:
            while not self.stop_evt.is_set():
                # Variable-length random tail (to vary message sizes and content)
                # Keep tails reasonably small to keep hashing fast
                tail_len = rng.randint(6, 18)
                tail = os.urandom(tail_len)

                msg = prefix + tail
                digest = hashlib.sha256(msg).digest()
                key = digest[-self.last_n:]

                with self.lock:
                    self.total_hashes += 1
                    if key in self.map:
                        other = self.map[key]
                        if other != msg:
                            self.found_pair = (other, msg)
                            self.stop_evt.set()
                            return
                    else:
                        self.map[key] = msg

                    local_count += 1
                    if self.total_hashes % self.progress_every == 0:
                        # Progress log to stderr only
                        eprint(f"[{time.strftime('%H:%M:%S')}] hashes={self.total_hashes:,} "
                               f"unique={len(self.map):,} threads={self.threads} "
                               f"width={self.last_n}B keyspace≈{256**self.last_n:,}")
        except Exception as ex:
            # Any unexpected error should stop the search and surface non-zero exit
            self.stop_evt.set()
            raise

    def run(self) -> Tuple[bytes, bytes]:
        eprint(f"Starting search: trailing={self.last_n} bytes, threads={self.threads}")
        eprint(f"Run salt tag: {self.salt_tag.decode('ascii', errors='ignore')}")
        threads = [threading.Thread(target=self._worker, args=(i,), daemon=True) for i in range(self.threads)]
        for t in threads: t.start()

        # Wait loop
        try:
            while not self.stop_evt.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            eprint("Interrupted by user.")
            self.stop_evt.set()
            for t in threads: t.join(timeout=0.2)
            sys.exit(1)

        for t in threads: t.join()

        if not self.found_pair:
            raise RuntimeError("Stopped without finding a collision (unexpected).")
        return self.found_pair

def b64(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')

def main(argv=None):
    parser = argparse.ArgumentParser(description="Find a partial SHA-256 collision where both inputs begin with a given Auburn email.")
    parser.add_argument("--email", required=True, help="Root Auburn email address (e.g., aat0034@auburn.edu)")
    parser.add_argument("--bytes", type=int, default=4, help="Number of trailing bytes of the SHA-256 digest to collide (default: 4)")
    parser.add_argument("--threads", type=int, default=max(1, os.cpu_count() or 1), help="Number of worker threads (default: CPU count)")
    parser.add_argument("--progress-every", type=int, default=200_000, help="Log progress to stderr every N total hashes")
    args = parser.parse_args(argv)

    email_bytes = args.email.encode("utf-8")
    finder = CollisionFinder(email=email_bytes, last_n=args.bytes, threads=args.threads, progress_every=args.progress_every)
    m1, m2 = finder.run()

    # OUTPUT CONTRACT: exactly two lines to stdout, each prefixed and Base64 encoded (Linux newlines)
    sys.stdout.write(f"INPUT 1 -- {b64(m1)}\n")
    sys.stdout.write(f"INPUT 2 -- {b64(m2)}\n")
    sys.stdout.flush()
    return 0

if __name__ == "__main__":
    sys.exit(main())
