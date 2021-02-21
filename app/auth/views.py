from flask_login.utils import logout_user
from app.models import UserData
from flask import render_template, redirect, flash, url_for, session
from . import auth
from app.forms import LoginForm
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash
#nueva vista que es como una ruta

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form':login_form
    }
    #render html templates
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('Información no coincide')        
        else:
            flash('El usuario no existe')
            

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form':signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)

        if user_doc.to_dict() in None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)
            user = UserModel(UserModel)
            login_user(user)
            flash('Bienvenido!')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe!')
    return render_template('signup.html', **signup_form)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    
    return redirect(url_for('auth.login'))