from pymongo import MongoClient
import urllib

host = 'mongodb+srv://pancham:pancham@exun.lqdp5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(host)
database = client['hackathon']
rewards_collection = database['rewards']
user_collection = database['users']

def get_all_rewards():
    rewards = []
    for reward in rewards_collection.find():
        rewards.append(reward)
    return rewards

def claim_reward(user, reward):
    user = user_collection.find_one({'_id':user})
    user_points = user['points']
    reward = rewards_collection.find_one({'redirect':reward})
    reward_points = reward['points']
    user_points -= reward_points
    if user_points < 0:
        return f"Insufficient points for {reward['name']}"
    user_collection.update_one({'_id':user},{'$set':{'points':user_points}})
    return f"Claimed {reward['name']}"