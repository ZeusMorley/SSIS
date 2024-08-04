from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_colleges():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            college.id, 
            college.collegeCode, 
            college.collegeName, 
            COUNT(course.id) AS courseCount
        FROM college
        LEFT JOIN course ON college.id = course.collegeId
        GROUP BY college.id
    """)
    colleges = cursor.fetchall()
    cursor.close()
    conn.close()
    return colleges
