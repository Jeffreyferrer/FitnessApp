from flask_app import app
from flask import render_template, redirect, flash, session, request 
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash


@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods = ['POST'])
def register_user():
    print("working")
    if not User.validate_register(request.form):
        print("still working")
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    user_id = User.create_user(data) 
    print("still working?")
    session['user_id'] = user_id # return that id number
    return redirect('/dashboard')

# Login
@app.route('/login', methods = ["POST"])
def login():
    
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    
    user = User.get_email(data)
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash('must be logged in')
        return redirect('/') 

    data = {
        'id': session['user_id']
    }

    user= User.get_id(data) 
    all_workouts=Workout.read_all()
    return render_template('dashboard.html', user=user, all_workouts= all_workouts)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/') 

@app.route('/lowerbody')
def lowerbody():

    data = {
        'id': session['user_id']
    }

    user= User.get_id(data) 

    return render_template('lower.html', user=user)

@app.route('/upperbody')
def upperbody():

    data = {
        'id': session['user_id']
    }

    user= User.get_id(data) 

    return render_template('upper.html', user=user)

@app.route('/chest')
def chest():

    data = {
        'id': session['user_id']
    }

    user= User.get_id(data) 

    return render_template('chest.html', user=user, all_workouts=Workout.read_all())

# @app.route('/leg')
# def leg():

#     data = {
#         'id': session['user_id']
#     }

#     user= User.get_id(data) 

#     return render_template('leg.html', user=user, all_workouts=Workout.read_all())