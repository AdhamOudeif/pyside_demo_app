import json
import os

DATA_FILE = "students.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_student(name, address):
    students = load_students()
    students.append({"name": name, "address": address})
    with open(DATA_FILE, 'w') as file:
        json.dump(students, file, indent=4)

def get_students():
    return load_students()

def delete_student(name, address):
    students = load_students()
    updated_students = [student for student in students if not (student['name'] == name and student['address'] == address)]
    with open(DATA_FILE, 'w') as file:
        json.dump(updated_students, file, indent=4)
