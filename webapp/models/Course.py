from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_courses():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT course.*, college.collegeName FROM course JOIN college ON course.collegeId = college.id")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses
