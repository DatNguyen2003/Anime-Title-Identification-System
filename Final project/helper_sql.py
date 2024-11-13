import mysql.connector
import os

# def run_sql(sql_file_name, conn, cursor):

#     sql_file_path = os.path.join('Final project//SQL_file', sql_file_name)

#     with open(sql_file_path, 'r') as sql_file:
#         sql_script = sql_file.read()

#     for statement in sql_script.split(';'):
#         if statement.strip():
#             cursor.execute(statement)
    
#     conn.commit()

def run_sql(sql_file_name, conn, cursor):
    # Use os.path.join to construct the file path in a platform-independent way
    base_dir = os.path.dirname(__file__)  # Get the current script directory
    sql_file_path = os.path.join(base_dir, 'SQL_file', sql_file_name)

    try:
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()

        # Execute each statement separately
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print(f"Executed SQL script from {sql_file_name} successfully.")
    except FileNotFoundError:
        print(f"SQL file not found: {sql_file_path}")
    except Exception as e:
        print(f"An error occurred while executing the SQL script: {e}")

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

def connect_database():
    db_config = {
        'user': 'root',          # Database username
        'password': '2003',      # Database password
        'host': 'localhost',     # Database host
        'database': 'anime_db'   # Name of the database to connect to
    }

    # Establish a connection to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_config)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

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