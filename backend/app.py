from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
import flask_cors
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

cors = flask_cors.CORS()
 
SECRET_KEY = os.urandom(24)
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
app.secret_key = "SECRET_KEY"
app.permanent_session_lifetime = timedelta(minutes=10)

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
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/api/signin',methods = ['GET','POST']) 
def user_login():

    if "user" in session:
        user_url = "/%s/project" % (session["user"])
        return redirect(user_url)

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

def get_data():
    if request.method == 'POST':
        source = requests.get('https://physionet.org/about/database/').text
        soup = BeautifulSoup(source, 'lxml')
        ul =soup.find('h2',{"id":"open"}).find_next_sibling('ul')
        lis = []
        data = []
        links = []
        counter = 0
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
            data.append(entry)
        for l in links:
            source = requests.get(l).text
            soup = BeautifulSoup(source, 'lxml')
            zipFile = soup.find("a",string = "Download the ZIP file")
            if(zipFile != None):
                data[counter].append('https://physionet.org/'+zipFile['href'])
            else:
                data[counter] = []
            counter = counter + 1
        dataList = [x for x in data if x != []]
            

        #print(links)
        return jsonify(dataList)

    return {'val':""}

if __name__ == '__main__':
 
    app.run()

