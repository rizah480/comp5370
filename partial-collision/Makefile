# Makefile living in partial-collision/
# Targets:
#   make run     -> run collision finder and produce input + digest files
#   make verify  -> run correctness checks (email prefix + last 4 bytes collide)
#   make clean   -> remove generated files

PYTHON  := python3
SCRIPT  := src/collision_sha256.py
EMAIL   := aat0034@auburn.edu
THREADS ?= 4

INPUT1  := 1-input.txt
DIGEST1 := 1-sha256-digest.txt
INPUT2  := 2-input.txt
DIGEST2 := 2-sha256-digest.txt
OUT     := out.txt

# Default: run (you can change to 'verify' if you prefer)
all: run

run: $(INPUT1) $(DIGEST1) $(INPUT2) $(DIGEST2)

# Step 1: generate the two Base64 inputs using your script
$(INPUT1) $(INPUT2): $(SCRIPT)
	@echo "Running collision finder with $(THREADS) threads..."
	@$(PYTHON) $(SCRIPT) --email $(EMAIL) --threads $(THREADS) > $(OUT)
	@awk -F' -- ' '/^INPUT 1/ {print $$2}' $(OUT) > $(INPUT1)
	@awk -F' -- ' '/^INPUT 2/ {print $$2}' $(OUT) > $(INPUT2)

# Step 2: compute SHA256 digests for both inputs
$(DIGEST1): $(INPUT1)
	@base64 -d $(INPUT1) | sha256sum | awk '{print $$1}' > $(DIGEST1)

$(DIGEST2): $(INPUT2)
	@base64 -d $(INPUT2) | sha256sum | awk '{print $$1}' > $(DIGEST2)

verify: run
	@echo "Verifying collision..."
	@$(PYTHON) - <<'PY'
import base64, hashlib, sys
EMAIL = b"aat0034@auburn.edu"
m1 = base64.b64decode(open("1-input.txt").read().strip())
m2 = base64.b64decode(open("2-input.txt").read().strip())
d1 = hashlib.sha256(m1).digest()
d2 = hashlib.sha256(m2).digest()
ok_email = m1.startswith(EMAIL) and m2.startswith(EMAIL)
ok_tail = d1[-4:] == d2[-4:]
print("Both start with email:", ok_email)
print("SHA256 last 4 equal?:", ok_tail, d1[-4:].hex(), d2[-4:].hex())
if not (ok_email and ok_tail):
    sys.exit(1)
PY

clean:
	rm -f $(INPUT1) $(DIGEST1) $(INPUT2) $(DIGEST2) $(OUT)
