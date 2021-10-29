from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask.helpers import url_for
from flask_mongoengine import MongoEngine
import mongoengine as db
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateField, DateTimeField, EmbeddedDocumentField, IntField, StringField
from const import mymongo_password
from datetime import datetime, timedelta
import ssl
import os
from markupsafe import escape
from methods import encrypt
import uuid

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


class addAccess(EmbeddedDocument):
    acc_userid = StringField()
    acc_proid = IntField()


class users (db.Document):
    user_encryptid = db.StringField(required=True)
    user_encryptpass = db.StringField(nullable=False)
    user_access = db.EmbeddedDocumentListField(addAccess)


class user_history(EmbeddedDocument):
    history_id = StringField()
    hwName = StringField()
    hwAmount = IntField()
    hwRemain = IntField()
    checkoutDate = DateTimeField(default=datetime.utcnow)


class dbModel (db.Document):
    user_id = db.StringField(reqired=True)
    project_name = db.StringField(required=True)
    description = db.StringField()
    project_id = db.IntField(nullable=False)
    date_created = db.DateTimeField(default=datetime.utcnow)
    checkout_history = db.EmbeddedDocumentListField(user_history)


class HW_info (db.Document):
    hw_name = db.StringField(required=True)
    hw_capacity = db.IntField()
    hw_availability = db.IntField()


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
                    flash("New account has been created!", "info")
                    return redirect('/login/')
                except:
                    return "Unkonwn error in creating new user account"

    return render_template('test_home.html', error=error)


@app.route('/login/', methods=('GET', 'POST'))
def user_login():

    if "user" in session:
        user_url = "/%s/project" % (session["user"])
        return redirect(user_url)

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
        flash("Access denied: you need to log in first:")
        return redirect('/login/')
    elif session["user"] != userid:
        flash("Access denied: you're not allowed to proceed that website")
        return redirect('/login/')

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
    try:
        user_info = users.objects(user_encryptid=userid)
        for user in user_info:
            if user.user_access:
                for acc in user.user_access:
                    proid = acc.acc_proid
                    projects_acc = dbModel.objects(project_id=proid).all()
            else:
                projects_acc = None
    except:
        error = "Unknown error: fail to add user"
    return render_template('test_project.html', projects=projects, projects_acc=projects_acc, error=error)


@ app.route('/<string:userid>/delete/<int:id>')
def delete_project(userid, id):
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return redirect('/login/')
    elif session["user"] != userid:
        flash("Access denied: you're not allowed to proceed that website")
        return redirect('/login/')

    pro_delete = dbModel.objects(project_id=id).first()
    project_url = '/%s/project' % (userid)
    try:
        pro_delete.delete()
        return redirect(project_url)
    except:
        return 'error in deleting'


@ app.route('/<string:userid>/project/<int:project_ID>', methods=("GET", "POST"))
def enter_project(userid, project_ID):
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return redirect('/login/')
    else:
        this_user = session["user"]
        if this_user != userid:
            access = False
            check = users.objects(user_encryptid=this_user)
            for item in check:
                for check_acc in item.user_access:
                    if check_acc.acc_userid == userid and check_acc.acc_proid == project_ID:
                        access = True
                        break
            if not access:
                flash("Access denied: you're not allowed to proceed that website")
                return redirect('/login/')

    error = None
    project_this = dbModel.objects(project_id=project_ID)
    if request.method == 'POST':
        try:
            add_user = encrypt(request.form["add-user"])
            user_target = users.objects(user_encryptid=add_user)
            if user_target:
                for user in user_target:
                    new_acc = addAccess(acc_userid=userid,
                                        acc_proid=project_ID)
                    user.user_access.append(new_acc)
                    user.save()
                    flash("user added")
            else:
                error = "invalid user name"
        except:
            error = error

        checkin = 0
        checkout = 0
        try:
            checkout = int(request.form["request"])
        except:
            error = "checked in"

        if checkout != 0:
            name = request.form["HW-requested"]
            HW_requested = HW_info.objects(hw_name=name)
            if HW_requested:
                for hw_requested in HW_requested:
                    availability = hw_requested.hw_availability
                    if availability >= checkout:
                        new_avail = availability-checkout

                    else:
                        new_avail = 0
                        checkout = availability
                        error = "Not enough resource! you have successfully checked in %d amount" % (
                            checkout)
                    hw_requested.hw_availability = new_avail
                    hw_requested.save()
                    new_history = user_history(
                        hwName=name, hwAmount=checkout, hwRemain=checkout, history_id=uuid.uuid4().hex)
                    for pro in project_this:
                        pro.checkout_history.append(new_history)
                        pro.save()
        else:
            try:
                checkin = int(request.form["checkin"])
            except:
                error = "checked out"
            if checkin != 0:
                hwname = request.form["checkin-name"]
                HW_check = HW_info.objects(hw_name=hwname)
                if HW_check:
                    for hw_check in HW_check:
                        availability = hw_check.hw_availability
                        after_avail = availability+checkin
                        if after_avail > hw_check.hw_capacity:
                            error = "wrong number!"
                        else:
                            hw_check.hw_availability = after_avail
                            hw_check.save()
                            history_id = request.form["history_id"]
                            for pro in project_this:
                                for history in pro.checkout_history:
                                    if history.history_id == history_id:
                                        remain = history.hwRemain
                                        if remain-checkin < 0:
                                            error = "wrong number!"
                                        else:
                                            history.hwRemain = remain-checkin
                                            pro.save()
                                        break

    for pro in project_this:
        histories = pro.checkout_history
    hw_informations = HW_info.objects().all()
    return render_template('hardwareInfo.html', project_ID=project_ID, hw_informations=hw_informations, histories=histories, error=error)


if __name__ == "__main__":
    app.run(debug=True)

