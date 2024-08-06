from flask import Blueprint, request, jsonify
from webapp.models.College import add_college, delete_college, check_if_has_courses

college_bp = Blueprint('college_bp', __name__)

@college_bp.route('/add-college', methods=['POST'])
def add_college_route():
    data = request.get_json()
    college_code = data.get('collegeCode')
    college_name = data.get('collegeName')

    if not college_code or not college_name:
        return jsonify({'success': False, 'message': 'All fields must be filled.', 'type': 'warning'}), 400

    success = add_college(college_code, college_name)

    if success:
        return jsonify({'success': True, 'message': 'College added successfully', 'type': 'success'})
    else:
        return jsonify({'success': False, 'message': 'College code already exists.', 'type': 'default'}), 400
    


@college_bp.route('/delete-college', methods=['DELETE'])
def delete_college_route():
    data = request.get_json()
    college_code = data.get('collegeCode')

    if check_if_has_courses(college_code):
        return jsonify({'success': False, 'message': 'You can only delete empty Colleges.', 'type': 'default'}), 400

    success = delete_college(college_code)

    if success:
        return jsonify({'success': True, 'message': 'College deleted successfully', 'type': 'success'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete college', 'type': 'default'}), 500


