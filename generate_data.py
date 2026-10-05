from pathlib import Path
import sqlite3
import random
import csv
from datetime import date, timedelta

SEED = 42
random.seed(SEED)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
POLICY_DIR = DATA / "policies"
COURSE_CONTENT = DATA / "course_content"

DB_PATH = DATA / "academic_records.sqlite"

FIRST_NAMES = [
    "Arun", "Bala", "Charan", "Deepak", "Dinesh", "Hari", "Karthik", "Manoj",
    "Naveen", "Pranav", "Rahul", "Rohit", "Sanjay", "Surya", "Vignesh",
    "Aishwarya", "Ananya", "Divya", "Harini", "Keerthana", "Meena", "Nandhini",
    "Pooja", "Priya", "Riya", "Shreya", "Swetha", "Vaishnavi", "Yamuna", "Zoya"
]

LAST_NAMES = [
    "Kumar", "Raj", "Sharma", "Iyer", "Nair", "Reddy", "Patel", "Singh",
    "Das", "Menon", "Rao", "Pillai", "Bose", "Thomas", "Joseph"
]

COURSES = [
    ("CSE", "B.Tech Computer Science and Engineering", 4),
    ("AIDS", "B.Tech Artificial Intelligence and Data Science", 4),
    ("ECE", "B.Tech Electronics and Communication Engineering", 4),
    ("EEE", "B.Tech Electrical and Electronics Engineering", 4),
]

SUBJECTS = [
    ("CS101", "Programming Fundamentals", 1, 4),
    ("MA101", "Engineering Mathematics I", 1, 4),
    ("CS201", "Data Structures", 2, 4),
    ("DB301", "Database Management Systems", 3, 4),
    ("ML401", "Machine Learning", 4, 4),
    ("AI501", "Artificial Intelligence", 5, 4),
    ("CN601", "Computer Networks", 6, 3),
    ("SE701", "Software Engineering", 7, 3),
]

