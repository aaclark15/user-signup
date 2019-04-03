from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True


def is_valid(str1): 
    if str1 == "": 
        error= "Field cannot be blank"
    elif len(str1)<3 or len(str1)>20: 
        error= "Field needs to be between 3-20 characters"
    elif " " in str1: 
        error = "Field cannot contain a space"
    else: 
        error = ""
    return error    


def is_valid_email(email):
    if len(email)>2 and len(email)<21: 
        if re.match(r"[?)[a-zA-Z0-9]+@([?)[a-zA-Z0-9])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
    else: 
        return False


@app.route("/")
def index():
    return render_template('home.html', title="Sign-up")


@app.route("/", methods=['POST'])
def validate():

    username = request.form['username']
    password = request.form['password']
    valid_pwd = request.form['valid_pwd']
    email = request.form['email']
    user_error = ''
    pwd_error = ''
    valid_pwd_error = ''
    email_error = ''

#is_valid is working below 
#add if statements if it is valid - check all boxes
    user_error = is_valid(username)
    pwd_error = is_valid(password)

    if user_error: 
        username=''
        password = ''
        valid_pwd=''

    if pwd_error: 
        password = ''
        valid_pwd = ''

    if valid_pwd != password: 
        valid_pwd = ''
        password = ''
        valid_pwd_error = "Passwords do not match"
        
    if email != "": 
        if not is_valid_email(email): 
            email = ''
            email_error = "This is not a valid email address"


#needs to be if stmt - this comes up if wrong, redirect to welcome if right
    if not user_error and not pwd_error and not valid_pwd_error and not email_error: 
        return redirect('/welcome?username={0}'.format(username))
    else: 
        return render_template('home.html', 
        username=username, user_error=user_error,
        password=password, pwd_error=pwd_error,
        valid_pwd=valid_pwd, valid_pwd_error=valid_pwd_error,
        email=email, email_error=email_error)
        



@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username )

app.run()