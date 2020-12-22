import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import boto3
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Setup Connection to MongoDB
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Setup Connection Variables for AWS server for image storage
BUCKET_NAME = "pmtoolms3"
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(BUCKET_NAME)

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET)


# Home Page Rendering
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.employees.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"],
                request.form.get("password")):
                session["employee"] = request.form.get("email").lower()
                flash("Welcome {}!".format(
                    existing_user["first_name"]
                    .capitalize()))
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


# Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    employees = mongo.db.employees.distinct("employee_id")
    if request.method == "POST":
        # check if email already exists within db
        existing_email = mongo.db.employees.find_one(
            {"email": request.form.get("email").lower()})

        if existing_email:
            flash("Email already in use, try logging in instead.")
            return redirect(url_for("login"))

        # Upload Image to AWS
        img = request.files["file"]
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
        imglocation = "{}{}".format(S3_LOCATION, filename)

        # Insert Info into Mondo DB
        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "phone": request.form.get("phone").lower(),
            "email": request.form.get("email").lower(),
            "employee_id": request.form.get("employee_id"),
            "dob": request.form.get("dob"),
            "manager_id": request.form.get("manager_id"),
            "title": request.form.get("title").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "imgurl": imglocation
        }
        mongo.db.employees.insert_one(register)

        # put the new user into 'session' cookie
        session["employee"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", email=session["employee"]))
    print(employees)
    return render_template("register.html", employees=employees)


# Client Directory
@app.route("/clients")
def clients():
    clients = list(mongo.db.clients.find())
    projects = mongo.db.projects.find()
    print(clients)
    return render_template("client.html", clients=clients, projects=projects)


# Add Client Functionality
@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        # check if client ID already exists within db
        existing_id = mongo.db.clients.find_one(
            {"client_id": request.form.get("client_id")})

        if existing_id:
            flash("Client ID already in use, try another ID number.")
            return render_template("client.html")

        # Insert Info into Mondo DB
        clientregister = {
            "name": request.form.get("client_name").lower(),
            "contact": request.form.get("client_contact").lower(),
            "phone": request.form.get("phone"),
            "email": request.form.get("email").lower(),
            "client_id": request.form.get("client_id"),
            "address": request.form.get("client_address").lower(),
        }
        mongo.db.clients.insert_one(clientregister)
        flash("Registration Successful!")
        return redirect(url_for("clients"))
    return render_template("client.html")


# Edit Client Functionality and page rendering
@app.route("/edit_client/<client_id>", methods=["GET", "POST"])
def edit_client(client_id):
    if request.method == "POST":
        # Insert Info into Mondo DB
        clientregister = {
            "name": request.form.get("client_name").lower(),
            "contact": request.form.get("client_contact").lower(),
            "phone": request.form.get("phone"),
            "email": request.form.get("email").lower(),
            "client_id": client_id,
            "address": request.form.get("client_address").lower(),
        }
        mongo.db.clients.update({"client_id": client_id}, clientregister)
        flash("Updated Successful!")
        return redirect(url_for("clients"))

    client = mongo.db.clients.find_one({"client_id": client_id})
    return render_template("edit_client.html", client=client)


# Delete Client - Admin Only
@app.route("/delete_client/<client_id>")
def delete_client(client_id):
    mongo.db.clients.remove({"client_id": client_id})
    flash("Client Successfully Deleted")
    return redirect(url_for("clients"))


# Client Search Query
@app.route("/client_search", methods=["GET", "POST"])
def client_search():
    query = request.form.get("clientquery")
    clients = list(mongo.db.clients.find({"$text": {"$search": query}}))
    return render_template("client.html", clients=clients)


# Project Directory
@app.route("/get_projects")
def get_projects():
    clients = list(mongo.db.clients.find())
    projects = list(mongo.db.projects.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    return render_template("projects.html",
                           projects=projects,
                           clients=clients, employees=employees)


# Add project Functionality
@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    # Insert Info into Mondo DB
    project_no = list(mongo.db.projects.distinct("project_no"))
    project_no_int = list(map(int, project_no))
    project_no_int.sort()
    new_project_no = project_no_int[-1] + 1
    projectregister = {
            "project_no": new_project_no,
            "project_name": request.form.get("project_name").lower(),
            "project_description":
            request.form.get("project_description").lower(),
            "client_id": request.form.get("client_id"),
            "project_manager_id": request.form.get("manager_id"),
            "team": request.form.getlist("team"),
            "start_date": request.form.get("startdate"),
            "end_date": request.form.get("enddate"),
            "fee":  request.form.get("fee")
    }
    mongo.db.projects.insert_one(projectregister)
    flash("Registration Successful!")
    return redirect(url_for("get_projects"))


# Project Search Query
@app.route("/project_search", methods=["GET", "POST"])
def project_search():
    query = request.form.get("projectquery")
    projects = list(mongo.db.projects.find({"$text": {"$search": query}}))
    return render_template("projects.html", projects=projects)


# Render Employee Profile
@app.route("/profile/<email>", methods=["GET", "POST"])
def profile(email):
    # grab the session user's first name from db
    first_name = mongo.db.employees.find_one(
        {"email": email})["first_name"]
    last_name = mongo.db.employees.find_one(
        {"email": email})["last_name"]
    imgurl = mongo.db.employees.find_one(
        {"email": email})["imgurl"]
    title = mongo.db.employees.find_one(
        {"email": email})["title"]
    email = mongo.db.employees.find_one(
        {"email": email})["email"]
    phone = mongo.db.employees.find_one(
        {"email": email})["phone"]
    managerid = mongo.db.employees.find_one(
        {"email": email})["manager_id"]
    managername = ' '.join([mongo.db.employees.find_one
                           ({"employee_id": managerid})["first_name"],
                            mongo.db.employees.find_one(
                            {"employee_id": managerid})["last_name"]])
    manageremail = mongo.db.employees.find_one(
        {"employee_id": managerid})["email"]

    if session["employee"]:
        return render_template("profile.html",
                               first_name=first_name.capitalize(),
                               last_name=last_name.capitalize(),
                               imgurl=imgurl, title=title,
                               phone=phone, email=email,
                               managername=managername,
                               manageremail=manageremail)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("employee")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # Change to false below submission
