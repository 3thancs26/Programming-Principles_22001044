class Assignment:
    """Represents an assignment."""
    def setup_assignment(self, course_name, student_id, title, status="Pending"):
        self.course_name = course_name
        self.student_id = student_id
        self.title = title
        self.status = status


class Course:
    """Represents a course."""
    def initialize_course(self, name):
        """Initialize the course."""
        self.name = name
        self.assignments = []

    def submit_assignment(self, student_id, assignment_title):
        """Submit an assignment."""
        assignment = Assignment()
        assignment.setup_assignment(self.name, student_id, assignment_title)
        self.assignments.append(assignment)
        print(f"Assignment '{assignment_title}' submitted successfully by {student_id} for course {self.name}")

    def check_assignment_status(self, student_id):
        """Check assignment status for a student."""
        assignments = [assignment for assignment in self.assignments if assignment.student_id == student_id]
        if assignments:
            for assignment in assignments:
                print(f"Assignment '{assignment.title}' status: {assignment.status}")
        else:
            print(f"No assignment submitted by {student_id} for course {self.name}")

    def update_assignment_status(self, assignment_title, status):
        """Update assignment status."""
        assignment = next((assignment for assignment in self.assignments if assignment.title == assignment_title), None)
        if assignment:
            assignment.status = status
            print(f"Assignment '{assignment_title}' status updated to '{status}'")
        else:
            print(f"No assignment found with title '{assignment_title}'")


class Faculty:
    """Represents a faculty member."""
    def initialize_with_name(self, name):
        """Initialize the faculty member."""
        self.name = name

    def update_assignment_status(self, course, assignment_title, status):
        """Update assignment status as a faculty member."""
        course.update_assignment_status(assignment_title, status)


class AssignmentSubmissionSystem:
    """Assignment submission system."""
    def initialize(self):
        """Initialize the submission system."""
        self.submissions = {}

    def load_submissions_from_file(self, file_path):
        """Load submissions from file."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    student_id, status = line.strip().split(',')
                    self.submissions[student_id] = status
        except FileNotFoundError:
            print("File not found. No submissions loaded.")

    def update_submission_status(self, student_id, status):
        """Update submission status."""
        if student_id in self.submissions:
            self.submissions[student_id] = status
            return True
        else:
            return False

    def check_submission_status(self, student_id):
        """Check submission status."""
        return self.submissions.get(student_id, "No submission found for this student.")

    def save_submissions_to_file(self, file_path):
        """Save submissions to file."""
        with open(file_path, 'w') as file:
            for student_id, status in self.submissions.items():
                file.write(f"{student_id},{status}\n")


def submit_or_check_assignments(course, submission_system):
    """Submit or check assignments."""
    while True:
        print("\nAssignment Submission Menu:")
        print("1. Submit Assignment")
        print("2. Check Assignment Status")
        print("3. Update Assignment Status (Faculty)")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            student_id = input("Enter student ID: ")
            assignment_title = input("Enter assignment title: ")
            course.submit_assignment(student_id, assignment_title)
        elif choice == '2':
            student_id = input("Enter student ID: ")
            submission_status = submission_system.check_submission_status(student_id)
            print(submission_status)
        elif choice == '3':
            if isinstance(submission_system, Faculty):
                assignment_title = input("Enter assignment title: ")
                status = input("Enter new status: ")
                course.update_assignment_status(assignment_title, status)
            else:
                print("Access denied. Only faculty members can update assignment status.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    python_course = Course()
    submission_system = AssignmentSubmissionSystem()

    submission_system.load_submissions_from_file("assignments_StudentID.txt")

    while True:
        print("\nMAIN MENU:")
        print("1. Submit/Check Assignments")
        print("2. Mark Attendance")
        print("3. Manage Timetables")
        print("4. Display")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            submit_or_check_assignments(python_course, submission_system)
        elif choice == '2':
            print("Marking attendance...")
        elif choice == '3':
            print("Managing timetables...")
        elif choice == '4':
            print("Displaying data...")
        elif choice == '5':
            submission_system.save_submissions_to_file("assignments_StudentID.txt")
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
