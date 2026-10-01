import json
import os
import tempfile
import unittest
from pathlib import Path

from main import Student, StudentManager


class TestStudent(unittest.TestCase):
    def test_total_average_grade_and_status(self):
        student = Student(1, "Test Student", 18, [80, 90, 70, 85, 75])
        self.assertEqual(student.total_marks, 400)
        self.assertEqual(student.average, 80)
        self.assertEqual(student.grade, "A")
        self.assertEqual(student.status, "PASS")

    def test_grade_boundaries(self):
        cases = [
            (95, "A+"), (85, "A"), (75, "B"),
            (65, "C"), (55, "D"), (35, "F")
        ]
        for mark, expected in cases:
            with self.subTest(average=mark):
                student = Student(1, "Test", 18, [mark] * 5)
                self.assertEqual(student.grade, expected)

    def test_pass_fail_boundary(self):
        passed = Student(1, "Pass", 18, [40] * 5)
        failed = Student(2, "Fail", 18, [39] * 5)
        self.assertEqual(passed.status, "PASS")
        self.assertEqual(failed.status, "FAIL")

    def test_update_recalculates_results(self):
        student = Student(1, "Old", 18, [50] * 5)
        student.update("New", 19, [90] * 5)
        self.assertEqual(student.name, "New")
        self.assertEqual(student.age, 19)
        self.assertEqual(student.total_marks, 450)
        self.assertEqual(student.average, 90)
        self.assertEqual(student.grade, "A+")

    def test_dictionary_conversion(self):
        student = Student(7, "Asha", 20, [60, 70, 80, 90, 100])
        restored = Student.from_dict(student.to_dict())
        self.assertEqual(restored.id, student.id)
        self.assertEqual(restored.name, student.name)
        self.assertEqual(restored.marks, student.marks)
        self.assertEqual(restored.average, student.average)


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        self.manager = StudentManager()

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

    def add_sample_students(self):
        first = self.manager.add_student("Asha", 18, [90, 90, 90, 90, 90])
        second = self.manager.add_student("Ravi", 19, [60, 60, 60, 60, 60])
        third = self.manager.add_student("Mina", 18, [75, 75, 75, 75, 75])
        return first, second, third

    def test_add_assigns_incrementing_ids_and_counts(self):
        first, second, _ = self.add_sample_students()
        self.assertEqual((first.id, second.id), (1, 2))
        self.assertEqual(self.manager.count_students(), 3)

    def test_search_by_id(self):
        first, _, _ = self.add_sample_students()
        self.assertIs(self.manager.search_student(first.id), first)
        self.assertIsNone(self.manager.search_student(999))

    def test_search_by_partial_case_insensitive_name(self):
        self.add_sample_students()
        found = self.manager.search_students_by_name("AS")
        self.assertEqual([student.name for student in found], ["Asha"])

    def test_update_student(self):
        self.add_sample_students()
        result = self.manager.update_student(2, "Ravi Kumar", 20, [85] * 5)
        self.assertTrue(result)
        updated = self.manager.search_student(2)
        self.assertEqual(updated.name, "Ravi Kumar")
        self.assertEqual(updated.average, 85)
        self.assertFalse(self.manager.update_student(999, "Missing", 18, [50] * 5))

    def test_delete_student(self):
        self.add_sample_students()
        self.assertTrue(self.manager.delete_student(2))
        self.assertIsNone(self.manager.search_student(2))
        self.assertEqual(self.manager.count_students(), 2)
        self.assertFalse(self.manager.delete_student(999))

    def test_top_lowest_and_sort(self):
        self.add_sample_students()
        self.assertEqual(self.manager.find_top_student().name, "Asha")
        self.assertEqual(self.manager.find_lowest_student().name, "Ravi")
        self.assertEqual(
            [student.name for student in self.manager.sort_students()],
            ["Asha", "Mina", "Ravi"]
        )

    def test_top_lowest_on_empty_manager(self):
        self.assertIsNone(self.manager.find_top_student())
        self.assertIsNone(self.manager.find_lowest_student())
        self.assertEqual(self.manager.sort_students(), [])

    def test_json_save_and_load(self):
        self.add_sample_students()
        self.manager.save_students()
        saved_path = Path("students.json")
        self.assertTrue(saved_path.exists())
        raw_data = json.loads(saved_path.read_text(encoding="utf-8"))
        self.assertEqual(len(raw_data), 3)

        loaded_manager = StudentManager()
        loaded_manager.load_students()
        self.assertEqual(loaded_manager.count_students(), 3)
        self.assertEqual(loaded_manager.search_student(1).name, "Asha")
        self.assertEqual(loaded_manager.search_student(1).average, 90)


if __name__ == "__main__":
    unittest.main()
