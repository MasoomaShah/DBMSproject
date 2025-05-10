from flask import Blueprint,render_template,request,flash,jsonify, url_for,redirect
from flask_login import login_required,current_user
from .models import Note
from . import db
import psycopg2
from config import config,fetch_data,Delete_rows
import json
views=Blueprint('views',__name__)

@views.route('/')
@login_required # so cant go to the home page unless you log in 

def home():

    columns,rows=fetch_data()

 
    return render_template("home.html",columns=columns,rows=rows)


# @views.route('/delete-records', methods=['POST'])
    
# def delete_records():
#     delete_rows()

#     return redirect(url_for('views.home'))
# def delete_rows():
#     Delete_rows()
#     return redirect(url_for('views.home') )

def delete_records(selected_ids):
      # Gets all selected checkboxes
    Delete_rows(selected_ids)


    # return redirect(url_for('views.home'))

@views.route('/handle_records', methods=['POST'])
def handle_records():
    action = request.form.get('action')
    selected_ids = request.form.getlist('selected_ids') 
    if not selected_ids:
        flash('Please select at least one record.',category='error')
        return redirect(url_for('views.home'))

    if action == 'delete':
        delete_records(selected_ids)

        return redirect (url_for('views.home'))
    elif action == 'edit':

      if len(selected_ids) != 1:

          flash('Please select exactly one record to edit.')
          return redirect(url_for('views.home'))
      record_id = selected_ids[0]
    
      return redirect(url_for('views.edit_record', census_id=record_id))

        # if len(selected_ids) != 1:
        #     flash('Please select exactly one record to edit.')
        #     return redirect(url_for('views.home'))
        # record_id = selected_ids[0]
        # return redirect(url_for('views.Edit_record'))

    else:
        flash('Unknown action.')
        return redirect(url_for('views.home'))



@views.route('/edit_record', methods=['GET', 'POST'])
def edit_record():
    census_id = request.args.get('census_id')
    params = config()
    conn = psycopg2.connect(**params) 
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.form.to_dict()
        values = [data[key] for key in list(data) if key != 'census_id']
        values.append(data['census_id'])

        cur.execute("CALL insert_edited_record(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)


        conn.commit()
        flash("Record updated.")
        return redirect(url_for('views.home'))

    cur.execute("SELECT * FROM pakistan_census_data WHERE census_id = %s", (census_id,))
    row = cur.fetchone()
    colnames = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()
    return render_template('edit.html',row=row, colnames=colnames,zip=zip)
@views.route('/insert_record', methods=['GET', 'POST'])
def insert_record():
    # this part for inserting data when form is submitted via post
    if request.method=='POST':
        data=request.form.to_dict() 
        data.pop("census_id", None)  # Remove census_id if present
        for key, value in data.items():
          if value.strip() == "":
            flash(f"The field '{key}' cannot be empty.", "error")
            return redirect(url_for("views.insert_record"))
#form fields to python dictionary 
        values = [data[key] for key in data]
        # creates a list of vlaues 
        #form the data dictiomary in the same order as the keys 
        # so only values and not column values that were in the dictionary 
        
        params = config()
        conn = psycopg2.connect(**params) 
        cur = conn.cursor()
        # %s converts is used as a placeholder
        cur.execute("select inserting_values_actual(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",values)
        conn.commit()
        cur.close()
        conn.close()
        flash("Record inserted successfully")
        return redirect(url_for('views.home'))
    #this part for retrieving column names to render the form via get 
    params=config()
    conn=psycopg2.connect(**params)
    cur=conn.cursor()
    cur.execute("SELECT * from pakistan_census_data limit 1;")
    colnames=[desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    colnames_no_id = [col for col in colnames if col != 'census_id']
    empty_row = ['' for _ in colnames_no_id]

    return render_template(
        'edit.html',
        row=empty_row,
        colnames=colnames_no_id,
        zip=zip,
        insert_mode=True
    )
@views.route("/backup")
def backup_page():
    params =config()
    conn=psycopg2.connect(**params)
    cur=conn.cursor()

    cur.execute("select * from pakistani_census_data_backup order by deleted_at desc")
    rows =cur.fetchall()
    colnames=[desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return render_template("backup.html",rows=rows,colnames=colnames)

@views.route("/restore_record", methods=["POST"])
def restore_record():
    census_id = request.form.get("census_id")

    if not census_id:
        flash("Invalid restore request.", "error")
        return redirect(url_for("views.backup_page"))

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    try:

        # Fetch from backup
      cur.execute("SELECT * FROM pakistani_census_data_backup WHERE census_id = %s", (census_id,))
      record = cur.fetchone()

      if not record:
          flash("Backup record not found.", "error")
          return redirect(url_for("views.backup_page"))

      # Get all columns
      colnames = [desc[0] for desc in cur.description]
      record_dict = dict(zip(colnames, record))

      # Remove deleted_at
      record_dict.pop("deleted_at", None)

      # Prepare insert
      columns = list(record_dict.keys())
      values = list(record_dict.values())

      insert_query = f"""
      INSERT INTO pakistan_census_data ({', '.join(columns)})
      VALUES ({', '.join(['%s'] * len(values))})
      """
      cur.execute(insert_query, values)


        # Optionally delete from backup
      cur.execute("DELETE FROM pakistani_census_data_backup WHERE census_id = %s", (census_id,))

      conn.commit()
      flash("Record restored successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash("Error restoring record: " + str(e), "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("views.backup_page"))
