import os

from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from forms import *
from models import *

app=Flask(__name__)

app.secret_key = os.environ.get('SECRET')

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)

socketio=SocketIO(app)

ROOMS = ["General","News","Coding","Games"]

login=LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():

    new_form=RegistrationForm()
    if new_form.validate_on_submit():
        username = new_form.username.data
        password = new_form.password.data

        hash_password = pbkdf2_sha256.hash(password)
        
        t_user = User(username=username, password=hash_password)
        db.session.add(t_user)
        db.session.commit()
        flash('Registered succesfully! Please login!', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=new_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    new_login_form=LoginForm()
    if new_login_form.validate_on_submit():
        user_object = User.query.filter_by(username=new_login_form.username.data).first()
        #return "Successfully logged in!"
        login_user(user_object)
        return redirect(url_for('chat'))
        

    return render_template("login_page.html", form=new_login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template('chat_page.html', username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have succesfully logged out!', 'success')
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%d-%b %I:%M:%S %p', localtime())}, room=data['room'])


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])


if __name__ == "__main__":
    app.run()