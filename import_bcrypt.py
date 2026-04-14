import re
import sqlite3
import sys
from pathlib import Path


DB_PATH = Path("hashes.db")
INPUT_PATH = Path("bcrypt_raw_data.txt")
BCRYPT_PATTERN = re.compile(r"^\$2[abxy]\$\d{2}\$[./A-Za-z0-9]{53}$")


def import_bcrypt_hashes() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_PATH

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.stat().st_size == 0:
        print(f"Input file is empty: {input_path}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    lines = 0
    inserted = 0
    duplicates = 0
    skipped_invalid = 0

    with input_path.open("r", encoding="utf-8", errors="ignore") as source:
        for raw_line in source:
            line = raw_line.strip()
            if not line:
                continue

            lines += 1
            parts = line.split()

            hash_value = None
            password_raw = None

            if len(parts) == 1:
                candidate = parts[0]
                if BCRYPT_PATTERN.fullmatch(candidate):
                    hash_value = candidate
            else:
                # Expected format: password_raw bcrypt_hash
                first, second = parts[0], parts[1]
                if BCRYPT_PATTERN.fullmatch(second):
                    password_raw = first
                    hash_value = second
                elif BCRYPT_PATTERN.fullmatch(first):
                    hash_value = first

            if not hash_value:
                skipped_invalid += 1
                continue

            try:
                cursor.execute(
                    "INSERT INTO bcrypt_hashes (hash_value, password_raw) VALUES (?, ?)",
                    (hash_value, password_raw),
                )
                inserted += 1
            except sqlite3.IntegrityError:
                duplicates += 1

    conn.commit()
    conn.close()

    print(
        f"lines={lines} inserted={inserted} "
        f"duplicates={duplicates} skipped_invalid={skipped_invalid}"
    )


if __name__ == "__main__":
    import_bcrypt_hashes()
