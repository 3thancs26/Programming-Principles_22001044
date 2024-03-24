import os
import random
import json
from datetime import datetime,timedelta

class ClassroomManagementSystem:
    def __init__(self):
        self.attendance_file = "attendance_StudentID.txt"
        self.timetable_file = "timetables_StudentID.txt"
        self.assignment_file = "assignment_StudentID.txt"
        self.file_path = "assignment_studentID.txt"
        self.courses = {}
        self.submissions = {}
        self.generated_codes = {}

    # Utility functions
    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def read_data_from_file(self, filename):
        """Read data from a file and return as a list of lines."""
        try:
            with open(filename, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return []

    def write_data_to_file(self, filename, data):
        """Write data to a file, each item on a new line."""
        with open(filename, "a") as file:
            for line in data:
                file.write(f"{line}\n")
    # Mark Attendance System 
    def read_student_data(self):
        student_data = {}
        try:
            with open(self.attendance_file, 'r') as f:
                for line in f:
                    student_info = line.strip().split(',')
                    if len(student_info) >= 2:
                        name = student_info[0].strip()
                        student_id = student_info[1].strip()
                        student_data[student_id] = name
        except FileNotFoundError:
            print("File not found or path is incorrect.")
        except Exception as e:
            print("An error occurred:", e)
        return student_data

    def teacher_login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == "eduhub" and password == "eduhub":
            print("Teacher login successful.")
            self.generate_check_in_code()
            return True
        else:
            print("Invalid username or password.")
            return False

    def student_login(self):
        student_data = self.read_student_data()
        if not student_data:
            print("No valid student IDs found in the file. Please contact School IT Department @ eduhub@imail.eduhub.edu.my")
            return False
        
        while True:
            user_input = input("Enter your student ID (type 'quit' to exit): ")
            if user_input.lower() == 'quit':
                print("Exiting...")
                return False
            if user_input in student_data:
                print(f"Name: {student_data[user_input]}, Student ID: {user_input}")
                return True
            else:
                print("Invalid student ID. Please try again.")

    def generate_check_in_code(self):
        subject_code = input("Enter subject code for attendance: ").strip().upper()
        generated_code = str(random.randint(100000, 999999))
        current_time = datetime.now()
        expiration_time = current_time + timedelta(minutes=15)
        self.generated_codes[subject_code] = {'code': generated_code, 'expiration_time': expiration_time}
        print(f"The check-in code for subject {subject_code} on {current_time.strftime('%Y-%m-%d %H:%M:%S')} is: {generated_code}")

    def is_code_valid(self, generated_time):
        current_time = datetime.now()
        return current_time <= generated_time

    def mark_attendance(self):
        valid_subject_codes = ['CSC101', 'NET1014', 'MAT1024','CSC1024', 'BIS1014', 'MPU3183', 'PSY1014']
        student_logged_in = self.student_login()
        if not student_logged_in:
            return
        
        while True:    
            subject_code = input("Enter subject code: ").strip().upper()
            if subject_code in valid_subject_codes:
                generated_code_info = self.generated_codes.get(subject_code)
                if generated_code_info and self.is_code_valid(generated_code_info['expiration_time']):
                    generated_code = generated_code_info['code']
                    break
                else:
                    print("The check-in code has expired.")
            else:
                print("Invalid subject code. Please enter valid subject code only")

        while True:
            student_code = input("Please enter the check-in code: ")
            if student_code.lower() == 'quit':
                print("Exiting...")
                break
            if student_code == generated_code:
                student_id = input("Enter student's ID: ")
                student_data = self.read_student_data()
                if student_id in student_data:
                    student_name = input("Enter student's full name: ").upper()
                    weekday = datetime.now().strftime('%A')
                    
                    with open(self.attendance_file, 'a') as f:
                        f.write(f"{student_name}, {student_id}, {subject_code}, {datetime.now().strftime('%Y-%m-%d')}, {weekday}\n")

                    print(f"Attendance marked successfully for subject {subject_code} on {datetime.now().strftime('%Y-%m-%d')}.")
                    return
                else:
                    print("Invalid student ID. Please try again.")
            else:
                print("Invalid check-in code. Please try again.")

    def calculate_attendance(self, student_id, subject_code):
        total_classes = 25
        attended_classes = 0

        try:
            with open(self.attendance_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 3:
                        if data[1].strip() == student_id and data[2].strip() == subject_code:
                            attended_classes += 1
        except FileNotFoundError:
            print("Attendance file not found.")
            return None

        attendance_percentage = (attended_classes / total_classes) * 100
        return attendance_percentage

    def check_attendance(self):
        student_logged_in = self.student_login()
        if not student_logged_in:
            return
        
        student_id = input("Enter student's ID: ")
        student_data = self.read_student_data()
        if student_id in student_data:
            subject_code = input("Enter subject code: ").upper()
            valid_subject_codes=['CSC101','NET1014','MAT1024','CSC1024','BIS1014','MPU3183','PSY1014']
            if subject_code in valid_subject_codes:
                attendance_percentage = self.calculate_attendance(student_id, subject_code)
                if attendance_percentage is not None:
                    print(f"Attendance percentage for student {student_id} in subject {subject_code}: {attendance_percentage:.2f}%")
            else:
                print("Invalid subject_code. Please enter a valid subject code.")
        else:
            print("Invalid student ID. Please try again.")
            
    def display_attendance_records(self):
        try:
            print("Displaying Attendance Records:")
            print("{:<30} {:<15} {:<15} {:<15} {:<15}".format("Name", "Student ID", "Course", "Date", "Day"))
            with open(self.attendance_file, 'r') as f:
                for record in f:
                    record_data = map(str.strip, record.split(','))
                    record_data = list(record_data)  # Convert map object to list
                    if len(record_data) >= 5:
                        name, student_id, course, date, day = record_data[:5]
                        print("{:<30} {:<15} {:<15} {:<15} {:<15}".format(name, student_id, course, date, day))
                    else:
                        print(f"Invalid record: {record_data}. Skipping...")
        except ValueError as e:
            print(f"Error processing record: {record}. Error: {e}")

    def manage_attendance(self):
        while True:
            print("[1] Teacher Login and Generate Code")
            print("[2] Student Mark Attendance")
            print("[3] Check Attendance")
            print("[4] Exit to main menu")
            choice = input("Enter your choice (1, 2, 3 or 4): ")

            if choice == '1':
                self.teacher_login()
            elif choice == '2':
                self.mark_attendance()
            elif choice == '3':
                self.check_attendance()
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                

    # TIMETABLE MANAGEMENT SYSTEM
    def create_timetable_teacher(self):
        teacher_username = 'eduhub'
        teacher_password = 'eduhub'
        entered_username = input("Please enter your username: ")
        entered_password = input("Please enter your password: ")
        if entered_username != teacher_username or entered_password != teacher_password:
            print("Authentication failed. Only lecturers and admins are allowed to create timetables.")
            return
            
        subject_code = input("Please enter subject code: ")
        subject_name = input("Please enter subject name: ")
        instructor = input("Please enter your subject instructor: ")
        room = input("Please enter the classroom number: ")
        start = input("Please enter your start time (HH:MM): ")
        end = input("Please enter your end time (HH:MM): ")
        weekday = input("Please enter your weekday of class: ")
        try:
            start_hour, start_minute = map(int, start.split(":"))
            end_hour, end_minute = map(int, end.split(":"))
            if not (0 <= start_hour < 24 and 0 <= start_minute < 60 and 0 <= end_hour < 24 and 0 <= end_minute < 60):
                raise ValueError("Invalid time format.")
        except ValueError:
            print("Error: Invalid time format. Please use HH:MM.")
            return
        with open(self.timetable_file, "w") as file:  
            file.write(f"{subject_code}, {subject_name}, {instructor}, {room}, {start}-{end}, {weekday}\n")

    def update_timetable_teacher(self):
        teacher_username = 'eduhub'
        teacher_password = 'eduhub'
        entered_username = input("Please enter your username: ")
        entered_password = input("Please enter your password: ")
        if entered_username != teacher_username or entered_password != teacher_password:
            print("Authentication failed. Only lecturers and admins are allowed to update timetables.")
            return
        
        subject_code = input("Please enter subject code: ")
        subject_name = input("Please enter subject name: ")
        instructor = input("Please enter your subject instructor: ")
        room = input("Please enter the classroom number: ")
        start = input("Please enter your start time (HH:MM): ")
        end = input("Please enter your end time (HH:MM): ")
        weekday = input("Please enter your weekday of class: ")
        try:
            start_hour, start_minute = map(int, start.split(":"))
            end_hour, end_minute = map(int, end.split(":"))
            if not (0 <= start_hour < 24 and 0 <= start_minute < 60 and 0 <= end_hour < 24 and 0 <= end_minute < 60):
                raise ValueError("Invalid time format.")
        except ValueError:
            print("Error: Invalid time format. Please use HH:MM.")
            return

        with open(self.timetable_file, "a") as file:  
            file.write(f"{subject_code}, {subject_name}, {instructor}, {room}, {start}-{end}, {weekday}\n")

    def delete_timetable_teacher(self):
        teacher_username = 'eduhub'
        teacher_password = 'eduhub'
        entered_username = input("Please enter your username: ")
        entered_password = input("Please enter your password: ")
        if entered_username != teacher_username or entered_password != teacher_password:
            print("Authentication failed. Only lecturers and admins are allowed to delete timetables.")
            return

        subject_to_delete = input("Enter the subject code to delete: ")
        try:
            with open(self.timetable_file, "r") as file:
                lines = file.readlines()
            with open(self.timetable_file, "w") as file:
                for line in lines:
                    if subject_to_delete not in line.split(',')[0]:
                        file.write(line)
            print(f"Timetable for {subject_to_delete} has been deleted.")
        except FileNotFoundError:
            print("Timetable file not found.")
        except Exception as e:
            print(f"An error occurred while deleting the timetable: {e}")
    
    def read_timetable_student(self):
        print("View course timetable")
        try:
            with open("timetables_StudentID.txt", "r") as file:
                timetable_data = []
                for line in file:
                    data = line.strip().split(", ")
                    subject_code, subject_name, instructor, room, time, weekday = data
                    start_time, end_time = map(lambda x: x.strip(), time.split("-"))
                    start_hour, start_minute = map(int, start_time.split(":"))
                    if "PM" in start_time and start_hour != 12:
                        start_hour += 12
                    end_hour, end_minute = map(int, end_time.split(":"))
                    if "PM" in end_time and end_hour != 12:
                        end_hour += 12
                    time_range = "{:02d}:{:02d} - {:02d}:{:02d}".format(start_hour, start_minute, end_hour, end_minute)
                    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    weekday_index = weekdays.index(weekday)
                    timetable_data.append((subject_code, subject_name, instructor, room, time_range, weekday_index))

                sorted_timetable_data = sorted(timetable_data, key=lambda x: (x[5], x[4]))

                print("{:<10} {:<50} {:<40} {:<10} {:<20} {:<10}".format(
                    "Code", "Subject", "Instructor", "Room", "Time", "Weekday"))
                for entry in sorted_timetable_data:
                    print("{:<10} {:<50} {:<40} {:<10} {:<20} {:<10}".format(
                        entry[0], entry[1], entry[2], entry[3], entry[4], weekdays[entry[5]]))
        except FileNotFoundError:
            print("Timetable file not found.")
        except ValueError:
            print("Error: Incorrect format in the timetable file.")
        except Exception as e:
            print("An error occurred:", e)

    def manage_timetable(self):
        while True:
            print("[1] Create course timetable (Log In Required)")
            print("[2] Update course timetable (Log In Required)")
            print("[3] Delete course timetable (Log In Required)")
            print("[4] Exit to main menu")
            selection = input("Please select 1, 2, 3, or 4: ")
                
            if selection == "1":
                self.create_timetable_teacher()
            elif selection == "2":
                self.update_timetable_teacher()
            elif selection == "3":
                self.delete_timetable_teacher()
            elif selection == "4":
                print("Exit to main menu")
                break
            else:
                print("ERROR: Invalid Selection")

    # ASSIGNMENT MANAGEMENT SYSTEM
    def submit_assignment(self, course_name, student_id, assignment_title):
        """Submit an assignment."""
        if course_name not in self.courses:
            self.courses[course_name] = []
        assignment = {'course_name': course_name, 'student_id': student_id, 'title': assignment_title, 'status': 'Submit'}
        self.courses[course_name].append(assignment)
        print(f"Assignment '{assignment_title}' submitted successfully by {student_id} for course {course_name}")
        self.save_courses_to_file()

    def check_assignment_status(self, course_name, student_id):
        """Check assignment status for a student."""
        if course_name in self.courses:
            assignments = [assignment for assignment in self.courses[course_name] if assignment['student_id'] == student_id]
            if assignments:
                for assignment in assignments:
                    print(f"Assignment '{assignment['title']}' status: {assignment['status']}")
            else:
                print(f"No assignment submitted by {student_id} for course {course_name}")
        else:
            print(f"Course {course_name} does not exist.")

    def update_assignment_status(self, course_name, assignment_title, status):
        """Update assignment status."""
        if course_name in self.courses:
            for assignment in self.courses[course_name]:
                if assignment['title'] == assignment_title:
                    assignment['status'] = status
                    print(f"Assignment '{assignment_title}' status updated to '{status}'")
                    self.save_courses_to_file()
                    return
        print(f"No assignment found with title '{assignment_title}' in course {course_name}")

    def load_courses_from_file(self):
        """Load courses from file."""
        try:
            with open(self.file_path, 'r') as file:
                self.courses = json.load(file)
        except FileNotFoundError:
            print("File not found. No courses loaded.")
        except Exception as e:
            print(f"An error occurred while loading courses: {e}")

    def save_courses_to_file(self):
        """Save courses to file."""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.courses, file)
        except Exception as e:
            print(f"An error occurred while saving courses: {e}")

    def load_submissions_from_file(self):
        """Load submissions from file."""
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    student_id, status = line.strip().split(',')
                    self.submissions[student_id] = status
        except FileNotFoundError:
            print("File not found. No submissions loaded.")
        except Exception as e:
            print(f"An error occurred while loading submissions: {e}")

    def save_submissions_to_file(self):
        """Save submissions to file."""
        with open(self.file_path, 'w') as file:
            for student_id, status in self.submissions.items():
                file.write(f"{student_id},{status}\n")

    def check_submission_status(self, student_id):
        """Check submission status."""
        if student_id in self.submissions:
            print(f"Submission status for student {student_id}: {self.submissions[student_id]}")
        else:
            print("No submission found for this student.")

    def update_submission_status(self, student_id, status):
        """Update submission status."""
        self.submissions[student_id] = status
        print(f"Submission status updated for student {student_id} to {status}")
        self.save_submissions_to_file()

    def display_assignment_statuses(self):
        print("Displaying Assignment Submission Statuses:")
        print("{:<10} {:<20} {:<10}".format("Student ID", "Assignment", "Status"))
        for record in self.read_data_from_file(self.assignment_file):
            student_id, assignment, status = map(str.strip, record.split(','))
            print("{:<10} {:<20} {:<10}".format(student_id, assignment, status))

    def manage_assignment(self):
        """Main function to manage assignments."""
        self.load_courses_from_file()
        self.load_submissions_from_file()

        while True:
            print("\nMenu:")
            print("[1] Submit Assignment")
            print("[2] Check Assignment Status")
            print("[3] Update Assignment Status")
            print("[4] Exit to main menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                course_name = input("Enter course name: ")
                student_id = input("Enter student ID: ")
                assignment_title = input("Enter assignment title: ")
                self.submit_assignment(course_name, student_id, assignment_title)
            elif choice == '2':
                course_name = input("Enter course name: ")
                student_id = input("Enter student ID: ")
                self.check_assignment_status(course_name, student_id)

            
            elif choice == '3':
                course_name = input("Enter course name: ")
                assignment_title = input("Enter assignment title: ")
                status = input("Enter new status: ")
                self.update_assignment_status(course_name, assignment_title, status)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_display(self):        
        print("[1] Display Attendance")
        print("[2] Display Timetables")
        print("[3] Display Assignment")
        print("[4] Display all")
        print("[5] Exit to main menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nDisplaying Attendance Records:")
            self.display_attendance_records()

        elif choice == '2':
            print("\nDisplaying Timetables:")
            self.read_timetable_student()  # Fixed method call
            
        elif choice == '3':
            print("\nDisplaying Assignment Submission Statuses:")
            self.display_assignment_statuses()

        elif choice == '4':
            print("\nDisplaying Attendance Records:")
            self.display_attendance_records()

            print("\nDisplaying Timetables:")
            self.read_timetable_student()
            
            print("\nDisplaying Assignment Submission Statuses:")
            self.display_assignment_statuses()

        elif choice == '5':
            print("Exiting program. Goodbye!")
            return
    
        else:
            print("Invalid choice. Please try again.")

    def readme(self):
        def center_bold_italic(text):
            return f"\033[1m{text}\033[0m"

        def print_section_heading(heading):
            print(center_bold_italic(f"\n{heading}"))

        def print_subsection_heading(heading):
            print(center_bold_italic(f"\n{heading}:"))

        print_section_heading("Edu Hub Classroom Management System User Manual")

        print_section_heading("Introduction:")
        print("Welcome to the Edu Hub Classroom Management System (Edu Hub CMS)! This system is designed to facilitate various administrative tasks within an educational institution, including attendance tracking, timetable management, and assignment submission tracking. It provides both teachers and students with tools to streamline these processes effectively.\n")

        print_section_heading("Getting Started:")
        print("To use the Classroom Management System, follow these steps:")
        print_subsection_heading("Installation")
        print("No installation is required for this program. You can directly run the provided Python script on your local machine, assuming you have Python installed.")
        print_subsection_heading("Launch the Program")
        print("Open the command line interface (CLI) or terminal on your computer. Navigate to the directory where the Python script (classroom_management_system.py) is located.")
        print_subsection_heading("Run the Program in Terminal")
        print("Type `py final.py` in Windows or `python3 final.py` on Mac/Linux and press Enter to execute the script.")
        print_subsection_heading("Main Menu")
        print("Once the program is running, you will be presented with a main menu offering different functionalities of the Classroom Management System.\n")

        print_section_heading("Functionality Overview:")
        print("1. Mark Attendance:")
        print("   - Teachers can mark attendance for students in their classes.")
        print("   - Students can log in to check their attendance status.")
        print("2. Manage Timetables:")
        print("   - Teachers can create, update, and delete course timetables.")
        print("   - Students can view their course timetables.")
        print("3. Submit Assignment:")
        print("   - Students can submit assignments for their courses.")
        print("   - Teachers can check and update assignment statuses.")
        print("4. Display Data:")
        print("   - Users can choose to display:")
        print("       - Attendance records")
        print("       - Course timetables")
        print("       - Assignment submission statuses")
        print("       - All of the above combined")
        print("5. Exit:")
        print("   - Exit the Classroom Management System.\n")

        print_section_heading("Detailed Functionality:")
        print_subsection_heading("Mark Attendance")
        print("- Teacher Login: Teachers can log in using the provided credentials.")
        print("- Generate Check-in Code: Teachers can generate a unique code for students to check in for attendance. It will expire after 15 Minutes.")
        print("- Mark Attendance: Students can mark their attendance using the generated code within the specified time limit.\n")

        print_subsection_heading("Manage Timetables")
        print("- Create Timetable (Teacher): Teachers can create whole new course timetables by providing relevant details such as subject code, name, instructor, room, and schedule. The Old timetable will be removed. This function is normally used in a new semester.")
        print("- Update Timetable (Teacher): Teachers can update existing course timetables with new information. Normally this function is used to add on any classes.")
        print("- Delete Timetable (Teacher): Teachers can delete course timetables for specific subjects.")
        print("- View Timetable (Student): Students can view their course timetables.\n")

        print_subsection_heading("Submit Assignment")
        print("- Submit Assignment: Students can submit assignments for their courses by providing necessary details like course name, student ID, and assignment title.")
        print("- Check Assignment Status: Students and teachers can check the status of submitted assignments.")
        print("- Update Assignment Status: Teachers can update the status of assignments (e.g., from 'Submit' to 'Graded').\n")

        print_subsection_heading("Display Data")
        print("- Display Attendance Records: View records of attendance, including student name, ID, course, date, and day.")
        print("- Display Timetables: View course timetables, including subject code, name, instructor, room, time, and weekday.")
        print("- Display Assignment Submission Statuses: View the status of submitted assignments for each student.\n")

        print_section_heading("Troubleshooting:")
        print("If you encounter any issues while using the Classroom Management System, please refer to the error messages provided by the system for guidance.")
        print("For further assistance, you can contact your institution's IT department or system administrator.\n")

        print_section_heading("Exiting the Program:")
        print("To exit the Classroom Management System, simply select the 'Exit' option from the main menu.")
        print("Thank you for using the Classroom Management System! Have a productive experience managing your educational tasks efficiently.")
        
def main():
    cms = ClassroomManagementSystem()
    while True:
        print("\nClassroom Management System Menu:")
        print("[1] Mark Attendance")
        print("[2] Manage Timetables")
        print("[3] Submit Assignment")
        print("[4] Display Data")
        print("[5] Exit")
        print("[6] For New Users READ ME!")
        choice = input("Enter your choice: ")

        if choice == '1':
            cms.manage_attendance()
        elif choice == '2':
            cms.manage_timetable()
        elif choice == '3':
            cms.manage_assignment()
        elif choice == '4':
            cms.manage_display()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        elif choice == '6':
            cms.readme()  
        else:
            print("Invalid choice. Please try again.")

'''
USERNAME AND PASSWORD
Username:eduhub
Password:eduhub
'''

main()
