from flask import Blueprint,render_template,request,flash,jsonify, url_for,redirect
from flask_login import login_required,current_user
from .models import Note
from . import db
import psycopg2
from config import fetch_data
import json
import datetime as datetime
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

# def delete_records():
#       # Gets all selected checkboxes
#     Delete_rows()


#     return redirect(url_for('views.home'))

@views.route('/handle_records', methods=['POST'])
def handle_records():
    print("HANDLE_RECORDS CALLED")

    flash(f"TEST: {datetime.now()}")
    return render_template('login.html')
    # if not selected_ids:
    #     flash('Please select at least one record.')
    #     return redirect(url_for('views.home'))

                # if action == 'delete':
                #     Delete_rows(selected_ids)


                # elif action == 'edit':
                #     flash("please work")

         
        # return redirect(url_for('views.test_flash'))
        # if len(selected_ids) != 1:
        #     flash('Please select exactly one record to edit.')
        #     return redirect(url_for('views.home'))
        # record_id = selected_ids[0]
        # return redirect(url_for('views.Edit_record'))

    # else:
    #     flash('Unknown action.')
    #     return redirect(url_for('views.home'))

@views.route('/Edit_record', methods=['GET', 'POST'])
def Edit_record():
    flash("you just clicked the edit button whaaaaaaaa")
    return render_template('login.html')
