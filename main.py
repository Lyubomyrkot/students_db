import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        self.connect()
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        data = cursor.fetchall()
        self.close()
        return data
        

db = DatabaseManager('students.db')

while True:
    print("0. Вихід")
    print("1. Показати всіх студентів")
    print("2. Показати всі курси")
    print("3. Додати студента")
    print("4. Додати курс")
    print("5. Записати студента на курс")
    print("6. Показати курси студента")
    print("7. Показати студентів курсу")

    choice = input("Enter your choice: ")
    
    if choice =="0":
        break
    
    elif choice == "1":
        students = db.execute_query('SELECT * FROM students')
        for student in students:
            print(student)
    
    elif choice == "2":
        courses = db.execute_query('SELECT * FROM courses')
        for course in courses:
            print(course)
    
    elif choice == "3":
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        grade = input("Enter student grade: ")
        db.execute_query('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    
    elif choice == "4":
        name = input("Enter course name: ")
        db.execute_query('INSERT INTO courses (name) VALUES (?)', (name,))
    
    elif choice == "5":
        student_id = int(input("Enter student ID: "))
        course_id = int(input("Enter course ID: "))
        db.execute_query('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
    
    elif choice == "6":
        student_id = int(input("Enter student ID: "))
        courses = db.execute_query('''
            SELECT courses.name 
            FROM courses 
            JOIN enrollments ON courses.id = enrollments.course_id 
            WHERE enrollments.student_id = ?
        ''', (student_id,))
        for course in courses:
            print(course[0])
    
    elif choice == "7":
        course_id = int(input("Enter course ID: "))
        students = db.execute_query('''
            SELECT students.name 
            FROM students 
            JOIN enrollments ON students.id = enrollments.student_id 
            WHERE enrollments.course_id = ?
        ''', (course_id,))
        for student in students:
            print(student[0])
    
    else:
        print("Invalid choice. Please try again.")


    