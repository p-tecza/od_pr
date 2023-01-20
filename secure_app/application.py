from flask import Flask, redirect, url_for, render_template, request, make_response, send_file, session, flash
from bcrypt import checkpw, hashpw, gensalt
from uuid import uuid4
from flask_sslify import SSLify
import sqlite3
import time
from pathlib import Path
import os
import re


from queries import *

# CO JEST DODANE:
# Self-signed certyfikat do dockera
# Baza danych (hasła z salt i pepper)
# Kontrola logowania (przy 3 niepoprawnych logowaniach ban, reset licznika przy poprawnym)
# Inkrementacja długości bana +30 minut co 3 niepoprawne
# Entropia hasła, nie może być zbyt słabe inaczej nie zarejestrujesz sie
# Upload zdjec
# Rodzaj dodawanych plików
# Walidacja wpisywanych danych do foremek
# Resetowanie hasła
# Odzyskanie dostępu
# Uprawnienia do zdjec (ubogo)
# Sprawdzenie czy hasło nie jest słownikowe

app=Flask(__name__)
sslify = SSLify(app)

UPLOAD_FOLDER="images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
p_file=open('/python-docker/db_pep.txt',"r")
global_pepper=""
app.secret_key =""
for s in p_file:
    if len(s)>20:
        global_pepper=s
    elif len(s)>5:
        app.secret_key=s


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def validate_input(this_input=[]):
    for x in this_input:
        if len(x)>100 or len(x)==0:
            return False
    return True

def replace_html(this_input):
    re.sub("/</g", "&lt", this_input)
    re.sub("/>/g", "&gt;", this_input)
    #new_input = this_input.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return this_input

@app.route("/")
def login_page():
    session['username']=""
    return render_template("login.html")

@app.route("/loginattempt", methods=["POST","GET"])
def main_page():
    time.sleep(1)     
    name = request.form["name"]
    password = request.form["pass"]


    name=replace_html(name)
    password=replace_html(password)

    if not validate_input([name,password]):
        return render_template("register.html",wrongLoginData="problem with input")


    if login_attempt(name):
        if check_if_banned(name):
            return render_template("login.html",wrongLoginData="account blocked.")

        if checkpw((password+global_pepper).encode('utf-8'),get_pass_hashed(name)):
            reset_bad_login_counter(name)
            session['username']=name
            return redirect("/index")
        else:
            if int(increment_bad_login_spree(name))>2:
                unlock_date=ban_account_for_minutes(name,30)
                message="account blocked until "+str(unlock_date)+"."
                return render_template("login.html",wrongLoginData=message)
    return render_template("login.html",wrongLoginData="incorrect login data.")

    

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('username',None)
    return redirect("/")

@app.route("/index", methods=["POST", "GET"])
def index():
    if not session['username']:
        return redirect("/")
    return render_template("index.html")


@app.route("/register")
def register_user():
    return render_template("register.html")

@app.route("/settings")
def settings_user():
    if not session['username']:
        return redirect("/")
    return render_template("settings.html")

@app.route("/addnewuser", methods=["POST"])
def add_user():

    login = request.form["name"]
    password = request.form["pass"]
    quest=request.form["quest"]
    answer=request.form["answer"]

    login = replace_html(login)
    password=replace_html(password)
    quest=replace_html(quest)
    answer=replace_html(answer)

    if not validate_input([login,password,quest,answer]):
        return render_template("register.html",errorMsg="problem with input")

    if check_if_username_exists(login):
        return render_template("register.html", errorMsg="user with that name already exists.")
    else:

        document=open("common_pass.txt","r")
        for x in document:
            if x[0:len(x)-1]==password:
                return render_template("register.html", errorMsg="password not original enough.")

        pass_bytes=(password+global_pepper).encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        if create_new_user(login,hash):
            session['username']=login
            code=commit_new_restore(login,quest,answer)
            return render_template("index.html",restoreCode=code)
        return render_template("register.html", errorMsg="problem occured while creating account.")
        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_image", methods=["POST"])
