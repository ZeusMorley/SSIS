from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector
import re
import cloudinary.uploader

def validate_student_id(student_id):
    pattern = r'^\d{4}-\d{4}$' 
    if re.match(pattern, student_id):
        return True
    return False


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



def add_student(data, file=None):
    required_fields = ['studentId', 'firstName', 'lastName', 'gender', 'year', 'courseName']
    for field in required_fields:
        if field not in data or not data[field]:
            return {"success": False, "message": "All fields are required.", "type": "warning"}
    
    if not validate_student_id(data['studentId']):
        return {"success": False, "message": "Student ID must be in the format YYYY-NNNN.", "type": "warning"}

    cloudinary_url = None
    if file:
        try:
            upload_result = cloudinary.uploader.upload(file, folder='student_photos')
            cloudinary_url = upload_result.get('secure_url')
        except Exception as e:
            return {"success": False, "message": f"Photo upload failed: {str(e)}", "type": "error"}

    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO student (studentId, firstName, lastName, gender, year, courseId, cloudinary_url)
            VALUES (%s, %s, %s, %s, %s, (SELECT id FROM course WHERE courseCode = %s), %s)
        """, (data['studentId'], data['firstName'], data['lastName'], data['gender'], data['year'], data['courseName'], cloudinary_url))
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



def delete_student(student_id):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM student WHERE studentId = %s", (student_id,))
        conn.commit()

        return {"success": True, "message": "Student deleted successfully.", "type": "success"}
        
    except mysql.connector.Error as e:
        return {"success": False, "message": str(e), "type": "error"}
    finally:
        cursor.close()
        conn.close()



def update_student(student_data):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        if student_data['studentId'] != student_data['currentStudentId']:
            cursor.execute(""" 
                SELECT COUNT(*) FROM student where studentId = %s
            """, (student_data['studentId'],))
            exists = cursor.fetchone()[0]

            if exists:
                return {'success': False, 'message': 'Student ID already exists.'}

        cursor.execute("""  
            UPDATE student
            SET studentId = %s, firstName = %s, lastName = %s, gender = %s, year =  %s, courseId = (
                SELECT id FROM course where courseCode = %s
            )
            WHERE studentId = %s
        """, (student_data['studentId'], student_data['firstName'], student_data['lastName'], student_data['gender'], student_data['year'], student_data['courseName'], student_data['currentStudentId']))                

        conn.commit()
        return {'success': True, 'message': 'Student updated successfully'}
    
    except mysql.connector.Error as e:
        conn.rollback()
        return {'success': False, 'message': str(e)}
    finally:
        cursor.close()
        conn.close

    # if not validate_student_id(student_id):
    #     return {"success": False, "message": "Invalid student ID format.", "type": "warning"}
    
    # query_parts = []
    # params = []
    
    # if 'firstName' in data:
    #     query_parts.append("firstName = %s")
    #     params.append(data['firstName'])
    
    # if 'lastName' in data:
    #     query_parts.append("lastName = %s")
    #     params.append(data['lastName'])
    
    # if 'gender' in data:
    #     query_parts.append("gender = %s")
    #     params.append(data['gender'])
    
    # if 'year' in data:
    #     query_parts.append("year = %s")
    #     params.append(data['year'])
    
    # if 'courseCode' in data:
    #     query_parts.append("courseId = (SELECT id FROM course WHERE courseCode = %s)")
    #     params.append(data['courseCode'])
    
    # if not query_parts:
    #     return {"success": False, "message": "No valid fields provided for update.", "type": "error"}
    
    # query = "UPDATE student SET " + ", ".join(query_parts) + " WHERE studentId = %s"
    # params.append(student_id)
    
    # try:
    #     cursor.execute(query, tuple(params))
    #     conn.commit()
        
    #     if cursor.rowcount == 0:
    #         return {"success": False, "message": "Student ID not found.", "type": "warning"}
        
    #     return {"success": True, "message": "Student updated successfully!", "type": "success"}
    
    # except mysql.connector.Error as e:
    #     return {"success": False, "message": str(e), "type": "error"}
    
    # finally:
    #     cursor.close()
    #     conn.close()