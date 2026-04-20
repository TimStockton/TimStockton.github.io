"""
Program: batch_rename.py [v1.0.0]
Description: Searches filenames in given directory for given string and replaces with given string.
Author: Timothy Stockton
Created: 20260121

use cases:
    - Rename multiple files requiring the same change
"""

import os
import sys

def batch_rename(directory, find_str, replace_str, dry_run=False):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    renamed = 0

    for filename in os.listdir(directory):
        if find_str not in filename:
            continue

        old_path = os.path.join(directory, filename)
        new_filename = filename.replace(find_str, replace_str)
        new_path = os.path.join(directory, new_filename)

        if old_path == new_path:
            continue

        print(f"{filename}  ->  {new_filename}")

        if not dry_run:
            os.rename(old_path, new_path)

        renamed += 1

    print(f"\nDone. Files renamed: {renamed}")
    if dry_run:
        print("Dry run mode: no files were actually renamed.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage:\n"
            "  python batch_rename.py <directory> <find_string> <replace_string> [--dry-run]\n\n"
            "Example:\n"
            "  python batch_rename.py . \" __Replace_ASAP__\" \" __Lossy_Source__\""
        )
        sys.exit(1)

    target_dir = sys.argv[1]
    find_string = sys.argv[2]
    replace_string = sys.argv[3]
    dry = "--dry-run" in sys.argv

    batch_rename(target_dir, find_string, replace_string, dry_run=dry)