def upload_image():
    if not session['username']:
        return redirect("/")
    if 'nazwa' not in request.files:
        errormsg='no file part'
        return render_template("index.html",error=errormsg)
    image=request.files['nazwa']
    is_shared=request.form.get('shared')

    if image.filename == '':
        errormsg ='no selected file'
        return render_template("index.html",error=errormsg)
    if not allowed_file(image.filename):
        errormsg='wrong file type (not [jpg, jpeg, png])'
        return render_template("index.html",error=errormsg)

    user_directory=app.config['UPLOAD_FOLDER']+str(session['username'])
    Path(user_directory).mkdir(parents=True, exist_ok=True)
    save_location=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"+str(image.filename)

    if is_shared:
        Path(app.config['UPLOAD_FOLDER']+"__shared__").mkdir(parents=True, exist_ok=True)
        save_location=app.config['UPLOAD_FOLDER']+"__shared__/"+str(image.filename)

    image.save(save_location)
    return redirect("/index")


@app.route("/changepassword", methods=["POST"])
def change_password():

    if not session['username']:
        return redirect("/")


    old=request.form["name"]
    new=request.form["pass"]

    old=replace_html(old)
    new=replace_html(new)

    if not validate_input([old,new]):
        return render_template("settings.html",error="problem with input")


    name=session['username']
    pass_bytes=(new+global_pepper).encode('utf-8')
    hash_new=hashpw(pass_bytes,gensalt())

    if try_to_change_password(name,old,hash_new,global_pepper):
        return render_template("settings.html",error="successfully changed password")
    else:
        return render_template("settings.html",error="wrong password")


@app.route("/forgot")
def forgot_password():
    return render_template("forgot.html")

@app.route("/fetchquestion",methods=["POST"])
def fetch_quest():

    name=request.form["name"]
    name=replace_html(name)

    if not validate_input([name]):
        return render_template("settings.html",error="problem with input")

    return render_template("forgot.html",fetched_quest=get_quest_for_user(name))

@app.route("/answerrestore", methods=["POST"])
def ansrestore():
    name=request.form["name"]
    answ=request.form["pass"]
    new_pass=request.form["new_pass"]

    name=replace_html(name)
    answ=replace_html(answ)
    new_pass=replace_html(new_pass)

    if not validate_input([name,answ,new_pass]):
        return render_template("settings.html",error="problem with input")
    if check_if_answer_correct(name,answ):
        pass_bytes=(new_pass+global_pepper).encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        just_change_password(name,hash)
        return render_template("login.html",wrongLoginData="password restored.")
    else:
        return render_template("login.html",wrongLoginData="password not restored. wrong data")

@app.route("/coderestore",methods=["POST"])
def coderestore():
    name=request.form["name"]
    code=request.form["pass"]
    new_pass=request.form["new_pass"]

    name=replace_html(name)
    code=replace_html(code)
    new_pass=replace_html(new_pass)
    if check_if_code_correct(name,code):
        pass_bytes=(new_pass+global_pepper).encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        just_change_password(name,hash)
        return render_template("login.html",wrongLoginData="password restored.")
    else:
        return render_template("login.html",wrongLoginData="password not restored. wrong data")

@app.route("/navigate_my_images")
def nav_my_img():
    return render_template("images.html")

@app.route("/myimages")
def return_images():

    path=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"
    photos=os.listdir(path)
    return photos

@app.route("/image/<myImage>")
def show_image(myImage):
    path=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"
    return send_file(str(path+str(myImage)), mimetype='image/gif')


@app.route("/navigate_shared_images")
def nav_shared_img():
    return render_template("shared.html")

@app.route("/sharedimages")
def return_shared():
    path=app.config['UPLOAD_FOLDER']+"__shared__/"
    photos=os.listdir(path)
    return photos

@app.route("/image-shared/<myImage>")
def show_shared_image(myImage):
    path=app.config['UPLOAD_FOLDER']+"__shared__/"
    return send_file(str(path+str(myImage)), mimetype='image/gif')

if __name__=="__main__":
    #app.run(host="0.0.0.0", port=5678, ssl_context='adhoc') # nie docker | 
    app.run(host="0.0.0.0", port=5678, ssl_context=('/python-docker/server.crt','/python-docker/server.key')) #docker




