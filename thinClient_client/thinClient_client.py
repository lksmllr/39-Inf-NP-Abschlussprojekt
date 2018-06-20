#!/usr/bin/env python3

import requests

r = requests.post("http://localhost:5000/heartbeat"
    , data={'id': 'macbook'})
print(r.status_code, r.reason)
