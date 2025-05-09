from flask import Blueprint,render_template,request,flash,jsonify, url_for,redirect
from flask_login import login_required,current_user
from .models import Note
from . import db
import psycopg2
from config import fetch_data,Delete_rows
import json
views=Blueprint('views',__name__)

@views.route('/')
@login_required # so cant go to the home page unless you log in 

def home():

    columns,rows=fetch_data()

 
    return render_template("home.html",columns=columns,rows=rows)


@views.route('/delete-records', methods=['POST'])
    
# def delete_records():
#     delete_rows()

#     return redirect(url_for('views.home'))
# def delete_rows():
#     Delete_rows()
#     return redirect(url_for('views.home') )

def delete_records():
      # Gets all selected checkboxes
    Delete_rows()


    return redirect(url_for('views.home'))


