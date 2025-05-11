from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

from .import db

# you cannot now backtrack to the original password like encryption
auth=Blueprint('auth',__name__)

from .models import User
from flask_login import login_user
from .firebase import db  # use your initialized Firestore client

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if user exists in Firestore
        existing = db.collection('Users').where('email', '==', email).limit(1).stream()

        if any(existing):
            flash('Email already exists', category='error')
            return render_template("sign_up.html")

        if len(email) < 4:
            flash('Email must be greater than three characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than one character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than seven characters', category='error')
        else:
            user_data = {
                'email': email,
                'password': password1,  # plain text for now
                'name': first_name
            }
            new_doc = db.collection('Users').add(user_data)
            new_user = User(id=new_doc[1].id, email=email, first_name=first_name)
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_docs = db.collection('Users').where('email', '==', email).limit(1).stream()
        for doc in user_docs:
            data = doc.to_dict()
            if data['password'] == password:
                user = User(id=doc.id, email=data['email'], first_name=data['name'])
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
                return render_template("login.html", user=current_user)

        flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)
