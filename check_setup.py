"""Run this before class:  python check_setup.py

It checks that your laptop is ready for the workshop.
"""

import importlib
import shutil
import socket
import subprocess
import sys

problems = []


def ok(message):
    print(f"[OK]  {message}")


def fix(message, how):
    problems.append(message)
    print(f"[FIX] {message}")
    print(f"      -> {how}")


# 1. Python version
version = sys.version.split()[0]
if sys.version_info >= (3, 11):
    ok(f"Python {version}")
else:
    fix(f"Python {version} is too old", "Install Python 3.11 or newer from https://www.python.org")

# 2. Packages
packages_ok = True
for package in ["fastapi", "uvicorn", "pytest", "httpx"]:
    try:
        importlib.import_module(package)
        ok(f"{package} is installed")
    except ImportError:
        packages_ok = False
        fix(f"{package} is missing", "Run: python -m pip install -r requirements.txt")

# 3. Git
if shutil.which("git") is None:
    fix("Git is not installed", "Install Git from https://git-scm.com")
else:
    for key in ["user.name", "user.email"]:
        result = subprocess.run(["git", "config", key], capture_output=True, text=True)
        if result.stdout.strip():
            ok(f"git {key} is set")
        else:
            fix(f"git {key} is not set", f'Run: git config --global {key} "your {key.split(".")[1]}"')

# 4. Port 8000
with socket.socket() as connection:
    if connection.connect_ex(("127.0.0.1", 8000)) == 0:
        fix("Port 8000 is already in use", "Stop the other program, or add --port 8001 when you run the app")
    else:
        ok("Port 8000 is free")

# 5. The app loads
if packages_ok:
    try:
        from app.main import app  # noqa: F401

        ok("The app loads")
    except Exception as error:
        fix(f"The app does not load: {error}", "Ask for help and share this message")

print()
if problems:
    print(f"{len(problems)} thing(s) to fix. See the [FIX] lines above.")
    sys.exit(1)
print("All good. You're ready for the workshop!")
