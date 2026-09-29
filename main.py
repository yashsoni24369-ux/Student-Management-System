import json


# =========================================================
# STUDENT CLASS
# =========================================================

class Student:

    def __init__(self, student_id, name, age, marks):

        self.id = student_id
        self.name = name
        self.age = age
        self.marks = marks

        self.calculate_results()

    # -----------------------------------------------------
    # Calculate Results
    # -----------------------------------------------------

    def calculate_results(self):

        self.total_marks = sum(self.marks)

        self.average = self.total_marks / len(self.marks)

        self.grade = self.calculate_grade()

        self.status = self.calculate_status()

    # -----------------------------------------------------
    # Calculate Grade
    # -----------------------------------------------------

    def calculate_grade(self):

        if self.average >= 90:
            return "A+"

        elif self.average >= 80:
            return "A"

        elif self.average >= 70:
            return "B"

        elif self.average >= 60:
            return "C"

        elif self.average >= 50:
            return "D"

        else:
            return "F"

    # -----------------------------------------------------
    # Calculate Status
    # -----------------------------------------------------

    def calculate_status(self):

        if self.average >= 40:
            return "PASS"

        else:
            return "FAIL"

    # -----------------------------------------------------
    # Update Student
    # -----------------------------------------------------

    def update(self, name, age, marks):

        self.name = name
        self.age = age
        self.marks = marks

        self.calculate_results()

    # -----------------------------------------------------
    # Convert Student to Dictionary
    # -----------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "marks": self.marks,
            "total_marks": self.total_marks,
            "average": self.average,
            "grade": self.grade,
            "status": self.status
        }

    # -----------------------------------------------------
    # Create Student from Dictionary
    # -----------------------------------------------------

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["id"],
            data["name"],
            data["age"],
            data["marks"]
        )


# =========================================================
# STUDENT MANAGER CLASS
# =========================================================

