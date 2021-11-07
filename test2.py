from flask import Flask, Response, render_template, redirect, request, flash, session, url_for, jsonify
import flask_cors
from flask_cors import cross_origin, CORS
from flask_session import Session
from flask.helpers import url_for
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateField, DateTimeField, EmbeddedDocumentField, IntField, StringField
import mongoengine as db
from const import mymongo_password
from datetime import datetime, timedelta
import ssl
import os
from markupsafe import escape
from methods import encrypt, decrypt
from bs4 import BeautifulSoup
import requests
import uuid

cors = flask_cors.CORS(supports_credentials=True)

app = Flask(__name__, static_folder='./frontend/build',
            static_url_path='/')
SECRET_KEY = os.urandom(24)
app.secret_key = "SECRET_KEY"
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.permanent_session_lifetime = timedelta(minutes=10)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
CORS(app)

database_name = "gettingStarted"

db_url = "mongodb+srv://user_cloud:{}@cluster0.u0k5p.mongodb.net/{}?retryWrites=true&w=majority".format(
    '20153', database_name)
db.connect(host=db_url, ssl_cert_reqs=ssl.CERT_NONE)


class addAccess(EmbeddedDocument):
    acc_userid = StringField()
    acc_proid = IntField()


class users (db.Document):
    user_encryptid = db.StringField(required=True)
    user_encryptemail = db.StringField(required=True)
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


cors.init_app(app)


@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
@cross_origin(supports_credentials=True)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/api/signin', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def user_login():

    # if "user" in session:
    #     user_url = "/%s/project" % (session["user"])
    #     return redirect(user_url)

    error = None
    if request.method == 'POST':
        username = request.get_json().get('username', None)
        password = request.get_json().get('password', None)
        encry_name = encrypt(username)
        search = users.objects(user_encryptid=encry_name)
        if search:
            for result in search:
                if result.user_encryptpass == encrypt(password):
                    session["user"] = encry_name
                    session.permanent = True
                    # print(session)
                    # session.modifies = True
                    return {'auth': 'pass'}
                else:
                    error = "incorrect password"
        else:
            error = "invalid user name"
        return {'auth': error}
    return {'auth': "error"}


