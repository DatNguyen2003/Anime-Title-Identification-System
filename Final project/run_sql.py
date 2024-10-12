import mysql.connector
import os

def run_sql(sql_file_name, conn, cursor):

    sql_file_path = os.path.join('Final project//SQL_file', sql_file_name)

    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    for statement in sql_script.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    conn.commit()