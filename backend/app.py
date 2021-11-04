from flask import Flask, Response, render_template, redirect, request, flash, session, url_for, jsonify
import flask_cors
from flask_cors import cross_origin, CORS
from flask_session import Session
from flask.helpers import url_for
from flask_mongoengine import MongoEngine
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateField, DateTimeField, EmbeddedDocumentField, IntField, StringField
import mongoengine as db
from pymongo import MongoClient
from const import mymongo_password
from datetime import datetime, timedelta
import ssl
import os
from markupsafe import escape
from methods import encrypt
from bs4 import BeautifulSoup
import requests

cors = flask_cors.CORS(supports_credentials = True)
 
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
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

cors.init_app(app)

@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
@cross_origin(supports_credentials=True)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/api/signin',methods = ['GET','POST']) 
@cross_origin(supports_credentials=True)
def user_login():

    # if "user" in session:
    #     user_url = "/%s/project" % (session["user"])
    #     return redirect(user_url)

    error = None
    if request.method == 'POST':
        username = request.get_json().get('username',None)
        password = request.get_json().get('password',None)
        encry_name = encrypt(username)
        search = users.objects(user_encryptid=encry_name)
        if search:
            for result in search:
                if result.user_encryptpass == encrypt(password):
                    session["user"] = encry_name
                    session.permanent = True
                    print(session)
                    session.modifies = True
                    return {'auth':'pass'}
                else:
                    error = "incorrect password"
        else:
            error = "invalid user name"
        return {'auth': error}
    return {'auth': "error"}


@app.route('/api/signup',methods = ['GET','POST']) 

def sign_up():
    error = None
    if request.method == 'POST':
        name = request.get_json().get('username',None)
        email = request.get_json().get('email',None)
        invalidname = users.objects(user_encryptid=encrypt(name))
        invalidemail = users.objects(user_encryptemail=encrypt(email))
        if invalidname:
            error = "Error:Invalid username"
        elif invalidemail:
            error = "Error:Invalid email"
        else:
            password = request.get_json().get('password',None)
            new_user = users(user_encryptemail = encrypt(email),user_encryptid=encrypt(
                    name), user_encryptpass=encrypt(password))
            try:
                new_user.save()
                    #flash("New account has been created!", "info")
                return {'auth': "done"}
            except:
                return {'auth': "error"}
                

    return {'auth': error}


@app.route('/api/data',methods = ['GET','POST']) 
@cross_origin(supports_credentials=True)
def get_data():
    if request.method == 'POST':
        currentEntry = request.get_json().get('currentEntry',None)
        physionet = []
        links = []
        source = requests.get('https://physionet.org/about/database/').text
        soup = BeautifulSoup(source, 'lxml')
        ul =soup.find('h2',{"id":"open"}).find_next_sibling('ul')
        lis = []
        data = []
        counter = 0
        
            
        if physionet == []:
            print("GETTING VALUES")
            for li in ul.findAll('li'):
                entry = []
                lis.append(li)
                entry.append(li.find('a').text)
                links.append('https://physionet.org/'+(li.find('a').get('href')))
                li.a.decompose()
                t = li.text.split()
                t.remove(t[0])
                desc = " ".join(t) #gets description
                entry.append(desc)
                physionet.append(entry)
        
        while len(data) < 5 and currentEntry < len(physionet)-2:
            newEntry = []
            source = requests.get(links[currentEntry]).text
            print(currentEntry)
            soup = BeautifulSoup(source, 'lxml')
            zipFile = soup.find("a",string = "Download the ZIP file")
            if(zipFile != None):
                newEntry = physionet[currentEntry]
                newEntry.append('https://physionet.org/'+zipFile['href'])
                data.append(newEntry)
                currentEntry = currentEntry + 1
            else:
                currentEntry = currentEntry + 1


        # for l in links:
        #     source = requests.get(l).text
        #     soup = BeautifulSoup(source, 'lxml')
        #     zipFile = soup.find("a",string = "Download the ZIP file")
        #     if(zipFile != None):
        #         data[counter].append('https://physionet.org/'+zipFile['href'])
        #     else:
        #         data[counter] = []
        #     counter = counter + 1
        #     currentEntry = currentEntry + 1
        # dataList = [x for x in data if x != []]
            

        #print(links)
        print(data)
        return jsonify(data)

    return {'val':""}


@app.route('/api/authorized',methods = ['GET','POST']) 
@cross_origin(supports_credentials=True)
def get_authorized():
    print(session)
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return {'auth':'rejected'}
    elif session["user"] != encrypt(request.get_json().get('username',None)):
        flash("Access denied: you're not allowed to proceed that website")
        print("HERE2")
        return {'auth':'rejected'}
    else:
        return {'auth':'access'}


@app.route('/api/logout',methods = ['GET','POST'])
@cross_origin(supports_credentials=True)
def log_out():
    print(session)
    session.clear()
    print(session)
    return {'status':"success"}

if __name__ == '__main__':
 
    app.run()

