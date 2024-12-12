# 🎓 Student Database Management System
---

**Student Database Management System** is a web application built using **Streamlit**, **MySQL**, and **Python**. It allows users to store, manage, and visualize student records, including student names, ages, and grades. Users can add new students, view the list of students, update existing student records, and delete student records.

This application also supports downloading the student records in both **CSV** and **Excel** formats.

---
- [🎓 Student Database Management System](#-banking-system)
  - [Features](#features)
  - [Tech Stack](#tech)
  - [Directory Structure:](#directory)
  - [Setup](#Setup)
  - [Installation](#installation)
  - [Database Setup](#database)
  - [Prerequisites](#Prerequisites)
  - [Install Dependencies](#Install-Dependencies)
  - [Code Logic](#Code)
  - [Download Options](#Download)
  - [Error Handling](#Error)
  - [Contributing](#Contributing)
  - [Acknowledgments](#Acknowledgments)
  - [Stay Connected](#Stay)
  - [License](#License)
 
---
## Features

- **Add Student**: Add a new student to the database by entering their name, age, and grade.
- **View Students**: View the list of all students in a tabular format, with the option to download the records as **CSV** or **Excel**.
- **Update Student**: Select a student to update their details, such as name, age, and grade.
- **Delete Student**: Select a student to delete their record from the database.

---

## Tech Stack

- **Frontend**: Streamlit (for building the web interface)
- **Backend**: Python (for logic and API calls)
- **Database**: MySQL (for storing student records)
- **Environment**: `.env` file for storing sensitive information like database credentials

---
## Directory Structure:
    
```bash
project/
│
├── .env             # Contains database credentials
├── database.py      # Database-related logic
├── main.py          # Streamlit app for visualization

```

---


## Setup
Install the required dependencies:
```bash
pip install -r requirements.txt
```

Create a .env file in the root directory of the project with the following structure:
  
```bash
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```
---

### Database Setup

* The application will automatically set up the database and create the necessary table on the first run.
* Make sure your MySQL database server is running, and the credentials in the .env file are correct.

---
### Prerequisites

Before running the application, ensure you have the following:

- Python 3.x installed.
- MySQL database running.
- A `.env` file with the database credentials.

---

### Install-Dependencies

1. Clone this repository to your local machine:

    ```bash
   git clone https://github.com/yourusername/student-database-management.git
   cd student-database-management
    ```
    ## Running the Application

    ```bash
        streamlit run main.py
    ```
    ---

## Code Logic
1. Database Connection (database.py)
The create_connection() function establishes a connection to the MySQL database. It accepts a boolean parameter use_database. If set to True, it connects to the database specified in the .env file. If set to False, it connects to MySQL without selecting a database (used for creating the database).

```python
    def create_connection(use_database=True):
    if use_database:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    else:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
```

2. Setting Up the Database (setup_database())
The setup_database() function ensures that the database and table exist. It attempts to create the database if it doesn't exist and then creates the students table with columns for id, name, age, and grade.

```python
    def setup_database():
    try:
        conn = create_connection(use_database=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' ensured to exist.")
        conn.database = DB_NAME

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            grade VARCHAR(10)
        )
        """)
        print("Table 'students' ensured to exist.")
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
```

3. Inserting a New Student (insert_student())
The insert_student() function adds a new student's details into the students table. It takes name, age, and grade as parameters, constructs an SQL query, and executes it.

```python
    def insert_student(name, age, grade):
    conn = create_connection(use_database=True)
    cursor = conn.cursor()

    query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, int(age), grade))
    conn.commit()
    conn.close()
```

4. Fetching All Students (get_all_students())
The get_all_students() function retrieves all records from the students table and returns them as a pandas DataFrame. This DataFrame is used in Streamlit for displaying the student data.

```python
    def get_all_students():
    conn = create_connection(use_database=True)
    query = "SELECT * FROM students"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
```

5. Updating a Student's Details (update_student())
The update_student() function updates a student's information. It takes the student_id, name, age, and grade as parameters and executes an SQL UPDATE query.

```python
    def update_student(student_id, name, age, grade):
    conn = create_connection(use_database=True)
    cursor = conn.cursor()

    query = """
    UPDATE students 
    SET name = %s, age = %s, grade = %s 
    WHERE id = %s
    """
    cursor.execute(query, (name, int(age), grade, int(student_id)))
    conn.commit()
    conn.close()
```

6. Deleting a Student (delete_student())
The delete_student() function deletes a student's record from the students table based on the student's ID.

``` python
    def delete_student(student_id):
    conn = create_connection(use_database=True)
    cursor = conn.cursor()

    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (int(student_id),))
    conn.commit()
    conn.close()
```

7. Streamlit User Interface (main.py)
The user interface (UI) is built using Streamlit. The UI provides a simple form for adding students, a table to view students, and dropdowns to update or delete student records. Additionally, it includes options to download student data in CSV and Excel formats.

```python
    # Streamlit User Interface
    st.set_page_config(page_title="Student Database Management System", layout="wide", page_icon="🎓")

    st.title("🎓 Student Database Management System")

    menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Student":
        # Add new student form
        # ...
    elif choice == "View Students":
        # View all students and provide download options
        # ...
    elif choice == "Update Student":
        # Update selected student
        # ...
    elif choice == "Delete Student":
        # Delete selected student
        # ...
```

---

### Download Options

* CSV Export: Download the list of students in CSV format.
* Excel Export: Download the list of students in Excel format.


### Error Handling

The application includes basic error handling to ensure smooth operation. If any errors occur (e.g., database issues or invalid input), they will be displayed to the user in a user-friendly format.

---

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.

## Acknowledgments

- Special thanks to the contributors of the dataset and the libraries used in this project.

## Stay Connected:
 * [![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff)](https://www.github.com/palakgandhi98)
 * [![LinkedIn](https://img.shields.io/badge/Linkedin-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/palakgandhi98)

Let's build something amazing together!


## License
This project is licensed under the MIT License.