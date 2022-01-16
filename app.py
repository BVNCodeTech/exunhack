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
            session['email'] = email
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


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/tasks')
def all_tasks():
    if session['login']:
        tasks = dict(get_all_tasks(session['email']))
        tasklist = []
        return tasklist.append(tasks[task]["description"] for task in tasks)
    else:
        flash('you deadass have not signed in you disgusting oompa loompa')
        return redirect('/login')

@app.route('/tasks/<id>')
def get_one_task(id):
    object_id = get_all_tasks(session['email'])[int(id)]['_id']
    return str(get_task(object_id))


@app.route('/tasks/add')
def new_task():
    return render_template('add_task.html', edit = False)


@app.route('/tasks/add/submit', methods = ['GET', 'POST'])
def new_task_submit():
    if request.method == 'POST':
        data = request.form
        flash(add_task(data.get('email'), data.get('name'), data.get('description'), data.get('deadline'), int(data.get('points'))))
        return redirect('/tasks')
    else:
        return redirect('/tasks/add')


@app.route('/tasks/remove/<id>', methods=['GET','POST'])
def del_task(id):
    object_id = get_all_tasks()[int(id)]['_id']
    flash(remove_task(object_id))
    return redirect('/tasks')


@app.route('/tasks/edit/<id>')
def edit_exis_task(id):
    task = get_all_tasks()[int(id)]
    return render_template('add_task.html', edit=True, data=task, id=str(id))


@app.route('/tasks/edit/<id>/submit', methods=['GET','POST'])
def edit_task_submit(id):
    if request.method == 'POST':
        data = request.form
        object_id = get_all_tasks()[int(id)]['_id']
        flash(edit_task(object_id, data.get('name'), data.get('description'), data.get('deadline'), int(data.get('points'))))
        return redirect('/tasks')
    else:
        return redirect('/tasks/edit/<id>')

if __name__ == '__main__':
    app.run(debug=True)