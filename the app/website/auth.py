from flask import Blueprint , render_template, request, flash, redirect, url_for
from bson import objectid
import pymongo
from pymongo import MongoClient
from flask_login import login_user, logout_user, current_user


cluster = MongoClient("mongodb+srv://iamnivedhav:N1vedha@cluster0.hfklgll.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=5000)
db= cluster["myapp"]
products = db["products"]
users= db['users']

auth = Blueprint('auth',__name__)

@auth.route('/', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form.get("email")
        password= request.form.get("password")
        user= db.users.find_one({'email':email})
        if user:
            if password == user['password']:
                flash('Logged in successfuly.',category= 'success')
                return redirect(url_for("views.home",user_id=user['user_id']))
            else:
                flash('error2.',category= 'error')   
        else:
             flash('error.',category= 'error')   
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged Out',category= 'success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods= ['GET','POST'])
def sign_up():
    if request.method == 'POST':

        name= request.form.get("user_name")
        email= request.form.get("email")
        password= request.form.get("password")
        contact_number= request.form.get("contact_no")
        user= db.users.find_one({'email':email})
        if user:
            flash('Email already registered. Login.',category= 'error')
        if len(email)<5:
            flash('email must have at least 5 charachters.',category= 'error')
        if len(name)<3:
            flash("name must have at least 3 charachters.", category='error')
        if type(contact_number) != int or len(str(contact_number)) != 10:
            flash("invalid contact number.",category='error')
        if len(password)<7:
            flash('email must have at least 7 charachters.',category= 'error')    
        else:
            user_details= {'_id':105,'user_id':105,'user_name':name, 'email':email, 'contact_no':contact_number,'password':password}
            db.users.insert_one(user_details)
            flash("Acount Created", category='success')
            return redirect(url_for("views.home",user_id=user_details['user_id']))

    return render_template("sign-up.html")