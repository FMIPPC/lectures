import subprocess
import sys


if __name__ == "__main__":
    command = [sys.executable, "-X", "utf8", "-m", "edtrace.execute", *sys.argv[1:]]
    raise SystemExit(subprocess.call(command))
