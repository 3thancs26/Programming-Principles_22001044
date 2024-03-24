# Function to submit assignment
def submit_assignment(student_id, assignment_name):
    # Create or update the submission file
    with open(f"{student_id_submissions}/{assignment_name}.txt", "w") as file:
        file.write("Submitted")

    print("Assignment submitted successfully.")

# Function to check assignment status
def check_assignment_status(student_id, assignment_name):
    submission_path = f"{student_id}_submissions/{assignment_name}.txt"
    try:
        with open(submission_path, "r") as file:
            status = file.read()
            print(f"Assignment status for {assignment_name}: {status}")
    except FileNotFoundError:
        print("Assignment not submitted yet.")

# Function to update assignment status (for faculty)
def update_assignment_status(student_id, assignment_name, new_status):
    submission_path = f"{student_id}_submissions/{assignment_name}.txt"
    try:
        with open(submission_path, "w") as file:
            file.write(new_status)
        print("Assignment status updated successfully.")
    except FileNotFoundError:
        print("Assignment not found.")

def main():
    students = [
        {"name": "YEOH JIE LONG", "student_id": "22071112", "course_code": "NET1024", "assignment_name": "Networking Packet Tracer"},
        {"name": "OOI JIN YON", "student_id": "22039069", "course_code": "NET1024", "assignment_name": "Networking Packet Tracer"}, 
        {"name": "LOH CHEE SUM", "student_id": "22001044", "course_code": "NET1024", "assignment_name": "Networking Packet Tracer"}, 
        {"name": "LIANG YRENN DA", "student_id": "22067128", "course_code": "NET1024", "assignment_name": "Networking Packet Tracer"}, 
        {"name": "PEGGY LIOW EN KI", "student_id": "23020852", "course_code": "NET1024", "assignment_name": "Networking Packet Tracer"},
    ]

    # Prompt the user for input
    user_input = input("Enter a student_id or assignment_name: ")

    # Check if the input matches any student_id or assignment_name
    for student in students:
        if user_input in [student["student_id"], student["assignment_name"]]:
            print("Student found - Name:", student["name"], "id:", student["student_id"], "course_code:", student["course_code"])
            submit_assignment(student["student_id"], student["assignment_name"])
            check_assignment_status(student["student_id"], student["assignment_name"])
            update_choice = input("Do you want to update assignment status? (yes/no): ").lower()
            if update_choice == "yes":
                new_status = input("Enter the new status: ")
                update_assignment_status(student["student_id"], student["assignment_name"], new_status)
            break
    else:
        print("Student not found.")

    return 0

if __name__ == "__main__":
    main()