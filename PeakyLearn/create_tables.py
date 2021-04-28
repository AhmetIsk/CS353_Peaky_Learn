import sqlite3
from sqlite3 import Error


def create_connection(db_file='db.sqlite3'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def exec_query(sql_query):
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


if __name__=='__main__':

    exec_query('CREATE TABLE user(\
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                username VARCHAR(50) UNIQUE NOT NULL,\
                password VARCHAR(50) NOT NULL,\
                registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                firstName VARCHAR(50) NOT NULL,\
                lastName VARCHAR(50) NOT NULL,\
                email VARCHAR(50) NOT NULL,\
                phone VARCHAR(50));')




    print(query)
    exec_query(query)