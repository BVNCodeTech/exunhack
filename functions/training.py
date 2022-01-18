from pymongo import MongoClient
import urllib

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
training_collection = database['training']

def add_training(name, description, link, points):
    training_collection.insert_one({'name':name, 'description':description, 'link':link, 'points':points})
    return 'New task added'

def get_all_training():
    training = []
    count = 0
    for train in training_collection.find():
        training.append(train)
    return training