class StudentManager:

    def __init__(self):

        self.students = []

    # -----------------------------------------------------
    # Get Next Student ID
    # -----------------------------------------------------

    def get_next_student_id(self):

        if not self.students:
            return 1

        return max(
            student.id
            for student in self.students
        ) + 1

    # -----------------------------------------------------
    # Add Student
    # -----------------------------------------------------

    def add_student(self, name, age, marks):

        student_id = self.get_next_student_id()

        student = Student(
            student_id,
            name,
            age,
            marks
        )

        self.students.append(student)

        self.save_students()

        return student

    # -----------------------------------------------------
    # Display One Student
    # -----------------------------------------------------

    def display_student(self, student):

        print("\nStudent ID:", student.id)

        print("Name:", student.name)

        print("Age:", student.age)

        print("Marks:")

        for i, mark in enumerate(
            student.marks,
            start=1
        ):

            print(
                f"  Subject {i}: {mark}"
            )

        print(
            "Total Marks:",
            student.total_marks
        )

        print(
            "Average:",
            round(student.average, 2)
        )

        print(
            "Grade:",
            student.grade
        )

        print(
            "Status:",
            student.status
        )

    # -----------------------------------------------------
    # Display All Students
    # -----------------------------------------------------

    def display_students(self):

        if not self.students:

            print("\nNo students found.")

            return

        print(
            "\n========== Student List =========="
        )

        for student in self.students:

            self.display_student(student)

    # -----------------------------------------------------
    # Search Student by ID
    # -----------------------------------------------------

    def search_student(self, student_id):

        for student in self.students:

            if student.id == student_id:

                return student

        return None

    # -----------------------------------------------------
    # Search Student by Name
    # -----------------------------------------------------

    def search_students_by_name(self, name):

        results = []

        for student in self.students:

            if name.lower() in student.name.lower():

                results.append(student)

        return results

    # -----------------------------------------------------
    # Delete Student
    # -----------------------------------------------------

    def delete_student(self, student_id):

        student = self.search_student(student_id)

        if student is None:

            return False

        self.students.remove(student)

        self.save_students()

        return True

    # -----------------------------------------------------
    # Update Student
    # -----------------------------------------------------

    def update_student(
        self,
        student_id,
        name,
        age,
        marks
    ):

        student = self.search_student(student_id)

        if student is None:

            return False

        student.update(
            name,
            age,
            marks
        )

        self.save_students()

        return True

    # -----------------------------------------------------
    # Count Students
    # -----------------------------------------------------

    def count_students(self):

        return len(self.students)

    # -----------------------------------------------------
    # Find Top Student
    # -----------------------------------------------------

    def find_top_student(self):

        if not self.students:

            return None

        return max(
            self.students,
            key=lambda student: student.average
        )

    # -----------------------------------------------------
    # Find Lowest Student
    # -----------------------------------------------------

    def find_lowest_student(self):

        if not self.students:

            return None

        return min(
            self.students,
            key=lambda student: student.average
        )

    # -----------------------------------------------------
    # Sort Students
    # -----------------------------------------------------

    def sort_students(self):

        return sorted(
            self.students,
            key=lambda student: student.average,
            reverse=True
        )

    # -----------------------------------------------------
    # Save Students
    # -----------------------------------------------------

    def save_students(self):

        try:

            data = [
                student.to_dict()
                for student in self.students
            ]

            with open(
                "students.json",
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except OSError:

            print(
                "Error: Could not save student data."
            )

    # -----------------------------------------------------
    # Load Students
    # -----------------------------------------------------

    def load_students(self):

        try:

            with open(
                "students.json",
                "r"
            ) as file:

                data = json.load(file)

                self.students = [
                    Student.from_dict(student)
                    for student in data
                ]

            print(
                "Student data loaded successfully."
            )

        except FileNotFoundError:

            self.students = []

        except json.JSONDecodeError:

            print(
                "Error: Student file contains "
                "invalid data."
            )

            self.students = []


# =========================================================
# INPUT VALIDATION FUNCTIONS
# =========================================================

def get_valid_name():

    while True:

        name = input(
            "Enter student name: "
        ).strip()

        if name:

            return name

        print(
            "Name cannot be empty."
        )


def get_valid_age():

    while True:

        try:

            age = int(
                input("Enter age: ")
            )

            if age <= 0:

                print(
                    "Age must be greater than 0."
                )

                continue

            return age

        except ValueError:

            print(
                "Please enter a valid number."
            )


def get_valid_mark(subject_number):

    while True:

        try:

            mark = float(
                input(
                    f"Enter marks for subject "
                    f"{subject_number}: "
                )
            )

            if mark < 0 or mark > 100:

                print(
                    "Marks must be between 0 and 100."
                )

                continue

            return mark

        except ValueError:

            print(
                "Please enter a valid number."
            )


def get_marks():

    marks = []

    for i in range(1, 6):

        mark = get_valid_mark(i)

        marks.append(mark)

    return marks


def get_valid_student_id(message):

    while True:

        try:

            return int(
                input(message)
            )

        except ValueError:

            print(
                "Please enter a valid ID."
            )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    manager = StudentManager()

    manager.load_students()

    while True:

        print(
            "\n================================"
        )

        print(
            "     STUDENT MANAGEMENT SYSTEM"
        )

        print(
            "================================"
        )

        print("1. Add Student")
        print("2. Display Students")
        print("3. Exit")
        print("4. Delete Student")
        print("5. Search Student by ID")
        print("6. Update Student")
        print("7. Count Students")
        print("8. Search Student by Name")
        print("9. Find Top Student")
        print("10. Find Lowest Student")
        print("11. Sort Students by Average")

        try:

            choice = int(
                input(
                    "\nEnter your choice: "
                )
            )

        except ValueError:

            print(
                "Please enter a number."
            )

            continue

        # -------------------------------------------------
        # Add Student
        # -------------------------------------------------

        if choice == 1:

            name = get_valid_name()

            age = get_valid_age()

            marks = get_marks()

            student = manager.add_student(
                name,
                age,
                marks
            )

            print(
                "\nStudent added successfully!"
            )

            print(
                "Student ID:",
                student.id
            )

        # -------------------------------------------------
        # Display Students
        # -------------------------------------------------

        elif choice == 2:

            manager.display_students()

        # -------------------------------------------------
        # Exit
        # -------------------------------------------------

        elif choice == 3:

            manager.save_students()

            print(
                "\nThank you for using "
                "Student Management System."
            )

            break

        # -------------------------------------------------
        # Delete Student
        # -------------------------------------------------

        elif choice == 4:

            if not manager.students:

                print(
                    "\nNo students found."
                )

                continue

            delete_id = get_valid_student_id(
                "Enter student ID to delete: "
            )

            deleted = manager.delete_student(
                delete_id
            )

            if deleted:

                print(
                    "Student deleted successfully."
                )

            else:

                print(
                    "Student not found."
                )

        # -------------------------------------------------
        # Search Student by ID
        # -------------------------------------------------

        elif choice == 5:

            if not manager.students:

                print(
                    "\nNo students found."
                )

                continue

            search_id = get_valid_student_id(
                "Enter student ID to search: "
            )

            student = manager.search_student(
                search_id
            )

            if student:

                print(
                    "\nStudent found!"
                )

                manager.display_student(
                    student
                )

            else:

                print(
                    "Student not found."
                )

        # -------------------------------------------------
        # Update Student
        # -------------------------------------------------

        elif choice == 6:

            if not manager.students:

                print(
                    "\nNo students found."
                )

                continue

            update_id = get_valid_student_id(
                "Enter student ID to update: "
            )

            student = manager.search_student(
                update_id
            )

            if student is None:

                print(
                    "Student not found."
                )

                continue

            print(
                "\nCurrent name:",
                student.name
            )

            print(
                "Current age:",
                student.age
            )

            print(
                "\nUpdate Name"
            )

            new_name = get_valid_name()

            print(
                "\nUpdate Age"
            )

            new_age = get_valid_age()

            print(
                "\nEnter new marks:"
            )

            new_marks = get_marks()

            updated = manager.update_student(
                update_id,
                new_name,
                new_age,
                new_marks
            )

            if updated:

                print(
                    "\nStudent updated successfully."
                )

        # -------------------------------------------------
        # Count Students
        # -------------------------------------------------

        elif choice == 7:

            print(
                "\nTotal Students:",
                manager.count_students()
            )

        # -------------------------------------------------
        # Search Student by Name
        # -------------------------------------------------

        elif choice == 8:

            if not manager.students:

                print(
                    "\nNo students found."
                )

                continue

            search_name = input(
                "Enter student name to search: "
            ).strip()

            if not search_name:

                print(
                    "Name cannot be empty."
                )

                continue

            results = (
                manager.search_students_by_name(
                    search_name
                )
            )

            if not results:

                print(
                    "Student not found."
                )

            else:

                for student in results:

                    print(
                        "\nStudent found!"
                    )

                    manager.display_student(
                        student
                    )

        # -------------------------------------------------
        # Find Top Student
        # -------------------------------------------------

        elif choice == 9:

            top_student = (
                manager.find_top_student()
            )

            if top_student is None:

                print(
                    "\nNo students found."
                )

            else:

                print(
                    "\n========== Top Student =========="
                )

                manager.display_student(
                    top_student
                )

        # -------------------------------------------------
        # Find Lowest Student
        # -------------------------------------------------

        elif choice == 10:

            lowest_student = (
                manager.find_lowest_student()
            )

            if lowest_student is None:

                print(
                    "\nNo students found."
                )

            else:

                print(
                    "\n========== Lowest Student =========="
                )

                manager.display_student(
                    lowest_student
                )

        # -------------------------------------------------
        # Sort Students
        # -------------------------------------------------

        elif choice == 11:

            if not manager.students:

                print(
                    "\nNo students found."
                )

                continue

            sorted_students = (
                manager.sort_students()
            )

            print(
                "\n========== "
                "Students Sorted by Average "
                "=========="
            )

            for student in sorted_students:

                manager.display_student(
                    student
                )

        # -------------------------------------------------
        # Invalid Choice
        # -------------------------------------------------

        else:

            print(
                "Invalid choice. "
                "Please select 1 to 11."
            )


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()