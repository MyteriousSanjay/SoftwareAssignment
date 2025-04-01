import json
from datetime import datetime
import getpass

# Constants
DATABASE_FILE = "database.json"

class MarksManager:
    def __init__(self):
        self.load_database()
        self.current_teacher = None

    def load_database(self):
        """Load the JSON database from file"""
        try:
            with open(DATABASE_FILE, 'r') as f:
                self.database = json.load(f)
        except FileNotFoundError:
            print("Database file not found. Creating new database.")
            self.database = {
                "students": [],
                "status": "editing",
                "last_updated": datetime.now().isoformat()
            }
            self.save_database()

    def save_database(self):
        """Save the database to file"""
        with open(DATABASE_FILE, 'w') as f:
            json.dump(self.database, f, indent=2)
        print("Changes saved to database.")

    def teacher_login(self):
        """Simple teacher authentication"""
        teachers = {
            "math_teacher": {"password": "math123", "subject": "math"},
            "physics_teacher": {"password": "physics123", "subject": "physics"},
            "chemistry_teacher": {"password": "chemistry123", "subject": "chemistry"}
        }

        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        if username in teachers and teachers[username]["password"] == password:
            self.current_teacher = username
            return teachers[username]["subject"]
        else:
            print("Invalid credentials")
            return None

    def update_marks(self, subject):
        """Update marks for the teacher's subject"""
        print("\nCurrent Students:")
        for student in self.database["students"]:
            print(f"\nRoll: {student['roll_number']}, Name: {student['name']}")
            print(f"Current {subject} marks: {student['marks'].get(subject, 'N/A')}")

        roll_number = input("\nEnter student roll number to update: ")
        new_mark = input(f"Enter new {subject} mark (0-100): ")

        # Validate input
        try:
            new_mark = int(new_mark)
            if not 0 <= new_mark <= 100:
                raise ValueError
        except ValueError:
            print("Invalid mark. Must be integer between 0-100.")
            return

        # Find and update student
        updated = False
        for student in self.database["students"]:
            if student["roll_number"] == roll_number:
                # Initialize marks dictionary if it doesn't exist
                if "marks" not in student:
                    student["marks"] = {}
                student["marks"][subject] = new_mark
                student["last_updated"] = datetime.now().isoformat()
                updated = True
                break

        if updated:
            self.database["last_updated"] = datetime.now().isoformat()
            self.save_database()
            print("Marks updated successfully!")
            # Show updated record
            for student in self.database["students"]:
                if student["roll_number"] == roll_number:
                    print(f"\nUpdated Record:")
                    print(f"Roll: {student['roll_number']}, Name: {student['name']}")
                    print(f"{subject}: {student['marks'].get(subject, 'N/A')}")
                    break
        else:
            print("Student not found.")

    def view_all_marks_public(self):
        """Public view of all marks (no authentication required)"""
        if not self.database["students"]:
            print("\nNo student records available.")
            return
            
        print("\n=== PUBLIC MARKS VIEW ===")
        print(f"Last Updated: {self.database.get('last_updated', 'Unknown')}")
        print("="*30)
        
        for student in sorted(self.database["students"], 
                            key=lambda x: sum(x.get("marks", {}).values()), 
                            reverse=True):
            print(f"\nRoll: {student['roll_number']}")
            print(f"Name: {student['name']}")
            marks = student.get("marks", {})
            for subject, mark in marks.items():
                print(f"{subject.title()}: {mark}")
            print(f"TOTAL: {sum(marks.values())}")
            print("-"*30)

    def view_marks(self, subject=None):
        """View marks for all students (filtered by subject if provided)"""
        if not self.database["students"]:
            print("\nNo student records available.")
            return
            
        print("\nStudent Marks:")
        for student in self.database["students"]:
            print(f"\nRoll: {student['roll_number']}, Name: {student['name']}")
            marks = student.get("marks", {})
            if subject:
                print(f"{subject}: {marks.get(subject, 'N/A')}")
            else:
                for subj, mark in marks.items():
                    print(f"{subj}: {mark}")
                print(f"Total: {sum(marks.values())}")

def teacher_menu(manager, subject):
    """Menu for authenticated teachers"""
    while True:
        print("\nMarks Management System (Teacher Mode)")
        print(f"Logged in as {manager.current_teacher} ({subject})")
        print("1. Update marks")
        print("2. View marks (my subject)")
        print("3. View all marks")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            manager.update_marks(subject)
        elif choice == "2":
            manager.view_marks(subject)
        elif choice == "3":
            manager.view_marks()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

def public_menu(manager):
    """Menu for public users"""
    while True:
        print("\nMarks Management System (Public View)")
        print("1. View all marks")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            manager.view_all_marks_public()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Try again.")

def main():
    manager = MarksManager()
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Teacher Login")
        print("2. Public Marks View")
        print("3. Exit System")

        choice = input("Enter your choice: ")

        if choice == "1":
            subject = manager.teacher_login()
            if subject:
                teacher_menu(manager, subject)
        elif choice == "2":
            public_menu(manager)
        elif choice == "3":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()