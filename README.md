# 📋 Student Attendance Management System

A simple, menu-driven **Python** program for taking and tracking class attendance from the terminal.
Built as an internal project at **Brainware University (BWU)** for the **B.Tech CSE (Cyber Security)** class.

> ✅ No installation needed — uses only Python's standard library.
> ✅ No database — everything is stored in two easy-to-open CSV files (Excel / Google Sheets compatible).

---

## 👩‍🏫 For Teachers — Quick Start

1. Install **Python 3.7+** (check with `python --version`).
2. Put these three files in the same folder:
   - `student_attendance_management.py`
   - `students.csv`
   - `attendance.csv`
3. Open a terminal in that folder and run:

   ```bash
   python student_attendance_management.py
   ```

   *(On some systems use `python3` instead of `python`.)*

4. Pick an option from the menu by typing its number and pressing **Enter**.

> 💡 If `students.csv` or `attendance.csv` are missing, the program creates them automatically on first run.

---

## 🧭 Main Menu

```
============================================
       STUDENT ATTENDANCE MANAGEMENT
============================================
1. Add Student
2. Mark Attendance
3. Calculate Attendance
4. Low Attendance Students
5. Search Student
6. View All Students
7. Exit
```

| # | Option | What it does |
|---|--------|--------------|
| 1 | **Add Student** | Registers a new student (code + name). Department is set automatically. |
| 2 | **Mark Attendance** | Takes attendance for **all** students for one date (P / A). |
| 3 | **Calculate Attendance** | Shows total / present / absent classes and attendance % for everyone. |
| 4 | **Low Attendance Students** | Lists students below a minimum % (default **75%**, you can change it). |
| 5 | **Search Student** | Shows one student's full attendance details by Student Code. |
| 6 | **View All Students** | Shows the full class table with attendance summary. |
| 7 | **Exit** | Closes the program. |

---

## 📖 How to Use Each Feature

### 1️⃣ Add Student

- The program already shows `BWU/` — you type only the rest, in the format **`XXX/XX/XXX`**.
- Example: type `BCC/25/063` → saved as `BWU/BCC/25/063`.
- You may also paste the full code (`BWU/BCC/25/063`); it works too.
- Letters are auto-converted to capitals.
- Duplicate Student Codes are rejected.
- Student name cannot be empty.

### 2️⃣ Mark Attendance

1. Enter the class date as `YYYY-MM-DD`, or just press **Enter** to use **today's date**.
2. For each student, type **`P`** (Present) or **`A`** (Absent).
3. After the last student, everything is saved at once.

**Rules to remember:**

| Rule | Why |
|------|-----|
| ❌ Future dates are not allowed | Prevents marking by mistake |
| ❌ One attendance session per date | If a date is already marked, the program refuses to mark it again (no duplicates) |
| ✅ Only `P` or `A` accepted | Any other key asks again |
| ✅ Saved only after all students are marked | No half-saved sessions |

> ⚠️ Because a date can only be marked once, **take attendance only after all students are registered**. A student added later will have no record for earlier dates.

### 3️⃣ Calculate Attendance

Shows a table for the whole class:

```
Student Code   | Name                 | Department       | Total | Present | Absent | Attendance
---------------+----------------------+------------------+-------+---------+--------+-----------
BWU/BCC/25/063 | Esarul Shekh         | B.tech CSE (CYS) |     3 |       1 |      2 |     33.33%
BWU/BCC/25/065 | Ishita Kundu         | B.tech CSE (CYS) |     3 |       3 |      0 |    100.00%
BWU/BCC/25/066 | Snehasis Gain        | B.tech CSE (CYS) |     3 |       2 |      1 |     66.67%
BWU/BCC/25/074 | Munshi Javed Hossain | B.tech CSE (CYS) |     0 |       0 |      0 |      0.00%
```

**Formula:**

```
Attendance % = (Present Classes ÷ Total Classes) × 100
```