POLICIES = [
    ("POL001", "Attendance Requirement", "attendance",
     "Students must maintain a minimum attendance of 75 percent in each course."),
    ("POL002", "Attendance Condonation", "attendance",
     "Students with attendance from 65 percent to 74 percent may apply for attendance condonation, subject to approval."),
    ("POL003", "Attendance Shortage", "attendance",
     "Students with attendance below 65 percent are not eligible for attendance condonation."),
    ("POL004", "Attendance Calculation", "attendance",
     "Attendance percentage is calculated from the total eligible instructional hours recorded for the course."),
    ("POL005", "Medical Leave", "leave",
     "Medical leave requests must include valid supporting medical documents and follow the institutional approval process."),
    ("POL006", "Leave Application", "leave",
     "Leave applications should be submitted through the approved institutional process before or immediately after the absence."),
    ("POL007", "Internal Assessment", "assessment",
     "Internal assessment contributes 40 marks to the final course evaluation."),
    ("POL008", "End Semester Examination", "assessment",
     "The end semester examination contributes 60 marks to the final course evaluation."),
    ("POL009", "Passing Requirement", "assessment",
     "A student must satisfy the applicable minimum marks requirement in the course to pass."),
    ("POL010", "Assignment Submission", "assessment",
     "Assignments must be submitted before the deadline specified by the course faculty."),
    ("POL011", "Late Assignment", "assessment",
     "Late assignment submissions may be accepted only when permitted by the course faculty or applicable policy."),
    ("POL012", "Revaluation Request", "examination",
     "Students may submit revaluation requests within the period announced after publication of examination results."),
    ("POL013", "Revaluation Limit", "examination",
     "A revaluation request applies only to eligible courses and must follow the examination office procedure."),
    ("POL014", "Exam Registration", "examination",
     "Students must complete examination registration within the announced registration period."),
    ("POL015", "Exam Eligibility", "examination",
     "Examination eligibility depends on fulfillment of applicable academic and attendance requirements."),
    ("POL016", "Hall Ticket", "examination",
     "Students must obtain the examination hall ticket through the approved institutional process before the examination."),
    ("POL017", "Academic Misconduct", "discipline",
     "Academic misconduct during an examination or assessment is handled according to institutional disciplinary procedures."),
    ("POL018", "Plagiarism", "discipline",
     "Submitted academic work must comply with the institution's academic integrity and plagiarism requirements."),
    ("POL019", "Course Withdrawal", "academic",
     "Course withdrawal requests must be made within the period and procedure specified by the institution."),
    ("POL020", "Course Registration", "academic",
     "Students must register for required courses during the designated registration period."),
    ("POL021", "Credit Requirement", "academic",
     "Students must complete the prescribed credit requirements of their programme for graduation eligibility."),
    ("POL022", "Backlog Examination", "examination",
     "Students with eligible failed courses may register for backlog examinations according to the announced schedule."),
    ("POL023", "Grade Publication", "academic",
     "Course grades are published through the institution's approved result publication process."),
    ("POL024", "Result Correction", "academic",
     "Requests to correct a published academic result must be submitted with supporting evidence through the designated office."),
    ("POL025", "Faculty Consultation", "academic",
     "Students may contact the concerned course faculty during the designated consultation or communication period."),
    ("POL026", "Course Coordinator", "academic",
     "The course coordinator is responsible for coordinating course-level academic activities and communication."),
    ("POL027", "Minimum Credits Per Semester", "academic",
     "Students should follow the prescribed semester-wise credit structure of their programme."),
    ("POL028", "Student Identification", "administration",
     "Students must use their assigned student identification number for academic record and examination processes."),
    ("POL029", "Record Privacy", "administration",
     "Student academic records must be accessed and handled only through authorized institutional processes."),
    ("POL030", "Data Correction Request", "administration",
     "Students may request correction of inaccurate personal or academic information through the designated process."),
    ("POL031", "Library Clearance", "administration",
     "Required library clearance must be completed when applicable to academic or institutional processes."),
    ("POL032", "Laboratory Attendance", "attendance",
     "Laboratory attendance is recorded as part of the applicable course attendance requirements."),
    ("POL033", "Project Evaluation", "assessment",
     "Project evaluation follows the assessment components and criteria communicated for the applicable programme or course."),
    ("POL034", "Internship Credit", "academic",
     "Internship credit is awarded only when the internship satisfies the applicable academic requirements."),
    ("POL035", "Graduation Eligibility", "academic",
     "Graduation eligibility requires completion of prescribed academic, credit, and institutional requirements."),
]

FAQS = [
    ("FAQ001", "What is the minimum attendance requirement?", "The minimum attendance requirement is 75 percent in each course.", "POL001"),
    ("FAQ002", "Can a student with 70 percent attendance apply for condonation?", "A student with attendance from 65 percent to 74 percent may apply for condonation, subject to approval.", "POL002"),
    ("FAQ003", "Is attendance below 65 percent eligible for condonation?", "Students with attendance below 65 percent are not eligible for attendance condonation.", "POL003"),
    ("FAQ004", "How much does internal assessment contribute?", "Internal assessment contributes 40 marks.", "POL007"),
    ("FAQ005", "How much does the end semester exam contribute?", "The end semester examination contributes 60 marks.", "POL008"),
    ("FAQ006", "Can students request revaluation?", "Eligible students may submit revaluation requests within the announced period and procedure.", "POL012"),
    ("FAQ007", "What is required for medical leave?", "Medical leave requests require valid supporting medical documents and follow the approval process.", "POL005"),
    ("FAQ008", "What happens to academic misconduct cases?", "Academic misconduct is handled according to institutional disciplinary procedures.", "POL017"),
    ("FAQ009", "Can students correct inaccurate records?", "Students may request correction through the designated institutional process.", "POL030"),
    ("FAQ010", "What is required for graduation?", "Students must satisfy prescribed academic, credit, and institutional requirements.", "POL035"),
]

