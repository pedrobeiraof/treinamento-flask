from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, lm

from app.models.tables import User
from app.models.forms import LoginForm, LogonForm


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in")
            return redirect(url_for("index"))
        else:
            flash("Invalid Login")
    return render_template('login.html',
                            form=form)


@app.route("/logon", methods=["GET", "POST"])
def logon():
    form = LogonForm()
    user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        if user:
            flash("Nome de Usuario ja foi cadastrado")
        else:
            password = form.password.data
            username = form.username.data
            name = form.name.data
            email = form.email.data
            i = User(username, password, name, email)
            db.session.add(i)
            db.session.commit()
            flash("Cadastro Efetuado com Sucesso")
            return redirect(url_for('index'))

    return render_template('logon.html',
                            form=form)


@app.route("/delete")
def delete():
    user = User.query.filter_by(username=form.username.data).first()
    return render_template('delete.html')


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("index"))


@app.route("/read/<info>")
@app.route("/read", defaults={"info": None})
def read(info):
    r = User.query.all()
    print (r)
    return "OK"


@app.route("/add")
def add():
    i = User("jose", "1234", "Jose", "jose@email.com")
    db.session.add(i)
    db.session.commit()
    return "Ok"


