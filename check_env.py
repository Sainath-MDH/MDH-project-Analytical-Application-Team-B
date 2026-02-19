import sys
import os

print("-" * 50)
print("PYTHON ENVIRONMENT DIAGNOSTICS")
print("-" * 50)
print(f"Python Executable: {sys.executable}")
print(f"Python Version:    {sys.version}")
print(f"Current Directory: {os.getcwd()}")
print("-" * 50)
print("SEARCH PATHS (sys.path):")
for path in sys.path:
    print(f"  - {path}")
print("-" * 50)

