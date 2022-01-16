from re import A
from flask import Flask, flash, request, session, jsonify
from flask.templating import render_template
from werkzeug.utils import redirect
from functions.users import *
from functions.tasks import *

app = Flask(__name__)
app.secret_key = 'HELIKOPTER HELIKOPTER'


@app.route('/')
def home():
    try:
        if session['login']:
            login = True
        else:
            login = False
    except KeyError:
        session['login'] = False
        login = session['login']
    return render_template('index.html', login=login)


@app.route('/login')
def loginpage():
    if session['login']:
        return redirect('/dashboard')
    else:
        return render_template('loginpage.html')


@app.route('/login/submit', methods=['GET', 'POST'])
def submitlogin():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']
        check = check_for_user(email, password)     # function returns True if user and pass are correct, false if user and email don't match, returns an error otherwise
        if check:
            session['login'] = True
            flash('Succesfully Logged in!')
            return redirect('/')
        elif not check:
            session['login'] = False
            flash('false')
            return redirect('/login')
        else:
            flash(check)
    else:    
        return redirect('/login')


@app.route('/logout')
def logout():
    if session['login']:
        session['login'] = False
    flash('successfully logged out')    
    return redirect('/')


@app.route('/signup')
def signup():
    if session['login']:
        return redirect('/dashboard')
    else:
        return render_template('signup.html')


@app.route('/signup/submit', methods=['GET', 'POST'])
def registerUser():
    if request.method == 'POST':
        if session['login']:
            return redirect('/')
        else:
            data = request.form
            name = data['name']
            email = data['email']
            password = data['password']
            status = register(name, email, password)
        if status:
            flash('Registration Successful!')
            return redirect('/')
        else:
            flash('an error occured, please try again')
            return redirect('/signup')
    else:
        return redirect('/signup')


@app.route('/tasks')
def all_tasks():
    return str(get_all_tasks())


@app.route('/tasks/add')
def new_task():
    return render_template('add_task.html')


@app.route('/tasks/add/submit', methods = ['GET', 'POST'])
def new_task_submit():
    if request.method == 'POST':
        data = request.form
        flash(add_task(data.get('name'), data.get('description'), data.get('deadline'), int(data.get('points'))))
        return redirect('/tasks')
    else:
        return redirect('/tasks/add')


if __name__ == '__main__':
    app.run(debug=True)