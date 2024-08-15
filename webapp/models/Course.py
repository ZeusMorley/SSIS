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
    required_fields = ['courseCode', 'courseName', 'collegeName']
    for field in required_fields:
        if field not in course_data or not course_data[field]:
            return {"success": False, "message": "All fields are required.", "type": "warning"}
        
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
            SELECT COUNT(*) FROM student WHERE courseId = (
                SELECT id FROM course WHERE courseCode = %s
            )
        """, (course_code,))
        student_count = cursor.fetchone()[0]

        if student_count > 0:
            return {'success': False, 'message': 'Cannot delete course. There are students enrolled in this course.'}

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


def update_course(course_data):
    required_fields = ['courseCode', 'courseName']
    for field in required_fields:
        if field not in course_data or not course_data[field]:
            return {"success": False, "message": "All fields are required.", "type": "warning"}

    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        if course_data['courseCode'] != course_data['currentCourseCode']:
            cursor.execute("""
                SELECT COUNT(*) FROM course WHERE courseCode = %s
            """, (course_data['courseCode'],))
            exists = cursor.fetchone()[0]

            if exists:
                return {'success': False, 'message': 'Course code already exists.', 'type': 'error'}

        cursor.execute("""
            SELECT collegeId FROM course WHERE courseCode = %s
        """, (course_data['currentCourseCode'],))
        result = cursor.fetchone()
        current_college_id = result[0] if result else None

        college_code = course_data.get('collegeName', '').strip()
        if not college_code:
            college_id = current_college_id
        else:
            cursor.execute("SELECT id FROM college WHERE collegeCode = %s", (college_code,))
            college_id_result = cursor.fetchone()
            college_id = college_id_result[0] if college_id_result else None

            if not college_id:
                return {'success': False, 'message': 'Invalid college code.', 'type': 'error'}

        cursor.execute("""
            UPDATE course
            SET courseCode = %s, courseName = %s, collegeId = %s
            WHERE courseCode = %s
        """, (course_data['courseCode'], course_data['courseName'], college_id, course_data['currentCourseCode']))

        conn.commit()
        return {'success': True, 'message': 'Course updated successfully', 'type': 'success'}
    
    except mysql.connector.Error as e:
        conn.rollback()
        return {'success': False, 'message': str(e), 'type': 'error'}
    
    finally:
        cursor.close()
        conn.close()




