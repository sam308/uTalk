from flask import Flask, render_template, redirect, url_for, flash



from forms import *
from models import *

app=Flask(__name__)

app.secret_key = 'replace'

app.config['SQLALCHEMY_DATABASE_URI']="postgresql:///samarpan"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


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
        return "Successfully logged in!"
        #login_user(user_object)
        #return redirect(url_for('chat'))


    return render_template("login_page.html", form=new_login_form)
