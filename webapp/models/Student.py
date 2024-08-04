from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_students():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT student.*, course.courseName, college.collegeName
    FROM student
    JOIN course ON student.courseId = course.id
    JOIN college ON course.collegeId = college.id
    """
    cursor.execute(query)
    students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return students
