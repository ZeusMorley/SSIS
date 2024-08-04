from flask import Blueprint, render_template, current_app, request, jsonify
from webapp.db import get_mysql_connection
from webapp.models.Student import get_all_students
from webapp.models.Course import get_all_courses
from webapp.models.College import get_all_colleges

base_bp = Blueprint('base', __name__)

@base_bp.route('/')
def base_page():
    students = get_all_students()
    courses = get_all_courses()
    colleges = get_all_colleges()
    return render_template("base.html", students=students, courses=courses, colleges=colleges)

