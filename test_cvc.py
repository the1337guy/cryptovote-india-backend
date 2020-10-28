import requests
from addict import Dict

# Step one
nid = input('Enter the NID: ')
resp = requests.post(
    'http://localhost:8000/api/auth', json={
        'obj': {
            'national_id': nid,
        }
    })
print('Response code: {}'.format(resp.status_code))
print('Result: {}'.format(resp.json()))
s1r = Dict(resp.json())
cresp = int(input('Enter challenge response: '))
s1resp = requests.post(
    'http://localhost:8000/api/2faresp',
    json={
        'obj': {
            'tokid': s1r.obj,
            'cresp': cresp,
        }
    })
print('Response code: {}'.format(s1resp.status_code))
print('Result: {}'.format(s1resp.json()))
