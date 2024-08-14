from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector
import re
import cloudinary.uploader
import cloudinary.api

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



def update_student(student_data, file=None):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        if student_data['studentId'] != student_data['currentStudentId']:
            cursor.execute(""" 
                SELECT COUNT(*) FROM student where studentId = %s
            """, (student_data['studentId'],))
            exists = cursor.fetchone()[0]

            if exists:
                return {'success': False, 'message': 'Student ID already exists.', 'type': 'error'}

        new_cloudinary_url = None
        if file:
            try:
                cursor.execute("SELECT cloudinary_url FROM student WHERE studentId = %s", (student_data['currentStudentId'],))
                old_cloudinary_url = cursor.fetchone()[0]

                upload_result = cloudinary.uploader.upload(file, folder='student_photos')
                new_cloudinary_url = upload_result.get('secure_url')

                if old_cloudinary_url:
                    public_id = old_cloudinary_url.split('/')[-1].split('.')[0]
                    cloudinary.uploader.destroy(public_id)
                
            except Exception as e:
                return {'success': False, 'message': f"Photo upload failed: {str(e)}", 'type': 'error'}

        update_query = """
            UPDATE student
            SET studentId = %s, firstName = %s, lastName = %s, gender = %s, year = %s, courseId = (
                SELECT id FROM course WHERE courseCode = %s
            )
        """
        
        update_params = [student_data['studentId'], student_data['firstName'], student_data['lastName'], student_data['gender'], student_data['year'], student_data['courseName']]

        if new_cloudinary_url:
            update_query += ", cloudinary_url = %s"
            update_params.append(new_cloudinary_url)

        update_query += " WHERE studentId = %s"
        update_params.append(student_data['currentStudentId'])

        cursor.execute(update_query, update_params)
        conn.commit()

        return {'success': True, 'message': 'Student updated successfully', 'type': 'success'}
    
    except mysql.connector.Error as e:
        conn.rollback()
        return {'success': False, 'message': str(e), 'type': 'error'}
    finally:
        cursor.close()
        conn.close()
        
