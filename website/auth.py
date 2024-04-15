import requests
from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for, session
from .models import add_users, check_exist_username
import sqlite3
auth = Blueprint('auth',__name__)



@auth.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        api_url = 'http://127.0.0.1:5000/users'
        response = requests.get(api_url)
        if response.status_code ==200:
            users = response.json()

            for user in users:
                if user['username'] == username and user['password'] == password:
                    if 'users' not in session:
                        session['users'] = []
                    # Thêm thông tin người dùng vào danh sách trong session
                    session['users'].append({
                        'id': user['id'],
                        'full_name': user['full_name'],
                        'username': user['username'],
                        'email': user['email'],
                    })
                    flash('Login successful!', category='success')
                    return redirect(url_for('views.home'))

            flash('Invalid username or password', category='error')
    return render_template('login.html')

@auth.route('/register', methods =['POST','GET'])
def register():
    if request.method == 'POST':
        fullName = request.form.get('fullName')  # Sử dụng 'request.form.get' 
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        if check_exist_username(username):
            flash('Username has existed', category='error')
        elif password!= confirmPassword:
            flash('Password and confirm password do not match', category='error')
        else:
            flash('Register successfully!', category='true')
            add_users(fullName, email, username, password)
    return render_template('register.html')
@auth.route('/account')
def account():
    return render_template('account.html')
@auth.route('/logout')
def logout():
    session.pop('users', None)
    # Redirect user to the desired page after logout
    return redirect(url_for('views.home'))