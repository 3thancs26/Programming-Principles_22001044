def calculate_attendance(student_id, subject_code):
    total_classes = 25  # Total number of classes for each subject
    attended_classes = 0

    try:
        with open('attendance_StudentID.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 3:  # Ensure the line contains at least three elements (student ID, subject code, and date)
                    if data[1].strip() == student_id and data[2].strip() == subject_code:  # Comparing student ID and subject code
                        attended_classes += 1
    except FileNotFoundError:
        print("Attendance file not found.")
        return None

    attendance_percentage = (attended_classes / total_classes) * 100
    return attendance_percentage

# Example usage:
student_id = input("Enter student's ID: ")
subject_code = input("Enter subject code: ").upper()

# Call the function with provided arguments
attendance_percentage = calculate_attendance(student_id, subject_code)
if attendance_percentage is not None:
    print(f"Attendance percentage for student {student_id} in subject {subject_code}: {attendance_percentage:.2f}%")
