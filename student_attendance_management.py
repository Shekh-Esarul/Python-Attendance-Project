"""Student Attendance Management System

A beginner-friendly, menu-driven Python project that stores data in CSV files.
The project uses only Python's standard library (no pip installation needed).
"""

import csv
import re
import shutil
from datetime import date
from pathlib import Path

# CSV files are stored beside this Python file.
BASE_DIR = Path(__file__).resolve().parent
STUDENTS_FILE = BASE_DIR / "students.csv"
ATTENDANCE_FILE = BASE_DIR / "attendance.csv"

# All students belong to the same department in this project.
DEPARTMENT = "B.tech CSE (CYS)"
STUDENT_CODE_PREFIX = "BWU/"
STUDENT_CODE_SUFFIX_PATTERN = re.compile(r"^[A-Z0-9]{3}/[A-Z0-9]{2}/[A-Z0-9]{3}$")

STUDENT_FIELDS = ["Student Code", "Name", "Department"]
ATTENDANCE_FIELDS = ["Student Code", "Date", "Status"]
DEFAULT_ATTENDANCE_LIMIT = 75.0


def write_csv_file(file_path, fieldnames, rows):
    """Write CSV data safely using a temporary file, then replace the old file."""
    temporary_path = file_path.with_suffix(file_path.suffix + ".tmp")
    with open(temporary_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary_path.replace(file_path)


def ensure_csv_files():
    """Create CSV files and upgrade older files that used the heading 'Roll'."""
    if not STUDENTS_FILE.exists() or STUDENTS_FILE.stat().st_size == 0:
        write_csv_file(STUDENTS_FILE, STUDENT_FIELDS, [])
    else:
        with open(STUDENTS_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            old_rows = list(reader)

        converted_rows = []
        for row in old_rows:
            student_code = (row.get("Student Code") or row.get("Roll") or "").strip()
            name = (row.get("Name") or "").strip()
            if student_code and name:
                converted_rows.append({
                    "Student Code": student_code,
                    "Name": name,
                    "Department": DEPARTMENT,
                })

        needs_upgrade = headers != STUDENT_FIELDS or any(
            (row.get("Department") or "").strip() != DEPARTMENT
            for row in old_rows
        )
        if needs_upgrade:
            backup_path = STUDENTS_FILE.with_suffix(STUDENTS_FILE.suffix + ".bak")
            if not backup_path.exists():
                shutil.copy2(STUDENTS_FILE, backup_path)
            write_csv_file(STUDENTS_FILE, STUDENT_FIELDS, converted_rows)

    if not ATTENDANCE_FILE.exists() or ATTENDANCE_FILE.stat().st_size == 0:
        write_csv_file(ATTENDANCE_FILE, ATTENDANCE_FIELDS, [])
    else:
        with open(ATTENDANCE_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            old_rows = list(reader)

        converted_rows = []
        for row in old_rows:
            student_code = (row.get("Student Code") or row.get("Roll") or "").strip()
            attendance_date = (row.get("Date") or "").strip()
            status = (row.get("Status") or "").strip().upper()
            if student_code and attendance_date and status in ("P", "A"):
                try:
                    date.fromisoformat(attendance_date)
                except ValueError:
                    continue
                converted_rows.append({
                    "Student Code": student_code,
                    "Date": attendance_date,
                    "Status": status,
                })

        if headers != ATTENDANCE_FIELDS:
            backup_path = ATTENDANCE_FILE.with_suffix(ATTENDANCE_FILE.suffix + ".bak")
            if not backup_path.exists():
                shutil.copy2(ATTENDANCE_FILE, backup_path)
            write_csv_file(ATTENDANCE_FILE, ATTENDANCE_FIELDS, converted_rows)


def load_students():
    """Read student records from students.csv."""
    students = []
    with open(STUDENTS_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_code = (row.get("Student Code") or row.get("Roll") or "").strip()
            name = (row.get("Name") or "").strip()
            if student_code and name:
                students.append({
                    "student_code": student_code,
                    "name": name,
                    "department": DEPARTMENT,
                })
    return students


def load_attendance():
    """Read valid attendance records from attendance.csv."""
    records = []
    with open(ATTENDANCE_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_code = (row.get("Student Code") or row.get("Roll") or "").strip()
            attendance_date = (row.get("Date") or "").strip()
            status = (row.get("Status") or "").strip().upper()

            if student_code and status in ("P", "A"):
                try:
                    date.fromisoformat(attendance_date)
                except ValueError:
                    continue
                records.append({
                    "student_code": student_code,
                    "date": attendance_date,
                    "status": status,
                })
    return records


def ask_new_student_code():
    """Ask for the part after BWU/ and build a code in BWU/XXX/XX/XXX format."""
    while True:
        entered_code = input(
            "Enter Student Code : BWU/"
        ).strip().upper()

        if not entered_code:
            print("Student code cannot be empty. Please try again.")
            continue

        # Also accept a complete code if the user pastes BWU/ at the beginning.
        if entered_code.startswith(STUDENT_CODE_PREFIX):
            entered_code = entered_code[len(STUDENT_CODE_PREFIX):]

        if STUDENT_CODE_SUFFIX_PATTERN.fullmatch(entered_code):
            return STUDENT_CODE_PREFIX + entered_code

        print("Invalid format. Please enter exactly XXX/XX/XXX, for example BCC/25/063.")


def ask_code_for_search():
    """Accept a full student code or just its part after BWU/."""
    entered_code = input(
        "Enter Student Code (example: BCC/25/063 or BWU/BCC/25/063): "
    ).strip().upper()

    if entered_code and not entered_code.startswith(STUDENT_CODE_PREFIX):
        # Preserve old numeric roll numbers so older CSV records can still be searched.
        if "/" in entered_code:
            entered_code = STUDENT_CODE_PREFIX + entered_code

    return entered_code


def get_student_attendance(student_code, attendance_records=None):
    """Calculate total, present, absent and percentage for one student."""
    if attendance_records is None:
        attendance_records = load_attendance()

    student_records = [
        record for record in attendance_records
        if record["student_code"].casefold() == student_code.casefold()
    ]

    total_classes = len(student_records)
    present_classes = sum(1 for record in student_records if record["status"] == "P")
    absent_classes = total_classes - present_classes
    percentage = (present_classes / total_classes * 100) if total_classes else 0.0

    return total_classes, present_classes, absent_classes, percentage


def add_student():
    """Register a student. The department is fixed for the whole class."""
    print("\n--- ADD NEW STUDENT ---")
    students = load_students()
    student_code = ask_new_student_code()

    for student in students:
        if student["student_code"].casefold() == student_code.casefold():
            print("A student with this Student Code already exists!")
            return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Student name cannot be empty. Student was not added.")
        return

    with open(STUDENTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=STUDENT_FIELDS)
        writer.writerow({
            "Student Code": student_code,
            "Name": name,
            "Department": DEPARTMENT,
        })

    print("\nStudent added successfully!")
    print("Student Code:", student_code)
    print("Name:", name)
    print("Department:", DEPARTMENT)


def get_attendance_date():
    """Ask for a date; use today's date when the user presses Enter."""
    today = date.today().isoformat()

    while True:
        entered_date = input(
            f"Enter attendance date (YYYY-MM-DD) [Enter for {today}]: "
        ).strip()
        selected_date = entered_date or today

        try:
            parsed_date = date.fromisoformat(selected_date)
            if parsed_date > date.today():
                print("Future dates are not allowed. Please enter today or an earlier date.")
                continue
            return parsed_date.isoformat()
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD, for example 2026-10-31.")


def mark_attendance():
    """Mark every registered student's attendance for one class date."""
    print("\n--- MARK ATTENDANCE ---")
    students = load_students()

    if not students:
        print("No students registered. Please add students first.")
        return

    attendance_date = get_attendance_date()
    attendance_records = load_attendance()
    already_marked_dates = {record["date"] for record in attendance_records}

    if attendance_date in already_marked_dates:
        print(f"Attendance for {attendance_date} has already been marked.")
        print("This prevents duplicate attendance for the same class date.")
        return

    print(f"\nMark attendance for {attendance_date}")
    print("Enter P for Present or A for Absent.\n")

    new_records = []
    for student in students:
        while True:
            status = input(
                f"{student['student_code']} | {student['name']} (P/A): "
            ).strip().upper()

            if status in ("P", "A"):
                new_records.append({
                    "Student Code": student["student_code"],
                    "Date": attendance_date,
                    "Status": status,
                })
                break

            print("Invalid input. Please enter only P or A.")

    # Save after all students have been marked, so the session is not half-saved.
    with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ATTENDANCE_FIELDS)
        writer.writerows(new_records)

    print("\nAttendance marked and saved successfully!")


def display_student_table(students, title="STUDENT RECORDS"):
    """Print an aligned table with columns sized to fit the actual values."""
    if not students:
        print("No students registered yet.")
        return

    attendance_records = load_attendance()
    headers = ["Student Code", "Name", "Department", "Total", "Present", "Absent", "Attendance"]
    rows = []

    for student in students:
        total, present, absent, percentage = get_student_attendance(
            student["student_code"], attendance_records
        )
        rows.append([
            student["student_code"],
            student["name"],
            DEPARTMENT,
            str(total),
            str(present),
            str(absent),
            f"{percentage:.2f}%",
        ])

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]
    table_width = sum(widths) + (3 * (len(headers) - 1))

    print("\n" + "=" * table_width)
    print(title.center(table_width))
    print("=" * table_width)
    print(" | ".join(headers[index].ljust(widths[index]) for index in range(len(headers))))
    print("-+-".join("-" * width for width in widths))

    for row in rows:
        formatted_cells = []
        for index, value in enumerate(row):
            if index >= 3:
                formatted_cells.append(value.rjust(widths[index]))
            else:
                formatted_cells.append(value.ljust(widths[index]))
        print(" | ".join(formatted_cells))

    print("=" * table_width)


def calculate_attendance():
    """Show attendance totals and percentages for all students."""
    students = load_students()
    display_student_table(students, "ATTENDANCE SUMMARY")
    if students:
        print("Formula: (Present Classes / Total Classes) x 100")


def get_attendance_limit():
    """Get a valid attendance threshold from 0 to 100."""
    while True:
        entered_limit = input(
            f"Enter minimum attendance percentage [default {DEFAULT_ATTENDANCE_LIMIT:g}%]: "
        ).strip()

        if not entered_limit:
            return DEFAULT_ATTENDANCE_LIMIT

        try:
            limit = float(entered_limit)
            if 0 <= limit <= 100:
                return limit
            print("Please enter a number from 0 to 100.")
        except ValueError:
            print("Please enter a valid number, for example 75.")


def show_low_attendance_students():
    """Display students whose attendance is below the selected limit."""
    students = load_students()
    if not students:
        print("No students registered yet.")
        return

    limit = get_attendance_limit()
    attendance_records = load_attendance()
    low_attendance_students = []

    for student in students:
        _, _, _, percentage = get_student_attendance(
            student["student_code"], attendance_records
        )
        if percentage < limit:
            low_attendance_students.append(student)

    if not low_attendance_students:
        print(f"\nNo students are below {limit:g}% attendance.")
        return

    print(f"\nStudents below {limit:g}% attendance:")
    display_student_table(low_attendance_students, "LOW ATTENDANCE STUDENTS")


def search_student():
    """Find one student using their Student Code."""
    print("\n--- SEARCH STUDENT ---")
    student_code = ask_code_for_search()

    if not student_code:
        print("Please enter a Student Code.")
        return

    found_student = None
    for student in load_students():
        if student["student_code"].casefold() == student_code.casefold():
            found_student = student
            break

    if found_student is None:
        print("Student not found.")
        return

    total, present, absent, percentage = get_student_attendance(found_student["student_code"])

    print("\nStudent Found!")
    print("Student Code:", found_student["student_code"])
    print("Name:", found_student["name"])
    print("Department:", DEPARTMENT)
    print("Total Classes:", total)
    print("Present:", present)
    print("Absent:", absent)
    print(f"Attendance: {percentage:.2f}%")

    if total == 0:
        print("No attendance has been marked for this student yet.")


def main():
    """Display the menu and run the selected feature."""
    ensure_csv_files()

    while True:
        print("\n============================================")
        print("       STUDENT ATTENDANCE MANAGEMENT")
        print("============================================")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. Calculate Attendance")
        print("4. Low Attendance Students")
        print("5. Search Student")
        print("6. View All Students")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            calculate_attendance()
        elif choice == "4":
            show_low_attendance_students()
        elif choice == "5":
            search_student()
        elif choice == "6":
            display_student_table(load_students())
        elif choice == "7":
            print("Thank you for using Student Attendance Management System!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
