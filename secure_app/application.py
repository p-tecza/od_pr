from flask import Flask, redirect, url_for, render_template, request, make_response, send_file
from bcrypt import checkpw, hashpw, gensalt
from uuid import uuid4
from flask_sslify import SSLify

app=Flask(__name__)
sslify = SSLify(app)
redis_url = "redis://127.0.0.1"
app.config["REDIS_URL"] = redis_url

authenticated_users={}
name_of_user=""
number_of_entries=0 #TESTOWANIE
previous_no_entries=0 #TESTOWANIE

@app.route("/")
def login_page():
    sid = request.cookies.get("sid")
    if sid in authenticated_users:
        return render_template("index.html",name_pass=name_of_user, number_of_entries=number_of_entries)
    return render_template("login.html")

@app.route("/page", methods=["POST","GET"])
def main_page():
    name = request.form["name"]
    # password = request.form["pass"]
    # hashed_password=redis_user_db.get(name)

    # if not hashed_password:
    #     return render_template("login.html", wrongLoginData="user does not exist.")

    response = redirect("/", code=302)

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

    return response

@app.route("/logout", methods=["GET"])
def logout():
    response= make_response(request.host)
    response.set_cookie('sid', '', expires=0)
    return response 

@app.route("/index", methods=["POST", "GET"])
def index():

    if request.method=="POST":
        login = request.form["login"]
        password = request.form["pass"]
        return render_template("index.html", username=login, greet="user: ")
    else:
        return render_template("index.html")


@app.route("/register")
def register_user():
    return render_template("register.html")

@app.route("/addnewuser", methods=["POST"])
def add_user():

    login = request.form["name"]
    password = request.form["pass"]
    email=request.form["email"]

    if False:#(redis_user_db.get(login)):
        return render_template("register.html", errorMsg="user with that name already exists.")
    else:
        pass_bytes=password.encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        # redis_user_db.mset({str(login):hash})
        # redis_email_db.mset({str(login):str(email)})
        return redirect("/",code=302)


@app.route("/get_image/<image_name>")
def response_image(image_name):
    path="product-images/"+image_name
    return send_file(path,mimetype="img/gif")


if __name__=="__main__":
    #app.run(host="0.0.0.0", port=5000, ssl_context='adhoc') # nie docker
    app.run(host="0.0.0.0", port=5000, ssl_context=('/python-docker/server.crt','/python-docker/server.key')) #docker




