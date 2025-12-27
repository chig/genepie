#!/usr/bin/env python
"""Download test data for integration tests from Google Drive.

Usage:
    python -m genepie.tests.download_test_data

This script downloads the chignolin test data (PDB, PSF, DCD) from Google Drive.
These files are required for running the integration tests (test_integration.py).
"""
# --------------------------------------------
if __name__ == "__main__" and __package__ is None:
    import sys, pathlib
    pkg_dir = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(pkg_dir.parent.parent))
    __package__ = "genepie.tests"
# --------------------------------------------

import subprocess
import pathlib

from .conftest import DATA_DIR

# Google Drive file IDs and filenames
# Download URL format: https://drive.google.com/uc?export=download&id=FILE_ID
FILES = [
    ("1WyFzvhuMjlwp2pNjga9B8RvTKoygBh-a", "chignolin.pdb"),
    ("1L1Y7YdSz46sTI1lQ7PoQJIqqbzM4F9Vh", "chignolin.psf"),
    ("1DZFUbCBVdCsfKzzrroIslre0eSctMaY-", "chignolin.dcd"),
]


def download():
    """Download chignolin test data from Google Drive."""
    data_dir = DATA_DIR / "chignolin"
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading test data to: {data_dir}")
    print()

    for file_id, filename in FILES:
        dest = data_dir / filename
        if dest.exists():
            print(f"[SKIP] {filename} (already exists)")
            continue

        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        print(f"[DOWNLOAD] {filename}...")

        try:
            result = subprocess.run(
                ["curl", "-L", url, "-o", str(dest)],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"  -> {dest}")
        except subprocess.CalledProcessError as e:
            print(f"  [ERROR] Failed to download {filename}")
            print(f"          {e.stderr}")
            # Remove partial file if exists
            if dest.exists():
                dest.unlink()
            continue
        except FileNotFoundError:
            print("  [ERROR] curl command not found. Please install curl.")
            return 1

    print()
    print("Download complete!")
    return 0


def main():
    import sys
    sys.exit(download())


if __name__ == "__main__":
    main()
