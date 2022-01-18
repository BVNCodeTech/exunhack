from logging import exception
from pymongo import MongoClient
import bcrypt
import urllib
import ssl

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE'
client = MongoClient(host, tls=True, tlsAllowInvalidCertificates=True)
database = client['hackathon']
user_collection = database['users']

def register(name, email, password):
    data = {
        '_id': email.lower(),
        'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
        'name': name,
        'role':'worker',
        'level':0,
        'points':0,
        'tasks':[]
    }
    if '@' in email:
        try:
            user_collection.insert_one(data)
            return True
        except:
            return False

def check_for_user(email, password):
    user = user_collection.find_one({'_id': email.lower()})
    if user:
        return bcrypt.checkpw(password.encode(), user['password'])
    else:
        return False


def check_admin(user):
    user = user_collection.find_one({'_id':user})
    if user['role'].lower() == 'admin':
        return True
    else:
        return False

def get_user_by_name(name):
    return user_collection.find_one({'name':name})

def get_user_by_id(email):
    return user_collection.find_one({'_id':email})

def get_all_users():
    users = []
    for user in user_collection.find():
        users.append(user)
    return users
