from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask.helpers import url_for
from flask_mongoengine import MongoEngine
import mongoengine as db
from const import mymongo_password
from datetime import datetime, timedelta
import ssl
import os
from markupsafe import escape
from methods import encrypt

SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.permanent_session_lifetime = timedelta(minutes=10)

database_name = "gettingStarted"
mongo_password = mymongo_password

database_name = "gettingStarted"
mongo_password = mymongo_password

db_url = "mongodb+srv://yx_wang:{}@cluster0.u0k5p.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongo_password, database_name)
db.connect(host=db_url, ssl_cert_reqs=ssl.CERT_NONE)


class users (db.Document):
    user_encryptid = db.StringField(required=True)
    user_encryptpass = db.StringField(nullable=False)


class dbModel (db.Document):
    user_id = db.StringField(reqired=True)
    project_name = db.StringField(required=True)
    description = db.StringField()
    project_id = db.IntField(nullable=False)
    date_created = db.DateField(default=datetime.now)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/signup/', methods=("GET", "POST"))
def sign_up():
    error = None
    if request.method == 'POST':
        name = request.form['newUsername']
        invalidname = users.objects(user_encryptid=encrypt(name))
        if invalidname:
            error = "Error:Invalid username"
        else:
            password = request.form['newPassword']
            passcheck = request.form['checkPassword']
            if password != passcheck:
                error = "Error:Inconsistent password"
            else:
                new_user = users(user_encryptid=encrypt(
                    name), user_encryptpass=encrypt(password))
                try:
                    new_user.save()
                    # error = "New account has been created!"
                    flash("New account has been created!", "info")
                    return redirect('/login/')
                except:
                    return "Unkonwn error in creating new user account"

    return render_template('test_home.html', error=error)


@app.route('/login/', methods=('GET', 'POST'))
def user_login():
    error = None
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        encry_name = encrypt(name)
        search = users.objects(user_encryptid=encry_name)
        if search:
            for result in search:
                if result.user_encryptpass == encrypt(password):
                    session["user"] = encry_name
                    session.permanent = True
                    unique_url = '/%s/project' % (encry_name)
                    return redirect(unique_url)
                else:
                    error = "incorrect password"
        else:
            error = "invalid user name"
        return render_template('test_home.html', error=error)
    return render_template('test_home.html')


@app.route('/logout/')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/<string:userid>/project', methods=('POST', 'GET'))
def project_table(userid):

    if "user" not in session:
        return redirect(url_for(user_login))

    error = None
    if request.method == 'POST':
        pname = request.form['ProjectName']
        pdescription = request.form['Description']
        pid = request.form['ProjectID']
        unvalid = dbModel.objects(project_id=pid)
        if unvalid:
            error = "unvalid projectID"
        else:
            new_pro = dbModel(user_id=userid, project_name=pname,
                              description=pdescription, project_id=pid)

            try:
                new_pro.save()
            except:
                error = 'Unknown error in creating new project'

    projects = dbModel.objects(user_id=userid).all()
    return render_template('test_project.html', projects=projects, error=error)


@app.route('/<string:userid>/delete/<int:id>')
def delete_project(userid, id):
    if "user" not in session:
        return redirect(url_for(user_login))

    pro_delete = dbModel.objects(project_id=id).first()
    project_url = '/%s/project' % (userid)
    try:
        pro_delete.delete()
        return redirect(project_url)
    except:
        return 'error in deleting'


@app.route('/<string:userid>/project/<int:project_ID>')
def enter_project(userid, project_ID):
    if "user" not in session:
        return redirect(url_for(user_login))

    return render_template('hardwareInfo.html', project_ID=project_ID)


if __name__ == "__main__":
    app.run(debug=True)


# def main():
    # name = 'name1'
    # password = '111'
    # new_user = users(user_encryptid=encrypt(
    #     name), user_encryptpass=encrypt(password))
    # new_user.save()
    # name = 'name1'
    # password = '111'
    # research = users.objects(user_encryptid=encrypt(name))
    # if research:
    #     print("yes")
    # for result in research:
    #     if result.user_encryptpass == encrypt(password):
    #         print("got")

# main();
