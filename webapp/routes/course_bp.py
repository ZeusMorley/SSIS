from flask import Blueprint, request, jsonify
from webapp.models.Course import add_course, delete_course, update_course

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/add-course', methods=['POST'])
def add_course_route():
    data = request.get_json()
    
    result = add_course(data)

    if result['success']:
        return jsonify({'success': True, 'message': result['message'], 'type': 'success'})
    else:
        return jsonify({'success': False, 'message': result['message'], 'type': 'warning'}), 400


@course_bp.route('/delete-course', methods=['DELETE'])
def delete_course_route():
    data = request.get_json()
    course_code = data.get('courseCode')

    result = delete_course(course_code)

    if result['success']:
        return jsonify({'success': True, 'message': result['message'], 'type': 'success'}), 200
    else:
        return jsonify({'success': False, 'message': result['message'], 'type': 'default'}), 500


@course_bp.route('/update-course', methods=['PUT'])
def update_course_route():
    data = request.get_json()
    result = update_course(data)

    if result['success']:
        return jsonify({'success': True, 'message': result['message'], 'type': 'success'})
    else:
        return jsonify({'success': False, 'message': result['message'], 'type': 'warning'}), 400
