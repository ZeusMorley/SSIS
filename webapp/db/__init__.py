from flask import current_app
import mysql.connector

def get_mysql_connection():
    connection = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )
    return connection

from .create_tables import create_tables
