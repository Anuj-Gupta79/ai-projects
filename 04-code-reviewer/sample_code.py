import requests
import json

# A simple user management system
users = []


def get_user(id):
    for i in range(len(users)):
        if users[i]["id"] == id:
            return users[i]


def add_user(name, email, age):
    user = {}
    user["id"] = len(users) + 1
    user["name"] = name
    user["email"] = email
    user["age"] = age
    users.append(user)
    return user


def delete_user(id):
    for i in range(len(users)):
        if users[i]["id"] == id:
            users.pop(i)
            return True


def get_all_users():
    return users


def fetch_user_from_api(user_id):
    response = requests.get("http://api.example.com/users/" + str(user_id))
    data = json.loads(response.text)
    return data


def calculate_average_age():
    total = 0
    for i in range(len(users)):
        total = total + users[i]["age"]
    average = total / len(users)
    return average


def search_users(keyword):
    results = []
    for i in range(len(users)):
        if keyword in users[i]["name"]:
            results.append(users[i])
    return results


def update_user(id, name, email):
    for i in range(len(users)):
        if users[i]["id"] == id:
            users[i]["name"] = name
            users[i]["email"] = email
            return True
