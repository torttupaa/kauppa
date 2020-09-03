from flask import render_template, session, request, redirect,url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User


@app.route('/admin')
def admin():
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    return render_template('admin/index.html', title='Admin Page')


#in case of creating admin
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Hoe ' +str(form.username.data) +' kullia imet')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', title="REGUSER", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            flash("yo logged biatch")
            session['username'] = form.username.data
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash("wrong!")

    return render_template('admin/login.html', form=form, title="Login Page")

