from pymongo import MongoClient
import urllib
from functions.tasks import generate_task_id

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
feedback_collection = database['feedback']

def add_feedback(text):
    feedback_collection.insert_one({'feedback':text, 'read':False, 'unique_id':generate_task_id()})
    return 'Feeback sent'

def mark_feedback_as_read(unique_id):
    feedback_collection.update_one({'unique_id':int(unique_id)}, {'$set':{'read':True}})
    return 'Feedback marked as read'

def delete_feedback(unique_id):
    feedback_collection.delete_one({'unique_id':int(unique_id)})
    return 'Feedback deleted'

def get_unread_feedback():
    unread_feedback = []
    for feed in feedback_collection.find():
        if not feed['read']:
            unread_feedback.append(feed)
    return unread_feedback

def get_read_feedback():
    read_feedback = []
    for feed in feedback_collection.find():
        if feed['read']:
            read_feedback.append(feed)
    return read_feedback 