def make_database():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE courses (
        course_code TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        duration_years INTEGER NOT NULL
    );

    CREATE TABLE subjects (
        subject_code TEXT PRIMARY KEY,
        subject_name TEXT NOT NULL,
        semester INTEGER NOT NULL,
        credits INTEGER NOT NULL
    );

    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        year INTEGER NOT NULL,
        semester INTEGER NOT NULL,
        email TEXT NOT NULL
    );

    CREATE TABLE academic_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        subject_code TEXT NOT NULL,
        attendance REAL NOT NULL,
        internal_marks REAL NOT NULL,
        end_sem_marks REAL NOT NULL,
        total_marks REAL NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(subject_code) REFERENCES subjects(subject_code)
    );
    """)

    cur.executemany("INSERT INTO courses VALUES (?, ?, ?)", COURSES)
    cur.executemany("INSERT INTO subjects VALUES (?, ?, ?, ?)", SUBJECTS)

    students = []
    records = []

    for i in range(1, 201):
        student_id = f"STU{i:04d}"
        name = f"{FIRST_NAMES[(i-1) % len(FIRST_NAMES)]} {LAST_NAMES[((i-1)//len(FIRST_NAMES)) % len(LAST_NAMES)]}"
        department = COURSES[(i-1) % len(COURSES)][0]
        year = ((i - 1) % 4) + 1
        semester = year * 2 - (1 if i % 2 else 0)
        email = f"{student_id.lower()}@example.edu"
        students.append((student_id, name, department, year, semester, email))

        subject = SUBJECTS[(i - 1) % len(SUBJECTS)]
        attendance = round(random.uniform(62, 98), 1)
        internal = round(random.uniform(22, 39), 1)
        end_sem = round(random.uniform(25, 58), 1)
        total = round(internal + end_sem, 1)

        if total >= 90:
            grade = "A+"
        elif total >= 80:
            grade = "A"
        elif total >= 70:
            grade = "B+"
        elif total >= 60:
            grade = "B"
        elif total >= 50:
            grade = "C"
        else:
            grade = "F"

        records.append((student_id, subject[0], attendance, internal, end_sem, total, grade))

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", students)
    cur.executemany("""
        INSERT INTO academic_records
        (student_id, subject_code, attendance, internal_marks, end_sem_marks, total_marks, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()
    conn.close()

def make_policies():
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    for policy_id, title, category, content in POLICIES:
        text = f"""Policy ID: {policy_id}
Title: {title}
Category: {category}

{content}
"""
        (POLICY_DIR / f"{policy_id}.txt").write_text(text, encoding="utf-8")

def make_faqs():
    faq_path = DATA / "faqs.csv"
    with faq_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["faq_id", "question", "answer", "source_policy_id"])
        writer.writerows(FAQS)

def make_course_content():
    COURSE_CONTENT.mkdir(parents=True, exist_ok=True)
    content = """# Academic Programme Information

This is synthetic benchmark data for the Hallucinators project.

## Programmes
- CSE — B.Tech Computer Science and Engineering — 4 years
- AIDS — B.Tech Artificial Intelligence and Data Science — 4 years
- ECE — B.Tech Electronics and Communication Engineering — 4 years
- EEE — B.Tech Electrical and Electronics Engineering — 4 years

## Subjects
- CS101 — Programming Fundamentals — Semester 1 — 4 credits
- MA101 — Engineering Mathematics I — Semester 1 — 4 credits
- CS201 — Data Structures — Semester 2 — 4 credits
- DB301 — Database Management Systems — Semester 3 — 4 credits
- ML401 — Machine Learning — Semester 4 — 4 credits
- AI501 — Artificial Intelligence — Semester 5 — 4 credits
- CN601 — Computer Networks — Semester 6 — 3 credits
- SE701 — Software Engineering — Semester 7 — 3 credits

All information in this file is synthetic and is intended only for system development and evaluation.
"""
    (COURSE_CONTENT / "academic_information.md").write_text(content, encoding="utf-8")

def main():
    DATA.mkdir(exist_ok=True)
    make_database()
    make_policies()
    make_faqs()
    make_course_content()

    print("Phase 1 data generation complete.")
    print(f"Database: {DB_PATH}")
    print(f"Students: 200")
    print(f"Policies: {len(POLICIES)}")
    print(f"FAQs: {len(FAQS)}")

if __name__ == "__main__":
    main()
