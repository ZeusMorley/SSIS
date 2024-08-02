import os
import mysql.connector

script_path = os.path.join(os.path.dirname(__file__), 'create_tables_script.sql')

def create_tables(app):
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )
    cursor = connection.cursor()
    with open(script_path, 'r') as f:
        sql = f.read()
    
    sql_commands = sql.split(';')
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()
