import mysql.connector

def connect_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="aTest",
        password="ashwin2801",
        buffered=True
    )

def get_number_of_cameras(cursor, branch_id):
    query = "SELECT camera_id FROM branch WHERE branch_id=%s"
    cursor.execute(query, [branch_id])
    return [result[0] for result in cursor.fetchall()]

def get_branch_count(cursor):
    query = "SELECT branch_id FROM branch"
    cursor.execute(query)
    return cursor.fetchall()

def get_branch_name(cursor, branch_id):
    query = "SELECT branch_details FROM branch WHERE branch_id=%s"
    cursor.execute(query, [branch_id])
    return cursor.fetchone()[0]
