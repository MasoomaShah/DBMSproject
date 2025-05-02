from flask import Blueprint,render_template,request,flash,jsonify, url_for,redirect
from flask_login import login_required,current_user
from .models import Note
from . import db
import psycopg2
from config import config,fetch_data
import json
views=Blueprint('views',__name__)


@login_required # so cant go to the home page unless you log in 
@views.route('/')
def home():
    columns,rows=fetch_data()

 
    return render_template("home.html", data=rows, columns=columns)
@views.route('/delete-note',methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id ==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/delete-records', methods=['POST'])
    
def delete_records():
    selected_ids = request.form.getlist('delete_ids')  # Gets all selected checkboxes

    if not selected_ids:
        flash("No rows selected.", "error")
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

    return redirect(url_for('views.home'))

