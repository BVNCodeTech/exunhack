from pymongo import MongoClient
import urllib

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
user_collection = database['users']
rewards_collection = database['rewards']


