import sqlite3
from datetime import datetime, timedelta
from sqlite3 import Error


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_number(conn, numero, alias):
    sql = ''' INSERT INTO numeros(id, alias)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (numero, alias))
    conn.commit()
    return cur.lastrowid


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


def unparse_date(date):    
    return date.isoformat(' ', timespec='milliseconds')


def get_all_numbers(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM numeros")

    rows = cur.fetchall()

    return rows


def get_number(conn, number):
    cur = conn.cursor()

    cur.execute("SELECT * FROM numeros WHERE id=?", (number, ))

    rows = cur.fetchall()

    return rows


def delete_number(conn, number):
    cur = conn.cursor()

    cur.execute("DELETE FROM numeros WHERE id=?", (number,))
    conn.commit()

def delete_all_numbers(conn):
    cur = conn.cursor()

    cur.execute("DELETE FROM numeros")
    conn.commit()
