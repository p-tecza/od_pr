from flask import Flask, redirect, url_for, render_template, request, make_response, send_file, session, flash
from bcrypt import checkpw, hashpw, gensalt
from uuid import uuid4
from flask_sslify import SSLify
import sqlite3
import time
from pathlib import Path
import os
import imghdr



from queries import *
from validation_sanitization import *

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
# Uprawnienia do zdjec (mutual friends muszą być żeby shared-friends działało)
# Sprawdzenie czy hasło nie jest słownikowe
# --------------------------------------------
# walidacja danych wejściowych na backendzie (dobra walidacja)
# sprawdzanie czy zdjęcie jest zdjęciem - biblioteka imagehdr
# hashowanie odpowiedzi i kodu



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

# DO DEVELOPMENTU
# global_pepper="1208r329h1f933fqiojbgviuoir@!#12e13ss1@fgb93rfqufijobneiwourfer12312#@!#!@"
# app.secret_key ="super secret key"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        return render_template("login.html",wrongLoginData="problem with input")

    if not name_validate(name):
        return render_template("login.html",wrongLoginData="problem with input (n)")

    if not password_validate(password):
        return render_template("login.html",wrongLoginData="problem with input (p)")

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

    if 'code' in session:
        s_var=session['code']
        session['code']=""
        session.pop('code',None)
        return render_template("index.html",restoreCode=s_var, user=session['username'])

    return render_template("index.html",user=session['username'])


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

    if not name_validate(login):
        return render_template("register.html",errorMsg="bad username")

    if not password_validate(password):
        return render_template("register.html",errorMsg="password not fiting requirements")

    if not question_validation(quest):
        return render_template("register.html",errorMsg="something's wrong with question")

    if not answer_validation(answer):
        return render_template("register.html",errorMsg="something's wrong with answer")

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

            answ_bytes=(answer+global_pepper).encode('utf-8')
            hash_answ=hashpw(answ_bytes,gensalt())
            code=commit_new_restore(login,quest,hash_answ,global_pepper)
            session['code']=code
            return redirect("/index")
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

    is_image_valid=imghdr.what(image)

    if is_image_valid is None:
        return render_template("index.html",error="corrupted image file.")

    if not checkbox_validation(is_shared):
        return render_template("index.html",error="something wrong with checkbox.")

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
        selected_val=request.form.get('share_how')
        if not select_validation(selected_val):
            errormsg='something wrong with selected value'
            return render_template("index.html",error=errormsg)

        if selected_val == "public":
            Path(app.config['UPLOAD_FOLDER']+"__shared__").mkdir(parents=True, exist_ok=True)
            save_location=app.config['UPLOAD_FOLDER']+"__shared__/"+str(image.filename)
        elif selected_val == "friends":
            user_directory=app.config['UPLOAD_FOLDER']+str(session['username'])+"/shared"
            Path(user_directory).mkdir(parents=True, exist_ok=True)
            save_location=user_directory+"/"+str(session['username'])+"-"+str(image.filename)

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

    if not password_validate(old):
        return render_template("settings.html",error="old passwords' format is not valid")

    if not password_validate(new):
        return render_template("settings.html",error="new password must be 8 characters long \
        and contain at least one: big letter, small leter, digit")

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
        return render_template("forgot.html",error="problem with input")

    if not name_validate(name):
        return render_template("forgot.html",error="problem with input (n)")

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
        return render_template("forgot.html",error="problem with input",fetched_quest="error! not correct restoration attempt")

    if not name_validate(name):
        return render_template("forgot.html",error="problem with input (n)",fetched_quest="error! not correct restoration attempt")

    if not answer_validation(answ):
        return render_template("forgot.html",error="problem with input (a)",fetched_quest="error! not correct restoration attempt")

    if not password_validate(new_pass):
        return render_template("forgot.html",error="new pass too weak!",fetched_quest="error! not correct restoration attempt")

    if check_if_answer_correct(name,answ,global_pepper):
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

    if not name_validate(name):
        return render_template("forgot.html",error="problem with input (n)",fetched_quest="error! not correct restoration attempt")

    if not password_validate(new_pass):
        return render_template("forgot.html",error="new pass too weak!",fetched_quest="error! not correct restoration attempt")

    if not code_validation(code):
        return render_template("forgot.html",error="wrong code structure!",fetched_quest="error! not correct restoration attempt")

    name=replace_html(name)
    code=replace_html(code)
    new_pass=replace_html(new_pass)
    if check_if_code_correct(name,code,global_pepper):
        pass_bytes=(new_pass+global_pepper).encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        just_change_password(name,hash)
        return render_template("login.html",wrongLoginData="password restored.")
    else:
        return render_template("login.html",wrongLoginData="password not restored. wrong data")

