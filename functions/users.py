from pymongo import MongoClient
import bcrypt
import urllib

host = 'mongodb+srv://admin:' + urllib.parse.quote("CT@exun2022") + '@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
user_collection = database['user_collection']

def register(email, password):
    data = {
        '_id': email.lower(),
        'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    }
    if '@' in email:
        user_collection.insert_one(data)

def check_for_user(email, password):
    user = user_collection.find_one({'_id': email.lower()})
    if user:
        return bcrypt.checkpw(password.encode(), user['password'])
    else:
        return False