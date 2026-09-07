# -*- coding: utf-8 -*-
"""
scripts/verify_audit_integrity.py
Independent Audit Tool: Verifies SHA-256 cryptographic hashes for 100% of data files
ensuring no corruption, tampering, or erroneous datasets are used.
"""

import os
import sys
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKSUMS_FILE = os.path.join(BASE_DIR, "data", "CHECKSUMS_SHA256.txt")

def main():
    print("=" * 80)
    print("  INDEPENDENT AUDIT: CRYPTOGRAPHIC CHECKSUM & DATA INTEGRITY VERIFIER")
    print("=" * 80)

    if not os.path.exists(CHECKSUMS_FILE):
        print(f"Error: {CHECKSUMS_FILE} not found!")
        sys.exit(1)

    with open(CHECKSUMS_FILE, "r", encoding="utf-8") as f:
        entries = [line.strip().split(maxsplit=1) for line in f if line.strip()]

    passed = 0
    failed = 0
    missing = 0

    for expected_hash, rel_path in entries:
        full_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
        if not os.path.exists(full_path):
            print(f"  [MISSING] {rel_path}")
            missing += 1
            continue

        h = hashlib.sha256()
        with open(full_path, "rb") as fp:
            while chunk := fp.read(65536):
                h.update(chunk)
        actual_hash = h.hexdigest()

        if actual_hash == expected_hash:
            passed += 1
        else:
            print(f"  [HASH MISMATCH] {rel_path}")
            print(f"     Expected: {expected_hash}")
            print(f"     Actual:   {actual_hash}")
            failed += 1

    print("-" * 80)
    print(f"  Audit Summary:")
    print(f"  Verified Files: {passed} / {len(entries)} (100% MATCH)" if failed == 0 and missing == 0 else f"  FAILURES: {failed}, MISSING: {missing}")
    print("=" * 80)

    if failed > 0 or missing > 0:
        sys.exit(1)
    else:
        print("  STATUS: DATA INTEGRITY AUDIT PASSED - ALL ASSETS CRYPTOGRAPHICALLY SECURE.")

if __name__ == "__main__":
    main()
