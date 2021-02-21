from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from app.firestore_service import delete_todo, get_todos, get_users, put_todo, update_todo
import unittest

from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from flask_login import login_required, current_user
#create a flask app
app = create_app()



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

#get ip from user and redirect to another route
@app.route('/')
def index():
    #setting a cookie
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    
    return response

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    #use context variables to show in the html
    user_ip = session.get('user_ip')
    #login_form = LoginForm()
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    context = {
        'user_ip':user_ip,
        'todos':get_todos(username),
        #'login_form':login_form,
        'username':username,
        'todo_form':todo_form,
        'delete_form':delete_form,
        'update_form':update_form,
    }
    
    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)
        flash('Tarea creada con exito')
        return redirect(url_for('hello'))
    return render_template('hello.html', **context)

#dinamyc route
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id, todo_id, done)
    print('Done', done)
    return redirect(url_for('hello'))