import subprocess
import sys

def run():
    print("Running verify_backend.py and capturing output...")
    try:
        result = subprocess.run([sys.executable, "backend/verify_backend.py"], 
                               capture_output=True, text=True, timeout=30)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        print(f"Exit code: {result.returncode}")
    except Exception as e:
        print(f"Failed to run: {e}")

if __name__ == "__main__":
    run()
