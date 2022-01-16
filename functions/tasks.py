import email
from pymongo import MongoClient
import urllib

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
user_collection = database['users']
task_collection = database['tasks']

def add_task(email, name, description, deadline, points):
    task_collection.insert_one({'email':email, 'name':name, 'description':description, 'points':int(points), 'deadline':deadline})
    return 'New task added'

def remove_task(id):
    task_collection.delete_one({'_id':id})
    return 'Task removed'

def edit_task(id, name, description, deadline, points):
    query = {'_id':id}
    updated = {'$set':{'name':name, 'description':description, 'points':int(points), 'deadline':deadline}}  
    task_collection.update_one(query, updated)
    return 'Task updated'

def get_all_tasks(email):
    tasks = {}
    count = 0
    try:
        for task in task_collection.find({"email":email}):
            count+=1
            tasks[count] = task
    except:
        return "you have no tasksskskskskks"
    return tasks

def get_task(id):
    return task_collection.find_one({'_id':id})