### 4️⃣ Low Attendance Students

- Enter a minimum percentage (0–100), or press **Enter** to use the default **75%**.
- Every student **below** that percentage is listed — handy for warnings, notices, or exam-eligibility checks.
- Students with **no classes recorded yet** show **0.00%**, so they also appear in this list.

### 5️⃣ Search Student

Enter a Student Code (`BCC/25/063` or `BWU/BCC/25/063`) to see that student's name, department, total classes, present, absent and attendance %.

### 6️⃣ View All Students

Same table as option 3, titled **STUDENT RECORDS**.

---

## 🗂️ Data Files (Editable in Excel / Google Sheets)

### `students.csv`

| Student Code | Name | Department |
|---|---|---|
| BWU/BCC/25/063 | Esarul Shekh | B.tech CSE (CYS) |

### `attendance.csv`

| Student Code | Date | Status |
|---|---|---|
| BWU/BCC/25/063 | 2026-11-02 | P |

- **Date** format: `YYYY-MM-DD`
- **Status**: `P` = Present, `A` = Absent
- Each student has **one row per class date**.

### ✏️ Correcting a mistake

The menu has no edit/delete option, so fix things directly in the CSV:

| Problem | Fix |
|---------|-----|
| Wrong P/A for a student | Open `attendance.csv`, change that row's `Status` to `P` or `A`, save |
| Misspelled name | Open `students.csv`, edit the `Name`, save |
| Student left the class | Delete that student's row in `students.csv` |
| Whole date marked wrongly | Delete all rows with that date in `attendance.csv`, then mark it again from the menu |

> ⚠️ **Close the CSV in Excel before running the program**, and keep the header row (first line) unchanged.

---

## 💾 Safety Features

- **Safe saving** — files are written to a temporary file first, then swapped in, so data is not corrupted if something goes wrong.
- **Automatic backup** — if the program has to upgrade an older CSV format, it first saves a `.bak` copy (`students.csv.bak` / `attendance.csv.bak`).
- **Invalid rows are skipped** — rows with a bad date or a status other than `P`/`A` are ignored instead of crashing the program.
- **Safe exit** — press `Ctrl + C` any time to stop the program cleanly.
- 🔒 Student data stays **on your computer** — nothing is sent online.

> 🔐 If you upload this project to a **public** GitHub repo, remove or replace the real student names in the CSV files first (or keep the repo private).

---

## ❓ FAQ / Troubleshooting

**`python` is not recognized**
Install Python from [python.org](https://www.python.org/downloads/) and tick **"Add Python to PATH"**, or try `python3`.

**"Invalid format" when adding a student**
Use exactly `XXX/XX/XXX` (letters/digits), e.g. `BCC/25/063`.

**"Attendance for this date has already been marked"**
Attendance is allowed once per date. Edit `attendance.csv` to fix it, or delete that date's rows and mark it again.

**"Future dates are not allowed"**
Enter today's date or an earlier one.

**A new student shows 0.00%**
Normal — no classes are recorded for them yet. It updates after the next attendance session.

**Attendance doesn't save / permission error**
Close the CSV files in Excel/other apps and make sure the folder is writable.

---

## 📁 Project Structure

```
Python-Attendance-Project/
├── student_attendance_management.py   # main program
├── students.csv                       # student list
├── attendance.csv                     # attendance records
└── README.md
```

## 🛠️ Tech Details

- **Language:** Python 3
- **Libraries:** `csv`, `re`, `shutil`, `datetime`, `pathlib` (all built-in)
- **Storage:** CSV files saved next to the script
- **Interface:** Command-line, menu-driven

## 👨‍💻 Author

**Esarul Shekh** — B.Tech CSE (Cyber Security), Brainware University, Barasat
Roll No: BWU/BCC/25/063

---

⭐ *Made for the classroom — simple for teachers, easy for students to understand.*
