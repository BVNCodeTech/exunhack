from pymongo import MongoClient
import urllib
import random
from functions.users import get_user_by_id, get_user_by_name

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
user_collection = database['users']
task_collection = database['tasks']
id_collection = database['used_ids']

def add_task(name, description, deadline, points):
    task_collection.insert_one({'name':name, 'description':description, 'points':int(points), 'deadline':deadline, 'unique_id':generate_task_id()})
    return 'New task added'

def remove_task(id):
    users = get_users_with_this_task(id)
    for user_name in users:
        user = get_user_by_name(user_name)
        tasks = user['tasks']
        tasks.remove(int(id))
        if not tasks:
            tasks = []
        user_collection.find_one_and_update({'_id':user['_id']}, {'$set':{'tasks':tasks}})
        task_collection.delete_one({'unique_id':int(id)})
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

def get_task_by_unique_id(unique_id):
    return task_collection.find_one({'unique_id':int(unique_id)})

def mark_task_as_complete(user, unique_id):
    user = get_user_by_id(user)
    tasks = user['tasks']
    tasks.remove(int(unique_id))
    user_points = user['points'] + get_task_by_unique_id(unique_id)['points']
    if not tasks:
        tasks = []
    user_collection.find_one_and_update({'_id':user['_id']}, {'$set':{'tasks':tasks, 'points':int(user_points)}})
    return 'Task marked as complete'
