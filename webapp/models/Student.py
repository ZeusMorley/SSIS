from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_students():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        student.*, 
        course.courseName, 
        course.courseCode, 
        college.collegeName, 
        college.collegeCode
    FROM student
    JOIN course ON student.courseId = course.id
    JOIN college ON course.collegeId = college.id
    """
    cursor.execute(query)
    students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return students

def add_student(data):
    required_fields = ['studentId', 'firstName', 'lastName', 'gender', 'year', 'courseName']
    for field in required_fields:
        if field not in data or not data[field]:
            return {"success": False, "message": "All fields are  required.", "type": "warning"}

    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO student (studentId, firstName, lastName, gender, year, courseId)
            VALUES (%s, %s, %s, %s, %s, (SELECT id FROM course WHERE courseCode = %s))
        """, (data['studentId'], data['firstName'], data['lastName'], data['gender'], data['year'], data['courseName']))
        conn.commit()
        return {"success": True, "message": "Student added successfully!", "type": "success"}
    
    except mysql.connector.IntegrityError as e:
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return {"success": False, "message": "Student ID already exists.", "type": "default"}
        else:
            return {"success": False, "message": f"Integrity error: {str(e)}", "type": "error"}
        
    except Exception as e:
        return {"success": False, "message": str(e), "type": "error"}
    finally:
        cursor.close()
        conn.close()


