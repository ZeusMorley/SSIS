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



def add_course(course_data):
    """Add a new course to the database."""
    conn = get_mysql_connection()
    cursor = conn.cursor()

    if len(course_data['courseCode']) > 8:
        return {'success': False, 'message': 'Course code too long. Must be up to 8 characters.'}
    
    try:
        cursor.execute("""
            INSERT INTO course (courseCode, courseName, collegeId)
            VALUES (%s, %s, (
                SELECT id FROM college WHERE collegeCode = %s
            ))
        """, (course_data['courseCode'], course_data['courseName'], course_data['collegeName']))

        conn.commit()
        return {'success': True, 'message': 'Course added successfully'}
    
    except mysql.connector.IntegrityError as e:
        conn.rollback()
        return {'success': False, 'message': 'Course code already exists.'}
    
    except Exception as e:
        conn.rollback()
        return {'success': False, 'message': str(e)}
    
    finally:
        cursor.close()
        conn.close()


def delete_course(course_code):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM course
            WHERE courseCode = %s
        """, (course_code,))
        
        conn.commit()
        return {'success': True, 'message': 'Course deleted successfully.'}
    
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return {'success': False, 'message': 'Failed to delete course.'}
    
    finally:
        cursor.close()
        conn.close()

