from pymongo import MongoClient
import urllib
import random
import ssl

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE'
client = MongoClient(host, tls=True, tlsAllowInvalidCertificates=True)
database = client['hackathon']
user_collection = database['users']
task_collection = database['tasks']
id_collection = database['used_ids']

def add_task(name, description, deadline, points):
    task_collection.insert_one({'name':name, 'description':description, 'points':int(points), 'deadline':deadline, 'unique_id':generate_task_id()})
    return 'New task added'

def remove_task(id):
    task_collection.delete_one({'_id':id})
    return 'Task removed'

def edit_task(id, name, description, deadline, points):
    query = {'_id':id}
    updated = {'$set':{'name':name, 'description':description, 'points':int(points), 'deadline':deadline}}  
    task_collection.update_one(query, updated)
    return 'Task updated'

def get_all_tasks():
    tasks = {}
    count = 0
    for task in task_collection.find():
        count+=1
        tasks[count] = task
    return tasks

def get_task(id):
    return task_collection.find_one({'_id':id})

def generate_task_id():
    while True:
        id = random.randint(1000, 99999)
        if not id_collection.find_one({'_id':id}):
            break
    id_collection.insert_one({'_id':id})
    return id

def get_users_without_this_task(id):
    users = []
    for user in user_collection.find():
        if int(id) not in user['tasks']:
            users.append(user['name'])
    return users

def get_users_with_this_task(id):
    users = []
    for user in user_collection.find():
        if int(id) in user['tasks']:
            users.append(user['name'])
    return users

def assign_user_tasks(id, email):
    user = user_collection.find_one({'_id':email})
    tasks = user['tasks']
    tasks.append(int(id))
    query = {'_id':email}
    update = {'$set':{'tasks':tasks}}
    user_collection.update_one(query, update)
    return 'Updated user tasks'

def get_user_tasks(email):
    user = user_collection.find_one({'_id': email})
    tasks = []
    for task_id in user['tasks']:    
        tasks.append(task_collection.find_one({'unique_id':int(task_id)}))
    return tasks