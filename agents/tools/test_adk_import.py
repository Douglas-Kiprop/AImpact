import sys
import os

print("Attempting to import google.adk.tools.FunctionTool...")
try:
    from google.adk.tools import FunctionTool
    print("Successfully imported FunctionTool from google.adk.tools!")
    if hasattr(FunctionTool, '__name__'):
        print(f"FunctionTool name: {FunctionTool.__name__}")
    else:
        print("FunctionTool does not have a __name__ attribute.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\nPython sys.path:")
for p in sys.path:
    print(p)

print("\nPYTHONPATH environment variable:")
python_path = os.environ.get('PYTHONPATH')
if python_path:
    print(python_path)
else:
    print("PYTHONPATH is not set or is empty.")
print(f"sys.executable: {sys.executable}")
print(f"sys.path: {sys.path}")