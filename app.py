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
    # create lists to pass to template
    clients = list(mongo.db.clients.find())
    projects = list(mongo.db.projects.find())
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
    #create lists to pass to template
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
    # project converted to int to match db type
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
    clients = list(mongo.db.clients.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    projects = list(mongo.db.projects.find({"$text": {"$search": query}}))
    return render_template("projects.html",
                           projects=projects,
                           clients=clients, employees=employees)


# Edit Project Functionality and page rendering
@app.route("/edit_project/<project_no>", methods=["GET", "POST"])
def edit_project(project_no):
    #convert string to int as per db
    int_project_no = int(project_no)
    if request.method == "POST":
        # Insert Info into Mondo DB
        projectregister = {
            "project_no": int_project_no,
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
        mongo.db.projects.update(
                                 {"project_no": int_project_no},
                                 projectregister)
        flash("Project Update Successful!")
        return redirect(url_for("get_projects"))
    #create lists to pass to templates
    clients = list(mongo.db.clients.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    project = mongo.db.projects.find_one({"project_no": int_project_no})
    return render_template("edit_project.html",
                           project=project,
                           clients=clients, employees=employees)


# Delete Project - Admin & PM Only
@app.route("/delete_project/<project_no>")
def delete_project(project_no):
    # convert to int to match db
    int_project_no = int(project_no)
    mongo.db.projects.remove({"project_no": int_project_no})
    flash("Project Successfully Deleted")
    return redirect(url_for("get_projects"))


# Employee Directory
@app.route("/get_employees")
def get_employees():
    #create list to pass to template
    managers = list(mongo.db.employees.find({}, {"password": 0}))
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    return render_template("employees.html",
                           employees=employees, managers=managers)


# Employee Search Query
@app.route("/employee_search", methods=["GET", "POST"])
def employee_search():
    query = request.form.get("employeequery")
    managers = list(mongo.db.employees.find({}, {"password": 0}))
    employees = list(mongo.db.employees.find({"$text": {"$search": query}}))
    return render_template("employees.html",
                           employees=employees, managers=managers)


# Delete Employee - Admin Only
@app.route("/delete_employee/<employee_id>")
def delete_employee(employee_id):
    mongo.db.employees.remove({"employee_id": employee_id})
    flash("Employee Successfully Deleted")
    return redirect(url_for("get_employees"))


# Edit Employee - Employee can edit own info or ADMIN can edit all
@app.route("/edit_employee/<employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    if request.method == "POST":
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
        # Gather Data from form to update DB
        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "phone": request.form.get("phone").lower(),
            "email": request.form.get("email").lower(),
            "employee_id": employee_id,
            "dob": request.form.get("dob"),
            "manager_id": request.form.get("manager_id"),
            "title": request.form.get("title").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "imgurl": imglocation
        }
        mongo.db.employees.update({"employee_id": employee_id}, register)
        flash("Employee Update Successful!")
        return redirect(url_for("get_employees"))
    employee = mongo.db.employees.find_one({"employee_id": employee_id})
    managers = list(mongo.db.employees.find({}, {"password": 0}))
    return render_template("edit_employee.html",
                           employee=employee,
                           managers=managers)


# Render Employee Profile
@app.route("/profile/<email>", methods=["GET", "POST"])
def profile(email):
    # grab the session user's first name from db
    first_name = mongo.db.employees.find_one(
        {"email": email})["first_name"]
    last_name = mongo.db.employees.find_one(
        {"email": email})["last_name"]
    employee_id = mongo.db.employees.find_one(
        {"email": email})["employee_id"]
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
    projects = list(mongo.db.projects.find())
    clients = list(mongo.db.clients.find())
    tasks = list(mongo.db.tasks.find({"employee_id": employee_id}))
    print(tasks)
    if session["employee"]:
        return render_template("profile.html",
                               first_name=first_name.capitalize(),
                               last_name=last_name.capitalize(),
                               employee_id=employee_id,
                               imgurl=imgurl, title=title,
                               phone=phone, email=email,
                               managername=managername,
                               manageremail=manageremail,
                               projects=projects,
                               clients=clients,
                               tasks=tasks)
    return redirect(url_for("login"))


# Tasks Directory
@app.route("/get_tasks")
def get_tasks():
    tasks = list(mongo.db.tasks.find())
    projects = list(mongo.db.projects.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    return render_template("tasks.html",
                           projects=projects,
                           tasks=tasks, employees=employees)


# Add Task Functionality
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # Insert Info into Mondo DB
    task_id = list(mongo.db.tasks.distinct("task_id"))
    task_id_int = list(map(int, task_id))
    task_id_int.sort()
    new_task_id = task_id_int[-1] + 1
    complete = "yes" if request.form.get("complete") else "no"
    taskregister = {
            "task_id": new_task_id,
            "task_name": request.form.get("task_name").lower(),
            "task_description":
            request.form.get("task_description").lower(),
            "project_no": request.form.get("project_no"),
            "due_date": request.form.get("duedate"),
            "employee_id": request.form.get("employee_id"),
            "progress": request.form.get("progress"),
            "complete": complete,
    }

    mongo.db.tasks.insert_one(taskregister)
    flash("Task added Successfully!")
    return redirect(url_for("get_tasks"))


# Edit Project Functionality and page rendering
@app.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    int_task_id = int(task_id)
    if request.method == "POST":
        # Insert Info into Mondo DB
        complete = "yes" if request.form.get("complete") else "no"
        taskregister = {
            "task_id": task_id,
            "task_name": request.form.get("task_name").lower(),
            "task_description":
            request.form.get("task_description").lower(),
            "project_no": request.form.get("project_no"),
            "due_date": request.form.get("duedate"),
            "employee_id": request.form.get("employee_id"),
            "progress": request.form.get("progress"),
            "complete": complete,
        }
        mongo.db.tasks.update(
                                 {"task_id": int_task_id},
                                 taskregister)
        flash("Task Update Successful!")
        return redirect(url_for("get_tasks"))
    projects = list(mongo.db.projects.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    task = mongo.db.tasks.find_one({"task_id": int_task_id})
    return render_template("edit_task.html",
                           projects=projects,
                           task=task, employees=employees)


# Tasks Search Query
@app.route("/task_search", methods=["GET", "POST"])
def task_search():
    query = request.form.get("taskquery")
    projects = list(mongo.db.projects.find())
    employees = list(mongo.db.employees.find({}, {"password": 0}))
    tasks = list(mongo.db.tasks.find({"$text": {"$search": query}}))
    return render_template("tasks.html",
                           projects=projects,
                           tasks=tasks, employees=employees)


# Delete tasks
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    int_task_id = task_id
    mongo.db.tasks.remove({"task_id": int_task_id})
    flash("Task Successfully Deleted")
    return redirect(url_for("get_tasks"))


# Logout Functionality
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("employee")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
