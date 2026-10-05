import sqlite3
from pathlib import Path

DB_PATH = Path("data/academic_records.sqlite")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = [
    "students",
    "academic_records",
    "courses",
    "subjects"
]

print("=== DATABASE VERIFICATION ===")

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count}")

print("\n=== SAMPLE STUDENTS ===")

cursor.execute("""
    SELECT student_id, name, department, year, semester
    FROM students
    LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

print("\n=== SAMPLE ACADEMIC RECORDS ===")

cursor.execute("""
    SELECT
        ar.student_id,
        s.name,
        ar.subject_code,
        ar.attendance,
        ar.total_marks,
        ar.grade
    FROM academic_records ar
    JOIN students s
        ON ar.student_id = s.student_id
    LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()

print("\nDatabase verification completed.")