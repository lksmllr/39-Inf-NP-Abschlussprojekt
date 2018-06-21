#!/usr/bin/env python3

import requests, json

r = requests.post("http://127.0.0.1:5000/heartbeat/"
    , data={'id': 'macbook1'})
print(r.status_code, r.reason)
