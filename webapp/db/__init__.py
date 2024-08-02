from flask import current_app
import mysql.connector

def get_mysql_connection(config):
    connection = mysql.connector.connect(
        host=config['MYSQL_HOST'],
        user=config['MYSQL_USER'],
        password=config['MYSQL_PASSWORD'],
        database=config['MYSQL_DATABASE']
    )
    return connection

# Import create_tables function from the same module
from .create_tables import create_tables
