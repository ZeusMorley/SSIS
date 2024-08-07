from flask import Flask
from .db import create_tables, get_mysql_connection
from webapp.config import Config
from dotenv import load_dotenv
import cloudinary
from cloudinary import config as cloudinary_config

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config.from_object(Config)

    cloudinary.config(
        cloud_name=app.config['CLOUD_NAME'],
        api_key=app.config['CLOUD_API_KEY'],
        api_secret=app.config['CLOUD_API_SECRET'],
        folder_name=app.config['CLOUD_FOLDER']
    )

    create_tables(app)

    from .routes.base_bp import base_bp
    from .routes.college_bp import college_bp
    from .routes.course_bp import course_bp
    # from .routes.student_bp import student

    app.register_blueprint(base_bp, url_prefix='/')
    app.register_blueprint(college_bp, url_prefix='/college')
    app.register_blueprint(course_bp, url_prefix='/course')
    # app.register_blueprint(student, url_prefix='/student')

    return app
