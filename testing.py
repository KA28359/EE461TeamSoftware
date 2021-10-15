#please note all code below is not yet guaranteed to work
#so far its just me gathering my thoughts ~CW

#database functions
import pymongo
client = pymongo.MongoClient("something")
db = client["database"]
#assume doc format for collection users is the following 
#{userid, username, password,email, projectAccess}
userCol = db["users"]
#assume doc format for collection projects is the following 
#{projectid, name, description, accessr, accessw}
projectCol = db["projects"]
 
def create_account(name, password, email):
    #note: upon creation only user id passed is the creator's
    doc = { "username": name, 
            "password": password,
            "email": email,
            "projectAccess": []}
    userCol.insert_one(doc)

def check_login(username, password): 
    #assume args already decrypted
    
    query = userCol.find({"$and":[{"username":{username}},
                                  {"password":{password}}]})

    user = userCol.find(query)
    for u in user:
        #should only be one
        #call function to login
        #maybe return userid as that will be used a lot
        return

    #if you get here call function to send error message to user


def check_project_access(userid, projectid):
    query = { "userid": userid }
    user = userCol.find(query)
    projects = []
    for u in user:
        projects = u["projectAccess"]
    
    if projectid in projects:
        #check access level
        return 

    return 

def create_new_project(name, id, description, userid):
    #note: upon creation only user id passed is the creator's
    doc = { "projectid": id, 
            "name": name,
            "description": description,
            "userids": [userid]}
    projectCol.insert_one(doc)

def add_project_user(projectid,email, access):

def check_out_set():

def return_set():
    
    

        
    