from flask import Flask, redirect, url_for, render_template, request, make_response, send_file, session, flash
from bcrypt import checkpw, hashpw, gensalt
from uuid import uuid4
from flask_sslify import SSLify
import sqlite3
import time
from pathlib import Path


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


# DO DODANIA:
# Resetowanie hasła / odzyskanie dostępu
# Opoznienie w requestach (nie jest dobrze zrobione xd)
# Uprawnienia do zdjec
# Bezpieczne przechowywanie plików graficznych
# Z jakiego ip kto się łączył (może)
# Sprawdzenie czy hasło nie jest słownikowe


app=Flask(__name__)
# sslify = SSLify(app)

UPLOAD_FOLDER="images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
global_pepper="1208r329h1f933fqiojbgviuoir@!#12e13ss1@fgb93rfqufijobneiwourfer12312#@!#!@"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/loginattempt", methods=["POST","GET"])
def main_page():

    time.sleep(1)               #opoznienie logowania

    name = request.form["name"]
    password = request.form["pass"]
    
    print("ADDR: "+str(request.remote_addr))
    # if not hashed_password:
    #     return render_template("login.html", wrongLoginData="user does not exist.")


    # print("DANE: "+name + "|" + password )
    # print("HASZ:"+str(hashpw((password+global_pepper).encode('utf-8'),gensalt())))
    # print("(password+global_pepper).encode('utf-8'): ",(password+global_pepper).encode('utf-8'))

    
    # print("TYP HASH: ",type(get_pass_hashed(name)))

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

    # if checkpw(password.encode('utf-8'),hashed_password):
    #     sid = str(uuid4())
    #     authenticated_users[sid] = name
    #     global name_of_user
    #     name_of_user=name
    #     response = redirect("/", code=302)
    #     response.set_cookie("sid", sid)
    #     return response
    # else:
    #     return render_template("login.html", wrongLoginData="wrong password/username.")

    

@app.route("/logout", methods=["GET"])
def logout():
    response= make_response(request.host)
    session.pop('username',None)
    response.set_cookie('sid', '', expires=0)
    return response 

@app.route("/index", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/register")
def register_user():
    return render_template("register.html")

@app.route("/addnewuser", methods=["POST"])
def add_user():

    login = request.form["name"]
    password = request.form["pass"]

    if check_if_username_exists(login):
        return render_template("register.html", errorMsg="user with that name already exists.")
    else:
        pass_bytes=(password+global_pepper).encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        print("DANE: "+login + "|" + password )
        print("HASZ:"+str(hash))
        print("(password+global_pepper).encode('utf-8'): ",(password+global_pepper).encode('utf-8'))
        if create_new_user(login,hash):
            session['username']=login
            return render_template("index.html")
        return render_template("register.html", errorMsg="problem occured while creating account.")
        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_image", methods=["POST"])
def upload_image():
    
    if 'nazwa' not in request.files:
        errormsg='no file part'
        return render_template("index.html",error=errormsg)
    image=request.files['nazwa']
    if image.filename == '':
        errormsg ='no selected file'
        return render_template("index.html",error=errormsg)
    if not allowed_file(image.filename):
        errormsg='wrong file type (not [jpg, jpeg, png])'
        return render_template("index.html",error=errormsg)

    user_directory=app.config['UPLOAD_FOLDER']+str(session['username'])
    Path(user_directory).mkdir(parents=True, exist_ok=True)
    save_location=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"+str(image.filename)
    image.save(save_location)
    return redirect("/index")


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5678) # nie docker | ssl_context='adhoc'
    #app.run(host="0.0.0.0", port=5000, ssl_context=('/python-docker/server.crt','/python-docker/server.key')) #docker




