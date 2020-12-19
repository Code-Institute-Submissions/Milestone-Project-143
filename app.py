import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/get_projects")
def get_projects():
    projects = mongo.db.projects.find()
    return render_template("projects.html", projects=projects)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if email already exists within db
        existing_email = mongo.db.employees.find_one(
            {"email": request.form.get("email").lower()})

        if existing_email:
            flash("Email already in use, try logging in instead.")
            return redirect(url_for("login"))

        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "phone": request.form.get("phone").lower(),
            "email": request.form.get("email").lower(),
            "employee_id": request.form.get("employee_id"),
            "dob": request.form.get("dob"),
            "manager_id": request.form.get("manager_id"),
            "title": request.form.get("title").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.employees.insert_one(register)

        # put the new user into 'session' cookie
        session["employee"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", email=session["employee"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.employees.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["employee"] = request.form.get("email").lower()
                    flash("Welcome {}!".format(
                        existing_user["first_name"].capitalize()))
                    return redirect(url_for("profile", email=session["employee"]))
            else:
                # invalid password match
                flash("Incorrect email and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/profile/<email>", methods=["GET", "POST"])
def profile(email):
    # grab the session user's first name from db
    first_name = mongo.db.employees.find_one(
        {"email": session["employee"]})["first_name"]
    last_name = mongo.db.employees.find_one(
        {"email": session["employee"]})["last_name"]
    return render_template("profile.html", first_name=first_name.capitalize(), last_name=last_name.capitalize(), )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  ##Change to false below submission