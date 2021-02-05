import requests 
import json

def createJson(data):
    return json.dumps(data)

def query(link, type, params={}, obj=None):
    if type=="GET":
        r = requests.get(link, params) 
        return r.json()
    elif type=="POST":
        r = requests.post(link, data=obj, headers=params)
        return r.json()