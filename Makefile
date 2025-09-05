
# THIS IF FOR RUNNNING ON WINDOWS
# .PHONY: run

# # Hardcode your python.exe path here:
# PY := C:\Users\aaron\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe

# run:
# 	@"$(PY)" main.py $(FILE)

# Reunion 
# 9/4/2024
# 9/4/2025
.PHONY: run
run:
	@./main.py $(FILE)
