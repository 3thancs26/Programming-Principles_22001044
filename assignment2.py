import json

# File path declaration
file_path = "assignment_studentID.txt"

# Global data structures to store course and submission information
courses = {}
submissions = {}

def submit_assignment(course_name, student_id, assignment_title):
    """Submit an assignment."""
    # Ensure the course exists
    if course_name not in courses:
        courses[course_name] = []
    # Create the assignment
    assignment = {'course_name': course_name, 'student_id': student_id, 'title': assignment_title, 'status': 'Pending'}
    # Add the assignment to the course
    courses[course_name].append(assignment)
    print(f"Assignment '{assignment_title}' submitted successfully by {student_id} for course {course_name}")
    save_courses_to_file(file_path)

def check_assignment_status(course_name, student_id):
    """Check assignment status for a student."""
    if course_name in courses:
        assignments = [assignment for assignment in courses[course_name] if assignment['student_id'] == student_id]
        if assignments:
            for assignment in assignments:
                print(f"Assignment '{assignment['title']}' status: {assignment['status']}")
        else:
            print(f"No assignment submitted by {student_id} for course {course_name}")
    else:
        print(f"Course {course_name} does not exist.")

def update_assignment_status(course_name, assignment_title, status):
    """Update assignment status."""
    if course_name in courses:
        for assignment in courses[course_name]:
            if assignment['title'] == assignment_title:
                assignment['status'] = status
                print(f"Assignment '{assignment_title}' status updated to '{status}'")
                save_courses_to_file(file_path)
                return
    print(f"No assignment found with title '{assignment_title}' in course {course_name}")

def load_courses_from_file(file_path):
    """Load courses from file."""
    global courses
    try:
        with open(file_path, 'r') as file:
            courses = json.load(file)  # Load courses from the file
    except FileNotFoundError:
        print("File not found. No courses loaded.")
    except Exception as e:
        print(f"An error occurred while loading courses: {e}")

def save_courses_to_file(file_path):
    """Save courses to file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(courses, file)  # Write courses to the file
    except Exception as e:
        print(f"An error occurred while saving courses: {e}")

def load_submissions_from_file(file_path):
    """Load submissions from file."""
    global submissions
    try:
        with open(file_path, 'r') as file:
            for line in file:
                student_id, status = line.strip().split(',')
                submissions[student_id] = status
    except FileNotFoundError:
        print("File not found. No submissions loaded.")
    except Exception as e:
        print(f"An error occurred while loading submissions: {e}")

def save_submissions_to_file(file_path):
    """Save submissions to file."""
    with open(file_path, 'w') as file:
        for student_id, status in submissions.items():
            file.write(f"{student_id},{status}\n")

def check_submission_status(student_id):
    """Check submission status."""
    if student_id in submissions:
        return submissions[student_id]
    else:
        return "No submission found for this student."

def update_submission_status(student_id, status):
    """Update submission status."""
    submissions[student_id] = status
    print(f"Submission status updated for student {student_id} to {status}")
    save_submissions_to_file(file_path)

def main():
    """Main function to run the script."""
    # Load data from the file
    load_courses_from_file(file_path)
    load_submissions_from_file(file_path)

    while True:
        print("\nMenu:")
        print("1. Submit Assignment")
        print("2. Check Assignment Status")
        print("3. Update Assignment Status")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            course_name = input("Enter course name: ")
            student_id = input("Enter student ID: ")
            assignment_title = input("Enter assignment title: ")
            submit_assignment(course_name, student_id, assignment_title)
        elif choice == '2':
            course_name = input("Enter course name: ")
            student_id = input("Enter student ID: ")
            check_assignment_status(course_name, student_id)
        elif choice == '3':
            course_name = input("Enter course name: ")
            assignment_title = input("Enter assignment title: ")
            status = input("Enter new status: ")
            update_assignment_status(course_name, assignment_title, status)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
