from flask import Flask, flash, request, session
from flask.templating import render_template
from werkzeug.utils import redirect
from functions.users import check_for_user

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
        
    return redirect('/login')

@app.route('/logout')
def logout():
    if session['login']:
        session['login'] = False
    flash('successfully logged out')    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)