from flask import Blueprint, request, jsonify
from webapp.models.Course import add_course 

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/add-course', methods=['POST'])
def add_course_route():
    data = request.get_json()
    
    result = add_course(data)

    if result['success']:
        return jsonify({'success': True, 'message': result['message'], 'type': 'success'})
    else:
        return jsonify({'success': False, 'message': result['message'], 'type': 'warning'}), 400
