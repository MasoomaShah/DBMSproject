from configparser import ConfigParser

import psycopg2
from flask import redirect, Blueprint,render_template,request,flash,jsonify, url_for,redirect
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

def Delete_rows():
    selected_ids = request.form.getlist('delete_ids')  # Gets all selected checkboxes

    if not selected_ids:
        flash("No rows selected.", category="error")
        return redirect(url_for('views.home'))
    
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for pk in selected_ids:
            cur.execute("DELETE FROM pakistan_census_data WHERE census_id= %s", (pk,))
        conn.commit()
        cur.close()
        conn.close()
        # flash instead for meaage box that was takinter
        flash("Deleted successfully",category="success")

    except Exception as e:
        flash(f"Error :{str(e)}",category="error")

def edit_record(tree, columns):
    selected_items = tree.selection()
    if len(selected_items) != 1:
        flash("Edit Record", "Select exactly one row to edit.")
        return

    selected_item = selected_items[0]
    row_values = tree.item(selected_item, 'values')

    edit_win = tk.Toplevel()
    edit_win.title("Edit Record")

    entries = []
    for idx, col in enumerate(columns):
        tk.Label(edit_win, text=col).grid(row=idx, column=0, sticky='w')
        entry = tk.Entry(edit_win)
        entry.insert(0, row_values[idx])
        entry.grid(row=idx, column=1)
        entries.append(entry)