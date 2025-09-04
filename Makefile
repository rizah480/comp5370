.PHONY: run

# Hardcode your python.exe path here:
PY := C:\Users\aaron\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe

run:
	@"$(PY)" main.py $(FILE)
