import sqlite3
from pathlib import Path


DB_PATH = Path("data/academic_records.sqlite")


def test_database_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    expected_counts = {
        "students": 200,
        "academic_records": 200,
        "courses": 4,
        "subjects": 8,
    }

    for table, expected in expected_counts.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        actual = cursor.fetchone()[0]

        assert actual == expected, (
            f"{table}: expected {expected}, got {actual}"
        )

    conn.close()