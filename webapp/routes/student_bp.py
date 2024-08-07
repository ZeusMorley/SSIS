from flask import Blueprint, request, jsonify
from webapp.models.Student import add_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/add-student', methods=['POST'])
def add_student_route():
    data = request.get_json()
    result = add_student(data)
    return jsonify(result)
