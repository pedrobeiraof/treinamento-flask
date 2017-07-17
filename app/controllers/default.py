from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db, lm
from sqlalchemy import desc

from app.models.tables import User, Post, Like
from app.models.forms import LoginForm, LogonForm, PostForm


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    post = Post.query.order_by(Post.id.desc())
    like = Like.query.order_by(Like.id.desc())
    if form.validate_on_submit():
        content = form.content.data
        user = current_user.id
        i = Post(content, user)
        db.session.add(i)
        db.session.commit()
    return render_template('index.html',
                            form=form, post=post, like=like)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    db.session.execute('delete from posts where id = %s' % id)
    db.session.commit()
    return index()


@app.route("/like/<post>/<user>", methods=["GET", "POST"])
def like(post, user):
    i = Like(post, user, current_user.id)
    db.session.add(i)
    db.session.commit()
    return 



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
    i = Post("novo post",3)
    db.session.add(i)
    db.session.commit()
    return "Ok"
