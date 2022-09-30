import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"novelas.db"

    sql_create_novels_table = """ CREATE TABLE IF NOT EXISTS novels (
                                        id integer PRIMARY KEY,
                                        url text,
                                        title text,
                                        author text,
                                        genres text,
                                        synopsis text,
                                        chapters text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_novels_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()