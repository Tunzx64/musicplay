from flask import Blueprint, render_template, url_for, redirect, flash, request
from models import db, User
from utils.form import FormLogin, FormRegister
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

setup_users = Blueprint('user_setup', __name__)

@setup_users.route('/login', methods=['POST', 'GET'])
def logar_user():
    form = FormLogin()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logado com sucesso !')
            return redirect(url_for('home.index'))
        else:
            flash('Senha ou email incorretos !')
            return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)

@setup_users.route('/register', methods=['POST', 'GET'])
def registrar_user():
    form = FormRegister()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        ip = request.remote_addr
        password = generate_password_hash(form.password.data)

        if User.query.filter_by(email=email).first():
            flash('Já existe um usuario utilizando esse email !')
            return render_template('register.html', form=form)
        if User.query.filter_by(ip_adress=ip).first():
            flash('Você já tem uma conta criada entre nela !')
            return redirect(url_for('home.index'))
        
        else:
            new_user = User(name=name, email=email, password=password, ip_adress=ip)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro finalizado com sucesso ! Logue em sua Conta')
            return redirect(url_for('home.index'))
    
    return render_template('register.html', form=form)

@setup_users.route('/logout', methods=['GET', 'POST'])
def deslogar(): 
    logout_user()
    flash('Você saiu da sua conta !')
    return redirect(url_for('home.index'))
        
