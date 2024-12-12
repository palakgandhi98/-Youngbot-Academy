import streamlit as st
from database import setup_database, insert_student, get_all_students, update_student, delete_student
import pandas as pd
from io import BytesIO

# Ensure the database and table are set up
setup_database()



# Streamlit User Interface
st.set_page_config(page_title="Student Database Management System", layout="wide", page_icon="🎓")

# The rest of your Streamlit code...
st.title("🎓 Student Database Management System")

menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Student":
    st.subheader("Add New Student")
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        grade = st.text_input("Grade")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            try:
                insert_student(name, age, grade)
                st.success(f"Student '{name}' added successfully!")
            except Exception as e:
                st.error(f"Error adding student: {e}")

elif choice == "View Students":
    st.subheader("All Students")
    try:
        df = get_all_students()
        
        if not df.empty:
            st.dataframe(df)

            # Add download buttons for CSV and Excel
            csv_data = df.to_csv(index=False).encode("utf-8")

            # Generate Excel file in memory using BytesIO
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Students")
            excel_data = excel_buffer.getvalue()

            # Create two columns to place the download buttons side by side
            col1, col2, col3, col4, col5  = st.columns(5)
            # Download buttons
            with col1:
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name="students.csv",
                    mime="text/csv",
                )
            with col2:
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name="students.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        else:
            st.info("No records found!")
    except Exception as e:
        st.error(f"Error retrieving students: {e}")

elif choice == "Update Student":
    st.subheader("Update Student Details")
    try:
        df = get_all_students()
        if not df.empty:
            st.dataframe(df)

            # Create a dropdown for selecting a student
            student_names = df["name"].tolist()
            selected_student = st.selectbox("Select Student to Update", student_names)

            if selected_student:
                selected_row = df[df["name"] == selected_student].iloc[0]
                student_id = selected_row["id"]

                # Pre-fill existing data
                name = st.text_input("Name", selected_row["name"])
                age = st.number_input(
                    "Age", min_value=1, max_value=100, step=1, value=selected_row["age"]
                )
                grade = st.text_input("Grade", selected_row["grade"])

                if st.button("Update Student"):
                    try:
                        update_student(student_id, name, age, grade)
                        st.success(f"Student '{name}' updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating student: {e}")
        else:
            st.info("No records found!")
    except Exception as e:
        st.error(f"Error retrieving students for update: {e}")

elif choice == "Delete Student":
    st.subheader("Delete Student Record")
    try:
        df = get_all_students()
        if not df.empty:
            st.dataframe(df)

            # Create a dropdown for selecting a student
            student_names = df["name"].tolist()
            selected_student = st.selectbox("Select Student to Delete", student_names)

            if selected_student:
                selected_row = df[df["name"] == selected_student].iloc[0]
                student_id = selected_row["id"]

                if st.button("Delete Student"):
                    try:
                        delete_student(student_id)
                        st.success(f"Student '{selected_student}' deleted successfully!")
                    except Exception as e:
                        st.error(f"Error deleting student: {e}")
        else:
            st.info("No records found!")
    except Exception as e:
        st.error(f"Error retrieving students for deletion: {e}")
