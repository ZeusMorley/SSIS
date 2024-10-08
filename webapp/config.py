from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = getenv('MYSQL_DATABASE')

    CLOUD_NAME = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUD_API_KEY = getenv('CLOUDINARY_API_KEY')
    CLOUD_API_SECRET = getenv('CLOUDINARY_API_SECRET')
    CLOUD_FOLDER = getenv('CLOUDINARY_URL')