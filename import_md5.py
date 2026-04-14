import re
import sqlite3
import sys
from pathlib import Path


DB_PATH = Path("hashes.db")
INPUT_PATH = Path("md5_raw_data.txt")
MD5_PATTERN = re.compile(r"^[0-9a-fA-F]{32}$")


def import_md5_hashes() -> None:
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
            hash_value = raw_line.strip()
            if not hash_value:
                continue

            lines += 1
            if not MD5_PATTERN.fullmatch(hash_value):
                skipped_invalid += 1
                continue

            try:
                cursor.execute(
                    "INSERT INTO md5_hashes (hash_value) VALUES (?)",
                    (hash_value.lower(),),
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
    import_md5_hashes()
