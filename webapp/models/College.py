from flask import current_app
from webapp.db import get_mysql_connection
import mysql.connector

def get_all_colleges():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM college")
    colleges = cursor.fetchall()
    cursor.close()
    conn.close()
    return colleges
