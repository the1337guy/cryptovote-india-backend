import requests
import json
import binascii

import nacl.signing
import nacl.encoding
import nacl.utils

from cvi.models import DummyNID

dummy = DummyNID.objects(name='John Doe')
if len(dummy) == 0:
    dummy = DummyNID()
    dummy.name = 'John Doe'
    dummy.save()
    print('Made a dummy NID:', dummy.id)
    pass
else:
    print('Amount of dummies in DB:', len(dummy))

# Step one
nid = input('Enter the NID: ')
resp = requests.post(
    'http://localhost:9001/api/auth', json={
        'obj': {
            'national_id': nid,
        }
    })
print('Response code: {}'.format(resp.status_code))
actresp = resp.json()
print('Result: {}'.format(actresp))
if resp.status_code != 200 or actresp['errored']:
    print('Got a non-200 response.')
    exit()

cresp = int(input('Enter challenge response: '))
sk = nacl.signing.SigningKey(seed=nacl.utils.random(32))

s1resp = requests.post(
    'http://localhost:9001/api/2faresp',
    json={
        'obj': {
            'tokid': actresp['token'],
            'cresp': cresp,
            'pubkey': sk.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
        }
    })
print('Response code: {}'.format(s1resp.status_code))
print('Result: {}'.format(s1resp.json()))

mbuf = json.dumps({
    'optid': 0
})
sig = sk.sign(mbuf.encode()).signature
s2resp = requests.post(
    'http://localhost:9001/api/vote',
    json={
        'obj': {
            'nid': nid,
            'message': mbuf,
            'signature': binascii.hexlify(sig).decode()
        }
    }
)
print('Response code: {}'.format(s2resp.status_code))
print('Result: {}'.format(s2resp.json()))

