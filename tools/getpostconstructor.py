#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import requests
import json
import types

def createJson(data):
    return json.dumps(data)

def query(link, type, params={}, obj=None):
    if type=="GET":
        r = requests.get(link, params)
        return r.json()
    elif type=="POST":
        r = requests.post(link, data=obj, headers=params)
        return r.json()

def json2obj(data):
    return json.loads(data, object_hook=lambda d: types.SimpleNamespace(**d))