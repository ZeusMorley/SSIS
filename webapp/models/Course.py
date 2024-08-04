from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_courses():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            course.id, 
            course.courseCode, 
            course.courseName, 
            college.collegeName, 
            college.collegeCode,
            COUNT(student.id) AS studentCount
        FROM course
        LEFT JOIN college ON course.collegeId = college.id
        LEFT JOIN student ON course.id = student.courseId
        GROUP BY course.id
    """)
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses
