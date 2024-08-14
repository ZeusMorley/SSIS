from flask import Blueprint, request, jsonify
from webapp.models.Student import add_student, delete_student, update_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/add-student', methods=['POST'])
def add_student_route():
    data = request.form.to_dict()
    file = request.files.get('studentPhoto')
    result = add_student(data, file)
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
    
@student_bp.route('/update-student', methods=['PUT'])
def update_student_route():
    data = request.form.to_dict()
    file = request.files.get('studentPhoto')
    result = update_student(data, file)
    
    return jsonify(result)