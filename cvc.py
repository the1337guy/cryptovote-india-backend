import requests

# Step one
nid = input('Enter NID retard: ')
resp = requests.post(
    'http://localhost:8000/api/auth', json={
        'obj': {
            'national_id': nid,
        }
    })
print('Response code: {}'.format(resp.status_code))
print('Result: {}'.format(resp.json()))
