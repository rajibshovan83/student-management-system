import json
import os

# ----------- Classes -----------

class Person:
    def __init__(self, name:str, age:int, address:str):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")


class Student(Person):
    def __init__(self, name, age, address, student_id:str):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}      # e.g., {"Math": "A"}
        self.courses = []     # list of enrolled course codes

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)

    def display_student_info(self, course_lookup=None):
        print("Student Information:")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        if course_lookup:
            names = [course_lookup[c].course_name for c in self.courses if c in course_lookup]
        else:
            names = self.courses
        print(f"Enrolled Courses: {', '.join(names) if names else 'None'}")
        print(f"Grades: {self.grades}")


class Course:
    def __init__(self, course_name:str, course_code: str, instructor: str):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []  # list of Student objects

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def display_course_info(self):
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        names = [s.name for s in self.students]
        print(f"Enrolled Students: {', '.join(names) if names else 'None'}")


# ----------- Management System -----------

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.default_file = "sms_data.json"

    def add_new_student(self, name, age, address, student_id):
        if student_id in self.students:
            return f"Error: Student ID {student_id} already exists."
        try:
            age = int(age)
        except ValueError:
            return "Error: Age must be a number."
        student = Student(name, age, address, student_id)
        self.students[student_id] = student
        return f"Student {name} (ID: {student_id}) added successfully."

    def add_new_course(self, course_name, course_code, instructor):
        course_code = course_code.upper()
        if course_code in self.courses:
            return f"Error: Course Code {course_code} already exists."
        course = Course(course_name, course_code, instructor)
        self.courses[course_code] = course
        return f"Course {course_name} (Code: {course_code}) created with instructor {instructor}."

    def enroll_student_in_course(self, student_id, course_code):
        course_code = course_code.upper()
        if student_id not in self.students:
            return f"Error: Student ID {student_id} not found."
        if course_code not in self.courses:
            return f"Error: Course Code {course_code} not found."
        student = self.students[student_id]
        course = self.courses[course_code]
        if course_code in student.courses:
            return f"Error: {student.name} already enrolled in {course.course_name}."
        student.enroll_course(course_code)
        course.add_student(student)
        return f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code})."

    def add_grade_for_student(self, student_id, course_code, grade):
        course_code = course_code.upper()
        if student_id not in self.students:
            return f"Error: Student ID {student_id} not found."
        if course_code not in self.courses:
            return f"Error: Course Code {course_code} not found."
        student = self.students[student_id]
        course = self.courses[course_code]
        if course_code not in student.courses:
            return f"Error: {student.name} is not enrolled in {course.course_name}."
        student.add_grade(course.course_name, grade)
        return f"Grade {grade} added for {student.name} in {course.course_name}."

    def display_student_details(self, student_id):
        if student_id not in self.students:
            return f"Error: Student ID {student_id} not found."
        self.students[student_id].display_student_info(self.courses)

    def display_course_details(self, course_code):
        course_code = course_code.upper()
        if course_code not in self.courses:
            return f"Error: Course Code {course_code} not found."
        self.courses[course_code].display_course_info()

    def save_data(self):
        data = {
            "students": {
                sid: {
                    "name": s.name,
                    "age": s.age,
                    "address": s.address,
                    "student_id": s.student_id,
                    "grades": s.grades,
                    "courses": s.courses
                } for sid, s in self.students.items()
            },
            "courses": {
                code: {
                    "course_name": c.course_name,
                    "course_code": c.course_code,
                    "instructor": c.instructor,
                    "students": [s.student_id for s in c.students]
                } for code, c in self.courses.items()
            }
        }
        with open(self.default_file, "w") as f:
            json.dump(data, f, indent=2)
        return "All student and course data saved successfully."

    def load_data(self):
        if not os.path.exists(self.default_file):
            return "Error: No saved data found."
        with open(self.default_file, "r") as f:
            data = json.load(f)
        self.students.clear()
        self.courses.clear()
        for sid, s in data["students"].items():
            student = Student(s["name"], s["age"], s["address"], s["student_id"])
            student.grades = s["grades"]
            student.courses = s["courses"]
            self.students[sid] = student
        for code, c in data["courses"].items():
            course = Course(c["course_name"], c["course_code"], c["instructor"])
            self.courses[code] = course
        for code, c in data["courses"].items():
            for sid in c["students"]:
                if sid in self.students:
                    self.courses[code].add_student(self.students[sid])
        return "Data loaded successfully."

    def run_cli(self):
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Save Data to File")
            print("8. Load Data from File")
            print("0. Exit")
            choice = input("Select Option: ").strip()
            if choice == "1":
                name = input("Enter Name: ")
                age = input("Enter Age: ")
                address = input("Enter Address: ")
                sid = input("Enter Student ID: ")
                print(self.add_new_student(name, age, address, sid))
            elif choice == "2":
                cname = input("Enter Course Name: ")
                ccode = input("Enter Course Code: ")
                instr = input("Enter Instructor: ")
                print(self.add_new_course(cname, ccode, instr))
            elif choice == "3":
                sid = input("Enter Student ID: ")
                ccode = input("Enter Course Code: ")
                print(self.enroll_student_in_course(sid, ccode))
            elif choice == "4":
                sid = input("Enter Student ID: ")
                ccode = input("Enter Course Code: ")
                grade = input("Enter Grade: ")
                print(self.add_grade_for_student(sid, ccode, grade))
            elif choice == "5":
                sid = input("Enter Student ID: ")
                sid = sid.upper()
                if sid in self.students:
                    self.students[sid].display_student_info(self.courses)
                else:
                    print(f"Error: Student ID {sid} not found.")
            elif choice == "6":
                ccode = input("Enter Course Code: ")
                ccode = ccode.upper()
                if ccode in self.courses:
                    self.courses[ccode].display_course_info()
                else:   
                    print(f"Error: Course Code {ccode} not found.")
            elif choice == "7":
                print(self.save_data())
            elif choice == "8":
                print(self.load_data())
            elif choice == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Try again.")


if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.run_cli()
