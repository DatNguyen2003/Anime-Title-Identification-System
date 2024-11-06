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

def connect_init_database():
    initial_config = {
        'user': 'root',  
        'password': '2003',  
        'host': 'localhost'
    }

    conn = mysql.connector.connect(**initial_config)
    cursor = conn.cursor()

    run_sql('create_db.sql' ,conn, cursor)

    conn.database = 'anime_db'
    return conn, cursor

def close_databse(conn, cursor):
    conn.close()
    cursor.close()
    return

def pack_str(list):
  return ".".join(list)

def unpack_str(str):
  return str.split(".")

def fetch_animes():
    conn, cursor = connect_init_database()

    cursor.execute('''
    SELECT ID, Title, Recap, Noun, Verb, Adj
    FROM animes
    ''')
    data = cursor.fetchall()

    close_databse(conn, cursor)

    return data