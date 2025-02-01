import sqlite3

def connect_db(my_db_name):
    my_conn = sqlite3.connect(my_db_name) # creates a connector
    my_conn.row_factory = sqlite3.Row # allow me to use column name
    my_cursor = my_conn.cursor()  # creates a cursor
    return my_conn, my_cursor

def read_query(my_cursor, query, type):
    my_cursor.execute(query)
    rows = my_cursor.fetchall()
    if type == list:
        result_list = [list(row) for row in rows]
        return result_list
    if type == dict:
        result_dict = [dict(row) for row in rows]
        return result_dict
    if type == tuple:
        result_tuple = [tuple(row) for row in rows]
        return result_tuple

def update_query(my_cursor, my_conn, query, param):
    my_cursor.execute(query, param)
    my_conn.commit()

def action_query (my_curser, my_conn, query):
    my_curser.execute (query)
    my_conn.commit()
