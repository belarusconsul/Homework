# Task 4.3
# File 'data/students.csv' stores information about students in CSV format.
# This file contains the student’s names, age and average mark.
# 1.Implement a function which receives file path and returns names of
# top performer students
# 2. Implement a function which receives the file path with students info
# and writes CSV student information to the new file in descending order of age.

import csv


def get_top_performers(file_path, number_of_top_students=5):
    """
    Return names of top performer students from a csv file

    Parameters
    ----------
    file_path : TYPE string
        DESCRIPTION. Path to a file
    number_of_top_students : TYPE integer, optional
        DESCRIPTION. Number of student names to return. The default is 5.

    Returns
    -------
    TYPE list
        DESCRIPTION. Top performer students from a csv file.

    """
    with open("data/students.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        headers = csv_reader.fieldnames
        list_of_students = sorted(
            csv_reader, key=lambda row: float(row[headers[2]]), reverse=True
        )[:number_of_top_students]
        return [student[headers[0]] for student in list_of_students]


def sort_students_by_age(file_path):
    """
    Read a csv file with student information and write a new csv file
    with student info sorted in descending order of age. The new file
    is located in the same folder as the old file.

    Parameters
    ----------
    file_path : TYPE string
        DESCRIPTION. Path to a file

    Returns
    -------
    None.

    """
    with open(file_path, "r") as file_unsorted:
        csv_reader = csv.DictReader(file_unsorted)
        headers = csv_reader.fieldnames
        list_of_students = sorted(
            csv_reader, key=lambda row: int(row[headers[1]]), reverse=True
        )
        new_path = file_path[: file_path.rfind("/") + 1] + "sorted_students.csv"
        with open(new_path, "w", newline="") as file_sorted:
            csv_writer = csv.DictWriter(file_sorted, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(list_of_students)


print(get_top_performers("students.csv"))
sort_students_by_age("data/students.csv")
