"""
gradebook.py
Mini Project: GradeBook Analyzer
Course: Programming for Problem Solving using Python

Submitted by : MANDAKANI  
Submitted to : Ms. Jyoti Ma'am
Date         : 2025-11-05             
Description  : Collects student names and marks, computes statistics
               (average, median, min, max), assigns letter grades,
               separates pass/fail lists, prints a results table and
               allows re-running analysis via a menu loop.
"""

from typing import Dict, List, Tuple
import statistics

def input_positive_int(prompt: str) -> int:
    """Robust integer input for positive integers."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 1:
                print("Please enter an integer greater than 0.")
                continue
            return value
        except ValueError:
            print("That's not a valid integer. Try again.")

def input_students(minimum: int = 5) -> Dict[str, int]:
    """
    Ask user how many students, then collect name and marks.
    Enforce at least `minimum` students as per assignment tests.
    Returns a dictionary: {name: marks}
    """
    while True:
        n = input_positive_int(f"How many students are in the class? (minimum {minimum}): ")
        if n < minimum:
            print(f"Assignment requires testing with at least {minimum} students. Please enter {minimum} or more.")
            continue
        break

    marks: Dict[str, int] = {}
    for i in range(1, n + 1):
        # Collect student name
        while True:
            name = input(f"Enter name of student #{i}: ").strip()
            if name == "":
                print("Name cannot be empty. Try again.")
                continue
            if name in marks:
                print("This name was already entered. Add a unique identifier or use last name too.")
                continue
            break

        # Collect marks as integer between 0 and 100
        while True:
            try:
                m = float(input(f"Enter marks for {name} (0 - 100): ").strip())
                if m < 0 or m > 100:
                    print("Marks must be between 0 and 100.")
                    continue
                marks[name] = int(round(m))  # store as integer (rounded)
                break
            except ValueError:
                print("Invalid number. Enter numeric marks (e.g. 78 or 78.5).")

    print("\nData entry complete.\n")
    return marks

def calculate_average(marks_dict: Dict[str, int]) -> float:
    """Return mean (average) of marks as float rounded to 2 decimals."""
    if not marks_dict:
        return 0.0
    avg = statistics.mean(marks_dict.values())
    return round(avg, 2)

def calculate_median(marks_dict: Dict[str, int]) -> float:
    """Return median of marks as float."""
    if not marks_dict:
        return 0.0
    med = statistics.median(marks_dict.values())
    return float(med)

def find_max_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Return tuple (name, score) of student with maximum marks.
       If multiple share max, return the first encountered."""
    if not marks_dict:
        return ("", 0)
    # keep insertion order (Python 3.7+ dicts preserve insertion order)
    max_name = max(marks_dict, key=lambda k: marks_dict[k])
    return (max_name, marks_dict[max_name])

