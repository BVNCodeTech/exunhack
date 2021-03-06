from re import A
from flask import Flask, flash, request, session, jsonify
from flask.templating import render_template
from werkzeug.utils import redirect
from functions.users import *
from functions.tasks import *
from functions.rewards import *
from functions.feedback import *
from functions.training import *

app = Flask(__name__)
app.secret_key = 'bablucopter'


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
    return redirect('/dashboard')


@app.route('/login')
def loginpage():
    try:
        if session['login'] and session['user']:
            return redirect('/dashboard')
        else:
            return render_template('loginpage.html')
    except KeyError:
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
            session['user'] = email
            flash('Succesfully Logged in!')
            return redirect('/dashboard')
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
        session['user'] = None
    flash('successfully logged out')    
    return redirect('/login')


@app.route('/add-user')
def signup():
    if check_admin(session['user']):
        return render_template('signup.html')
    else:
        return render_template('unauthorized.html')


@app.route('/signup/submit', methods=['GET', 'POST'])
def registerUser():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        password = data['password']
        status = register(name, email, password)
        if status:
            flash('Registration Successful!')
            return redirect('/add-user')
        else:
            flash('an error occured, please try again')
            return redirect('/add-user')
    else:
        return redirect('/add-user')

    
@app.route('/dashboard')
def dashboard():
    try:
        if session['login'] and session['user']:
            three_tasks = get_user_tasks(session['user'])[:3]
            user = get_user_by_id(session['user'])
            points = user['points']
            level = user['level']
            return render_template('dashboard.html', name=get_user_by_id(session['user'])['name'], admin=check_admin(session['user']), tasks=three_tasks, points=points, level=level)
        else:
            return redirect('/login')
    except KeyError:
        return redirect('/login')

@app.route('/tasks')
def all_tasks():
    try:
        if session['login'] and session['user']:
            if check_admin(session['user']):
                tasks = []
                for task in dict(get_all_tasks()).values():
                    task['unassigned_users'] = get_users_without_this_task(task['unique_id'])
                    tasks.append(task)
                return render_template('tasks.html', name = get_user_by_id(session['user'])['name'], tasks = tasks, admin=True)
            else:
                tasks = get_user_tasks(session['user'])
                return render_template('tasks.html', name = get_user_by_id(session['user'])['name'], tasks = tasks, admin=False)

        else:
            return redirect('/login')
    except KeyError:
        return redirect('/login')


@app.route('/tasks/<id>')
def get_one_task(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            object_id = get_all_tasks()[int(id)]['_id']
            return str(get_task(object_id))
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/add')
def new_task():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            return render_template('add_task.html', edit = False, admin=check_admin(session['user']))
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/add/submit', methods = ['GET', 'POST'])
def new_task_submit():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            if request.method == 'POST':
                data = request.form
                flash(add_task(data.get('name'), data.get('description'), data.get('deadline'), int(data.get('points'))))
                return redirect('/tasks')
            else:
                return redirect('/tasks/add')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/complete/<id>', methods=["GET", "POST"])
def completetask(id):
    if session['user'] and session['login']:
        if request.method == "POST":
            flash(mark_task_as_complete(session['user'], int(id)))
            return redirect('/tasks')
        else:
            return redirect('/tasks')
    else:
        return redirect('/login')
        
        
@app.route('/tasks/remove/<id>', methods=['GET','POST'])
def del_task(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            flash(remove_task(id))
            return redirect('/tasks')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/edit/<id>')
def edit_exis_task(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            task = get_all_tasks()[int(id)]
            return render_template('add_task.html', edit=True, data=task, id=str(id), admin=check_admin(session['user']))
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/edit/<id>/submit', methods=['GET','POST'])
def edit_task_submit(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            if request.method == 'POST':
                data = request.form
                object_id = get_all_tasks()[int(id)]['_id']
                flash(edit_task(object_id, data.get('name'), data.get('description'), data.get('deadline'), int(data.get('points'))))
                return redirect('/tasks')
            else:
                return redirect('/tasks/edit/<id>')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')


@app.route('/tasks/assign/<id>', methods=['GET','POST'])
def assign_task(id):
    if session['login'] and session['user']:
        if request.method == 'POST':
            data = request.form
            name = data.get('users')
            if not name:
                return redirect('/tasks')
            user = get_user_by_name(name)
            flash(assign_user_tasks(id, user['_id']))
            return redirect('/tasks')
        else:
            return redirect('/tasks')
    else:
        return redirect('/login')


@app.route('/workers')
def all_oompa_loompas():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            return render_template('workers.html', users=get_all_users(), name=get_user_by_id(session['user'])['name'], admin=check_admin(session['user']))
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')

@app.route('/rewards')
def rewards():
    if session['login'] and session['user']:
        return render_template('rewards.html', name=get_user_by_id(session['user'])['name'], rewards=get_all_rewards(), admin=check_admin(session['user']))
    else:
        return redirect('/login')

@app.route('/rewards/<reward>', methods=['GET','POST'])
def redeem_reward(reward):
    if session['login'] and session['user']:
        flash(claim_reward(session['user'], reward))
        return redirect('/rewards')
    else:
        return redirect('/login')

@app.route('/feedback')
def feedback():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            return render_template('feedback_admin.html', read_feedback=get_read_feedback(), unread_feedback=get_unread_feedback(), name=get_user_by_id(session['user'])['name'], admin=check_admin(session['user']))
        else:
            return render_template('feedback.html', name=get_user_by_id(session['user'])['name'], admin=check_admin(session['user']))
    else:
        return redirect('/login')

@app.route('/feedback/submit', methods=['GET','POST'])
def submit_feedback():
    if session['login'] and session['user']:
        if request.method == 'POST':
            flash(add_feedback(request.form.get('feedback')))
            return redirect('/feedback')
        else:
            return redirect('/feedback')
    else:
        return redirect('/login')

@app.route('/feedback/read/<id>', methods=['GET','POST'])
def read_feedback(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            if request.method == 'POST':
                flash(mark_feedback_as_read(id))
                return redirect('/feedback')
            else:
                return redirect('/feedback')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')

@app.route('/feedback/delete/<id>', methods=['GET','POST'])
def feedback_delete(id):
    if session['login'] and session['user']:
        if check_admin(session['user']):
            if request.method == 'POST':
                flash(delete_feedback(id))
                return redirect('/feedback')
            else:
                return redirect('/feedback')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')

@app.route('/training')
def training_loompas():
    if session['login'] and session['user']:
        return render_template('train.html', name=get_user_by_id(session['user'])['name'], training=get_all_training(), admin=check_admin(session['user']))
    else:
        return redirect('/login')

@app.route('/training/add')
def training_add():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            return render_template('add_training.html', admin=check_admin(session['user']),  name=get_user_by_id(session['user'])['name'])
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')

@app.route('/training/add/submit', methods = ['GET', 'POST'])
def training_add_submit():
    if session['login'] and session['user']:
        if check_admin(session['user']):
            if request.method == 'POST':
                data = request.form
                flash(add_training(data.get('name'), data.get('description'), data.get('link'), data.get('points')))
                return redirect('/training')
            else:
                return redirect('/training/add')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect('/login')

@app.errorhandler(404)
def error(error):
    return render_template('404.html')


@app.errorhandler(500)
def error(error):
    session['user'] = None
    session['login'] = False
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)