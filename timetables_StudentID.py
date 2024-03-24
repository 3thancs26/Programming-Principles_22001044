def create_timetable():
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
    with open("timetables_StudentID.txt", "a") as file:  
        file.write(f"{subject_code}, {subject_name}, {instructor}, {room}, {start}-{end}, {weekday}\n")

def update_timetable():
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

    with open("timetables_StudentID.txt", "a") as file:  
        file.write(f"{subject_code}, {subject_name}, {instructor}, {room}, {start}-{end}, {weekday}\n")

def delete_timetable():
    subject_to_delete = input("Enter the subject code to delete: ")
    try:
        with open("timetables_StudentID.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Timetable file not found.")
        return
    remaining_lines = [line for line in lines if subject_to_delete not in line]
    try:
        with open("timetables_test.txt", "w") as file:
            for line in remaining_lines:
                file.write(line)
    except Exception as e:
        print("An error occurred while deleting the timetable:", e)
        return
    
    print("Timetable for", subject_to_delete, "has been deleted.")


def read_timetable():
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


def main():
    while True:
        print("[1] Create course timetable")
        print("[2] Update course timetable")
        print("[3] Delete course timetable")
        print("[4] Read course timetable")
        print("[5] Exit")
        selection = input("Please select 1, 2, 3, 4, or 5: ")
        
        if selection == "1":
            create_timetable()
        elif selection == "2":
            update_timetable()
        elif selection == "3":
            delete_timetable()
        elif selection == "4":
            read_timetable()
        elif selection == "5":
            print("Exiting...")
            break
        else:
            print("ERROR: Invalid Selection")
    return 0
main()