def find_min_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Return tuple (name, score) of student with minimum marks."""
    if not marks_dict:
        return ("", 0)
    min_name = min(marks_dict, key=lambda k: marks_dict[k])
    return (min_name, marks_dict[min_name])

def assign_grade(score: int) -> str:
    """Assign letter grade based on numeric score."""
    if score >= 90:
        return "A"
    elif 80 <= score <= 89:
        return "B"
    elif 70 <= score <= 79:
        return "C"
    elif 60 <= score <= 69:
        return "D"
    else:
        return "F"

def build_grades_dict(marks_dict: Dict[str, int]) -> Dict[str, str]:
    """Return dictionary of grades for each student."""
    return {name: assign_grade(score) for name, score in marks_dict.items()}

def grade_distribution(grades_dict: Dict[str, str]) -> Dict[str, int]:
    """Return counts of each grade category found in grades_dict."""
    categories = ["A", "B", "C", "D", "F"]
    dist = {cat: 0 for cat in categories}
    for g in grades_dict.values():
        if g in dist:
            dist[g] += 1
        else:
            dist[g] = 1  # safety, shouldn't be necessary
    return dist

def pass_fail_lists(marks_dict: Dict[str, int]) -> Tuple[List[str], List[str]]:
    """Use list comprehensions to separate passed and failed students.
       Pass criteria: marks >= 40 (as specified in assignment example)."""
    passed = [name for name, m in marks_dict.items() if m >= 40]
    failed = [name for name, m in marks_dict.items() if m < 40]
    return (passed, failed)

def print_statistics(marks_dict: Dict[str, int]) -> None:
    """Compute & print average, median, max and min in a neat format."""
    avg = calculate_average(marks_dict)
    med = calculate_median(marks_dict)
    max_name, max_score = find_max_score(marks_dict)
    min_name, min_score = find_min_score(marks_dict)

    print("STATISTICAL SUMMARY")
    print("-------------------")
    print(f"Average (mean) marks : {avg}")
    print(f"Median marks         : {med}")
    print(f"Highest marks        : {max_score}  (Student: {max_name})")
    print(f"Lowest marks         : {min_score}  (Student: {min_name})")
    print()

def print_results_table(marks_dict: Dict[str, int], grades_dict: Dict[str, str]) -> None:
    """Print formatted table:
       Name       Marks     Grade
       --------------------------
       Alice        78         C
    """
    # Determine column widths (nice formatting even for long names)
    name_col = max(4, max((len(name) for name in marks_dict), default=4))
    marks_col = 5
    grade_col = 5

    header = f"{'Name':<{name_col}}  {'Marks':>{marks_col}}  {'Grade':^{grade_col}}"
    sep = "-" * (name_col + marks_col + grade_col + 4)
    print(header)
    print(sep)
    for name, marks in marks_dict.items():
        grade = grades_dict.get(name, "")
        print(f"{name:<{name_col}}  {marks:>{marks_col}}      {grade:^{grade_col}}")
    print()

def run_analysis_once() -> None:
    """Runs one full cycle: input -> stats -> grades -> table -> pass/fail -> distribution."""
    # Task 2: Manual Input
    marks = input_students(minimum=5)

    # Task 3: Statistical Analysis Functions
    print_statistics(marks)

    # Task 4: Grade Assignment and Distribution
    grades = build_grades_dict(marks)
    dist = grade_distribution(grades)
    print("GRADE SUMMARY")
    print("-------------")
    for cat in ["A", "B", "C", "D", "F"]:
        print(f"{cat}: {dist.get(cat, 0)}")
    print()

    # Task 5: Pass/Fail using list comprehension
    passed, failed = pass_fail_lists(marks)
    print("PASS / FAIL")
    print("-----------")
    print(f"Passed students ({len(passed)}): {passed}")
    print(f"Failed students ({len(failed)}): {failed}")
    print()

    # Task 6: Results Table
    print("RESULTS TABLE")
    print("-------------")
    print_results_table(marks, grades)

    # Extra - small summary
    print("Analysis complete. You may choose to run again or exit from the menu.\n")


def main_menu() -> None:
    """Menu-driven interface that allows reruns or exit."""
    welcome = """
Welcome to GradeBook Analyzer
----------------------------
A simple Python tool to analyze and report student grades.
Please follow the on-screen prompts to enter data and view results.
    """
    print(welcome)
    while True:
        print("Menu:")
        print("1. Enter student data and run analysis")
        print("2. Example run (pre-filled sample) - FOR QUICK DEMO")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == "1":
            run_analysis_once()
        elif choice == "2":
            # Pre-filled demonstration data for quick checking / instructor demo
            demo_marks = {
                "Alice": 78,
                "Bob": 92,
                "Carol": 56,
                "David": 34,
                "Eve": 88
            }
            print("\nRunning example/demo with 5 sample students (Alice, Bob, Carol, David, Eve)\n")
            print_statistics(demo_marks)
            demo_grades = build_grades_dict(demo_marks)
            print("GRADE SUMMARY")
            for cat, cnt in grade_distribution(demo_grades).items():
                print(f"{cat}: {cnt}")
            passed, failed = pass_fail_lists(demo_marks)
            print(f"\nPassed ({len(passed)}): {passed}")
            print(f"Failed ({len(failed)}): {failed}\n")
            print_results_table(demo_marks, demo_grades)
        elif choice == "3":
            print("Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")
        # After each run, ask whether to continue or not (keeps loop friendly)
        cont = input("Return to menu? (y/n): ").strip().lower()
        if cont not in ("", "y", "yes"):
            print("Exiting GradeBook Analyzer. Goodbye!")
            break

if __name__ == "__main__":
    main_menu()