from configparser import ConfigParser
from flask import request, redirect, flash
import psycopg2
# Here in this file I tried to create GUI using tkinter
# The GUI created here contain different fields to insert record in the
import psycopg2
def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    
    return db
def fetch_data():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM pakistan_census_data")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return columns, rows
    except Exception as e:
        print("Database error:", e)
        return [], []

