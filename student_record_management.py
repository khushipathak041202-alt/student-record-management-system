"""Beginner-friendly Student Record Management System.
Run: python student_record_management.py
"""
import json
from pathlib import Path

DATA_FILE = Path("students.json")


def load_students():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("Data file could not be read; starting with an empty list.")
    return []


def save_students(students):
    DATA_FILE.write_text(json.dumps(students, indent=2), encoding="utf-8")


def add_student(students):
    student_id = input("Student ID: ").strip()
    if any(s["id"] == student_id for s in students):
        print("That ID already exists.")
        return
    name = input("Student name: ").strip()
    course = input("Course: ").strip()
    try:
        marks = float(input("Marks (0-100): "))
        if not 0 <= marks <= 100:
            raise ValueError
    except ValueError:
        print("Please enter marks between 0 and 100.")
        return
    students.append({"id": student_id, "name": name, "course": course, "marks": marks})
    save_students(students)
    print("Student added.")


def view_students(students):
    if not students:
        print("No student records yet.")
        return
    print("\\nID | Name | Course | Marks")
    print("-" * 45)
    for s in students:
        print(f'{s["id"]} | {s["name"]} | {s["course"]} | {s["marks"]}')


def search_student(students):
    student_id = input("Enter student ID to search: ").strip()
    found = next((s for s in students if s["id"] == student_id), None)
    print(found if found else "Student not found.")


def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()
    remaining = [s for s in students if s["id"] != student_id]
    if len(remaining) == len(students):
        print("Student not found.")
        return
    students[:] = remaining
    save_students(students)
    print("Student deleted.")


def main():
    students = load_students()
    actions = {
        "1": lambda: add_student(students),
        "2": lambda: view_students(students),
        "3": lambda: search_student(students),
        "4": lambda: delete_student(students),
    }
    while True:
        print("\\nSTUDENT RECORD MANAGEMENT")
        print("1. Add student  2. View students  3. Search by ID  4. Delete student  5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "5":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Choose an option from 1 to 5.")


if __name__ == "__main__":
    main()
