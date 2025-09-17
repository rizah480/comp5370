# Makefile in partial-collision/
# Always (re)generate inputs, then verify.
# Targets: make run | make verify | make clean

PYTHON  := python3
SCRIPT  := src/collision_sha256.py
EMAIL   := aat0034@auburn.edu
THREADS ?= 4

INPUT1  := 1-input.txt
DIGEST1 := 1-sha256-digest.txt
INPUT2  := 2-input.txt
DIGEST2 := 2-sha256-digest.txt
OUT     := out.txt

.PHONY: all run verify clean
all: run

run:
	@echo "Running collision finder with $(THREADS) threads..."
	@$(PYTHON) $(SCRIPT) --email $(EMAIL) --threads $(THREADS) > $(OUT)
	@awk -F' -- ' '/^INPUT 1/ {print $$2}' $(OUT) > $(INPUT1)
	@awk -F' -- ' '/^INPUT 2/ {print $$2}' $(OUT) > $(INPUT2)
	@base64 -d $(INPUT1) | sha256sum | awk '{print $$1}' > $(DIGEST1)
	@base64 -d $(INPUT2) | sha256sum | awk '{print $$1}' > $(DIGEST2)

verify: run
	@echo "Verifying collision..."
	@$(PYTHON) -c 'import base64,hashlib,sys; \
m1=base64.b64decode(open("$(INPUT1)").read().strip()); \
m2=base64.b64decode(open("$(INPUT2)").read().strip()); \
d1=hashlib.sha256(m1).digest(); d2=hashlib.sha256(m2).digest(); \
ok_email=m1.startswith(b"$(EMAIL)") and m2.startswith(b"$(EMAIL)"); \
ok_tail=d1[-4:]==d2[-4:]; \
print("Both start with email:", ok_email); \
print("SHA256 last 4 equal?:", ok_tail, d1[-4:].hex(), d2[-4:].hex()); \
sys.exit(0 if (ok_email and ok_tail) else 1)'

clean:
	@rm -f $(INPUT1) $(DIGEST1) $(INPUT2) $(DIGEST2) $(OUT)