@app.route('/api/signup', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        name = request.get_json().get('username', None)
        email = request.get_json().get('email', None)
        invalidname = users.objects(user_encryptid=encrypt(name))
        invalidemail = users.objects(user_encryptemail=encrypt(email))
        if invalidname:
            error = "Error:Invalid username"
        elif invalidemail:
            error = "Error:Invalid email"
        else:
            password = request.get_json().get('password', None)
            new_user = users(user_encryptemail=encrypt(email), user_encryptid=encrypt(
                name), user_encryptpass=encrypt(password))
            try:
                new_user.save()
                #flash("New account has been created!", "info")
                return {'auth': "done"}
            except:
                return {'auth': "error"}

    return {'auth': error}


@app.route('/api/data', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_data():
    if request.method == 'POST':
        currentEntry = request.get_json().get('currentEntry', None)
        physionet = []
        links = []
        source = requests.get('https://physionet.org/about/database/').text
        soup = BeautifulSoup(source, 'lxml')
        ul = soup.find('h2', {"id": "open"}).find_next_sibling('ul')
        lis = []
        data = []
        counter = 0

        if physionet == []:
            print("GETTING VALUES")
            for li in ul.findAll('li'):
                entry = []
                lis.append(li)
                entry.append(li.find('a').text)
                links.append('https://physionet.org/' +
                             (li.find('a').get('href')))
                li.a.decompose()
                t = li.text.split()
                t.remove(t[0])
                desc = " ".join(t)  # gets description
                entry.append(desc)
                physionet.append(entry)

        while len(data) < 5 and currentEntry < len(physionet)-2:
            newEntry = []
            source = requests.get(links[currentEntry]).text
            print(currentEntry)
            soup = BeautifulSoup(source, 'lxml')
            zipFile = soup.find("a", string="Download the ZIP file")
            if(zipFile != None):
                newEntry = physionet[currentEntry]
                newEntry.append('https://physionet.org/'+zipFile['href'])
                data.append(newEntry)
                currentEntry = currentEntry + 1
            else:
                currentEntry = currentEntry + 1
        return jsonify(data)

    return {'val': ""}


@app.route('/api/authorized', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_authorized():
    print(session)
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return {'auth': 'rejected'}
    elif session["user"] != encrypt(request.get_json().get('username', None)):
        flash("Access denied: you're not allowed to proceed that website")
        return {'auth': 'rejected'}
    else:
        return {'auth': 'access'}


@app.route('/api/project/authorized', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_authorized_with_pro():
    print(session)
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return {'auth': 'rejected'}
    else:
        this_user = session["user"]
        userid = encrypt(request.get_json().get('username', None))
        if this_user != userid:
            access = False
            project_ID = int(request.get_json().get('projectid', None))
            check = users.objects(user_encryptid=this_user)
            for item in check:
                for check_acc in item.user_access:
                    if check_acc.acc_userid == userid and check_acc.acc_proid == project_ID:
                        access = True
                        return {'auth': 'access'}
            if not access:
                flash("Access denied: you're not allowed to proceed that website")
                return {'auth': 'rejected'}


@app.route('/api/logout', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def log_out():
    print(session)
    session.clear()
    print(session)
    return {'status': "success"}


def project_serializer(project):
    return{
        "user": project.user_id,
        "proname": project.project_name,
        "prodesc": project.description,
        "proid": project.project_id,
        "prodate": project.date_created
    }


@app.route('/api/project', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def project_table():
    error = None
    if request.method == 'POST':
        userid = encrypt(request.get_json().get('name', None))
        projects = dbModel.objects(user_id=userid).all()
        try:
            user_info = users.objects(user_encryptid=userid)
            for user in user_info:
                if user.user_access:
                    for acc in user.user_access:
                        proid = acc.acc_proid
                        projects_acc = dbModel.objects(project_id=proid).all()
                else:
                    projects_acc = []
        except:
            error = "Unknown error: fail to add user"

        return jsonify([*map(project_serializer, projects)]+[*map(project_serializer, projects_acc)])


@app.route('/api/project/add', methods=['POST', 'GET'])
def project_create():
    error = None
    if request.method == 'POST':
        userid = encrypt(request.get_json().get('userid', None))
        pname = request.get_json().get('name', None)
        pdescription = request.get_json().get('desc', None)
        pid = request.get_json().get('proid', None)
        unvalid = dbModel.objects(project_id=pid)
        if unvalid:
            error = "unvalid projectID"
            return{"error": error}
        else:
            new_pro = dbModel(user_id=userid, project_name=pname,
                              description=pdescription, project_id=pid)

            try:
                new_pro.save()
                return{"error": "None"}
            except:
                error = 'Unknown error in creating new project'
                return{"error": error}


@ app.route('/api/project/delete', methods=['POST', 'GET'])
def delete_project():
    if request.method == 'POST':
        userid = request.get_json().get('userid', None)
        id = request.get_json().get('proid', None)
        pro_delete = dbModel.objects(project_id=id).first()
        try:
            pro_delete.delete()
            return {"error": "None"}
        except:
            return {"error": 'error in deleting'}


def hardware_serializer(hw):
    return{
        "hwname": hw.hw_name,
        "capacity": hw.hw_capacity,
        "avail": hw.hw_availability
    }


def history_serializer(his):
    return{
        "id": his.history_id,
        "hwname": his.hwName,
        "amount": his.hwAmount,
        "remain": his.hwRemain,
        "date": his.checkoutDate
    }


@ app.route('/api/project/hardware', methods=["GET", "POST"])
def show_hardware():
    if request.method == 'POST':
        error = ''
        userid = encrypt(request.get_json().get('name', None))
        projectID = request.get_json().get('proid', None)
        project_ID = int(projectID)
        project_this = dbModel.objects(project_id=project_ID)
        for pro in project_this:
            histories = pro.checkout_history
        hw_informations = HW_info.objects().all()
        return {
            "info": [*map(hardware_serializer, hw_informations)],
            "history": [*map(history_serializer, histories)]
        }


@ app.route('/api/project/hardware/checkout', methods=["GET", "POST"])
def checkout_hardware():
    if request.method == 'POST':
        error = ''
        userid = encrypt(request.get_json().get('name', None))
        projectID = request.get_json().get('proid', None)
        project_ID = int(projectID)
        project_this = dbModel.objects(project_id=project_ID)
        checkout = 0
        inputnumber = request.get_json().get('checkout', None)
        checkout = int(inputnumber)
        if checkout > 0:
            name = request.get_json().get("hwname", None)
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
            error = "unvalid input"
        return{"error": error}


@ app.route('/api/project/hardware/checkin', methods=["GET", "POST"])
def checkin_hardware():
    if request.method == 'POST':
        error = ''
        userid = encrypt(request.get_json().get('name', None))
        project_ID = int(request.get_json().get('proid', None))
        project_this = dbModel.objects(project_id=project_ID)
        checkin = int(request.get_json().get("checkin", None))
        if checkin > 0:
            hwname = request.get_json().get("hwname", None)
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
                        history_id = request.get_json().get("historyid", None)
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
        else:
            error = "unvalid input"
        return {"error": error}


@ app.route('/api/project/hardware/adduser', methods=["GET", "POST"])
def project_adduser():
    if request.method == 'POST':
        error = ''
        userid = encrypt(request.get_json().get('name', None))
        project_ID = int(request.get_json().get('proid', None))
        project_this = dbModel.objects(project_id=project_ID)
        add_user = encrypt(request.get_json().get('usertoadd', None))
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
    return {'error': error}


if __name__ == "__main__":
    app.run(debug=True)
