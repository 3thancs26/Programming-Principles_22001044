import random
import datetime

# Assuming valid_subject_codes is defined globally
valid_subject_codes = ['CS101', 'NET1014', 'MAT1024']

def read_student_data(file_path):
    student_data = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                student_info = line.strip().split(',')
                if len(student_info) >= 2:  # Ensure the line contains at least two elements (name and ID)
                    name = student_info[0].strip()
                    student_id = student_info[1].strip()
                    student_data[student_id] = name
    except FileNotFoundError:
        print("File not found or path is incorrect.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return student_data

def student_login():
    file_path = 'attendance_StudentID.txt'
    student_data = read_student_data(file_path)
    if not student_data:
        print("No valid student IDs found in the file.")
        return
    
    while True:
        user_input = input("Enter your student ID (type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Exiting...")
            break
        if user_input in student_data:
            print(f"Name: {student_data[user_input]}, Student ID: {user_input}")
            break
        else:
            print("Invalid student ID. Please try again.")

def generate_check_in_code(subject_code):
    generated_code = str(random.randint(100000, 999999))
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"The check-in code for subject {subject_code} on {current_date} is: {generated_code}")
    return generated_code, current_date

def is_code_valid(generated_time):
    current_time = datetime.datetime.now()
    generated_time = datetime.datetime.strptime(generated_time, "%Y-%m-%d %H:%M:%S")
    time_difference = current_time - generated_time
    return time_difference.total_seconds() <= 15*60  # 15 minutes in seconds

def mark_attendance():
    subject_code = input("Enter subject code: ").strip().upper()
    if subject_code not in valid_subject_codes:
        print("Invalid subject code. Please enter a valid subject code.")
        return

    generated_code, generated_time = generate_check_in_code(subject_code)

    student_code = input("Please enter the check-in code: ")
    if student_code.lower() == 'quit':
        print("Exiting...")
        return
    if not is_code_valid(generated_time):
        print("The check-in code has expired.")
        return
    if student_code != generated_code:
        print("Invalid check-in code. Please try again.")
        return

    # Verify student ID
    student_id = input("Enter student's ID: ")
    student_data = read_student_data('attendance_StudentID.txt')
    if student_id not in student_data:
        print("Invalid student ID. Please try again.")
        return

    student_name = student_data[student_id]  # Use the name from student_data
    with open('attendance_StudentID.txt', 'a') as f:
        f.write(f"{student_name}, {student_id}, {subject_code}, {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
    print(f"Attendance marked successfully for {student_name} in subject {subject_code}.")

# Placeholder for read_timetable(), assuming it returns a dictionary {subject_code: total_classes}
def read_timetable(file_path):
    # Implement this function to read the timetable data from a file
    # Example return format: [('CS101', '2024-03-15'), ('NET1014', '2024-03-16'), ...]
    pass

def calculate_attendance_percentage():
    # Assuming 'attendance_StudentID.txt' records each attendance with subject code and date
    attendance_records = {}
    with open('attendance_StudentID.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 4:  # Ensure the line has all required parts
                continue
            student_name, student_id, subject_code, date = parts
            key = (student_id, subject_code)
            attendance_records.setdefault(key, []).append(date)

    timetable_data = read_timetable('timetable.txt')  # Assuming this function is implemented
    total_classes_per_subject = {}
    for subject_code, _ in timetable_data:
        total_classes_per_subject[subject_code] = total_classes_per_subject.get(subject_code, 0) + 1

    attendance_percentage = {}
    for (student_id, subject_code), dates in attendance_records.items():
        total_classes = total_classes_per_subject.get(subject_code, 0)
        if total_classes == 0:
            continue  # Avoid division by zero
        percentage = len(dates) / total_classes * 100
        attendance_percentage.setdefault(student_id, {}).update({subject_code: percentage})

    # Optionally, format the output for better readability or further processing
    for student_id, percentages in attendance_percentage.items():
        student_name = student_data.get(student_id, "Unknown Student")
        print(f"Attendance for {student_name} ({student_id}):")
        for subject_code, percentage in percentages.items():
            print(f" - {subject_code}: {percentage:.2f}%")
    return attendance_percentage


# Example of how to structure your main program flow
def main():
    while True:
        print("\nClassroom Management System Menu")
        print("1. Student Login")
        print("2. Mark Attendance")
        print("3. Calculate Attendance Percentage")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            student_login()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            calculate_attendance_percentage()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
