from logging import exception
from pymongo import MongoClient
import bcrypt
import urllib

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
user_collection = database['users']

def register(name, email, password):
    data = {
        '_id': email.lower(),
        'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
        'name': name
    }
    if '@' in email:
        try:
            user_collection.insert_one(data)
            return 'Registration Successful!'
        except:
            return 'an error occured'

def check_for_user(email, password):
    user = user_collection.find_one({'_id': email.lower()})
    if user:
        return bcrypt.checkpw(password.encode(), user['password'])
    else:
        return False