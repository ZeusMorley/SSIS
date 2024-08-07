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

def add_college(college_code, college_name):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = "INSERT INTO college (collegeCode, collegeName) VALUES (%s, %s)"
        cursor.execute(query, (college_code, college_name))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_if_has_courses(college_code):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM course WHERE collegeId = (SELECT id FROM college WHERE collegeCode = %s)"
        cursor.execute(query, (college_code,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0] > 0
    except Exception as e:
        print(f"Error: {e}")
        return False



def delete_college(college_code):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "DELETE FROM college WHERE collegeCode = %s"
        cursor.execute(query, (college_code,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_college_code_exists(college_code):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM college WHERE collegeCode = %s"
        cursor.execute(query, (college_code,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        
        return count > 0
    except Exception as e:
        print(f"Error: {e}")
        return False


def update_college(current_college_code, new_college_code, new_college_name):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "UPDATE college SET collegeCode = %s, collegeName = %s WHERE collegeCode = %s"
        cursor.execute(query, (new_college_code, new_college_name, current_college_code))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
