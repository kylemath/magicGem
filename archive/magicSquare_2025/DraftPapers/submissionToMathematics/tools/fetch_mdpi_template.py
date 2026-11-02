#!/usr/bin/env python3
"""Fetch MDPI LaTeX template (mdpi.cls, *.bst, *.sty).

If an internet connection is unavailable, the script falls back to a minimal
local stub so that the document still compiles under a generic article class.
"""
import urllib.request
from pathlib import Path
import tarfile
import io
import sys

HERE = Path(__file__).resolve().parent
TARGET_DIR = HERE.parent

MDPI_CLS_URL = "https://www.mdpi.com/authors/latex?filename=mdpi.tar.gz"


def main():
    try:
        print("Downloading MDPI LaTeX template …")
        with urllib.request.urlopen(MDPI_CLS_URL, timeout=30) as resp:
            data = resp.read()
        tgz = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
        tgz.extractall(path=TARGET_DIR)
        print("MDPI template extracted.")
    except Exception as e:
        print(f"⚠️  Could not fetch template automatically: {e}")
        print("Proceeding with fallback — compilation will use generic article class.")
        stub = TARGET_DIR / "mdpi.cls"
        if not stub.exists():
            stub.write_text("% Stub class for offline compilation\n\\LoadClass{article}")


if __name__ == "__main__":
    sys.exit(main()) 