@app.route("/navigate_my_images")
def nav_my_img():
    if not session['username']:
        return redirect("/")
    return render_template("images.html")

@app.route("/myimages")
def return_images():
    if not session['username']:
        return redirect("/")
    path=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"
    isExist = os.path.exists(path)
    if not isExist:
        return []
    photos=os.listdir(path)
    return photos

@app.route("/image/<myImage>")
def show_image(myImage):
    if not session['username']:
        return redirect("/")
    path=app.config['UPLOAD_FOLDER']+str(session['username'])+"/"
    return send_file(str(path+str(myImage)), mimetype='image/gif')

@app.route("/navigate_friends_images")
def nav_fr_img():
    if not session['username']:
        return redirect("/")
    return render_template("shared_friends.html")

@app.route("/friendsimages")
def return_friends_imgs():
    if not session['username']:
        return redirect("/")
    name=session['username']
    friends=get_friends(name)

    all_friends_images=[]

    for x in friends:
        if check_if_mutual_friends(name,x):
            path=app.config['UPLOAD_FOLDER']+str(x)+"/shared/"
            isExist = os.path.exists(path)
            if not isExist:
                continue
            for y in os.listdir(path):
                all_friends_images.append(y)
    return all_friends_images

@app.route("/image-friends/<image>")
def show_friend_image(image):
    if not session['username']:
        return redirect("/")

    friend_name=image.split("-")[0]

    print("friend name from filename: ",friend_name)

    path=app.config['UPLOAD_FOLDER']+friend_name+"/shared/"
    return send_file(str(path+str(image)), mimetype='image/gif')


@app.route("/navigate_shared_images")
def nav_shared_img():
    if not session['username']:
        return redirect("/")
    return render_template("shared.html")

@app.route("/sharedimages")
def return_shared():
    if not session['username']:
        return redirect("/")
    path=app.config['UPLOAD_FOLDER']+"__shared__/"
    isExist = os.path.exists(path)
    if not isExist:
        return []

    photos=os.listdir(path)
    return photos

@app.route("/image-shared/<myImage>")
def show_shared_image(myImage):
    if not session['username']:
        return redirect("/")
    path=app.config['UPLOAD_FOLDER']+"__shared__/"
    return send_file(str(path+str(myImage)), mimetype='image/gif')


@app.route("/newfriend", methods=["POST"])
def new_friend():
    if not session['username']:
        return redirect("/")
    friend=request.form['friend_name']
    if not validate_input([friend]):
        return render_template("settings.html",error="problem with input")
    name=session['username']

    if name==friend:
        return render_template("settings.html",error="unfortunately you cant add yourself as a friend")

    if login_attempt(friend):
        if not check_if_already_friends(name,friend):
            add_new_friend(name, friend)
            return render_template("settings.html",error="successfully added friend")
        else:
            return render_template("settings.html",error="you are already friend with that user")
    else:
        return render_template("settings.html",error="this user doesnt exist")

@app.route("/getfriends")
def getting_friends():

    if not session['username']:
        return redirect("/")
    name=session['username']
    friends=get_friends(name)
    return friends


if __name__=="__main__":
    # app.run(host="0.0.0.0", port=5678, ssl_context='adhoc') # nie docker | 
    app.run(host="0.0.0.0", port=5678, ssl_context=('/python-docker/server.crt','/python-docker/server.key')) #docker




