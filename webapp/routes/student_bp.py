from flask import Blueprint, request, jsonify
from webapp.models.Student import add_student, delete_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/add-student', methods=['POST'])
def add_student_route():
    data = request.get_json()
    result = add_student(data)
    return jsonify(result)

@student_bp.route('/delete-student', methods=['DELETE'])
def delete_student_route():
    data = request.get_json()
    student_id = data.get('studentId')
    
    if student_id:
        result = delete_student(student_id)
        return jsonify({'success': True, 'message': result['message'], 'type': 'success'}), 200
    else:
        return jsonify({"success": False, "message": "Student ID is required", "type": "error"})