from marshmallow import Schema, fields
from .validation import ensure_valid, make_error, make_success
from .models import TwoFARToken, Vote
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
import binascii
import json
import time


class VHSchema(Schema):
    tokid = fields.String(required=True)
    message = fields.String(required=True)
    signature = fields.String(required=True)
    pass


@ensure_valid(VHSchema)
def vote_handler(data):
    try:
        tok = TwoFARToken.objects.get(id=data.tokid)
    except TwoFARToken.DoesNotExist:
        return make_error('No such token m8')
    o = tok.origin
    vk = VerifyKey(o.pub, encoder=HexEncoder)
    try:
        valid = vk.verify(data.message.encode(),
                          binascii.unhexlify(data.signature))
    except binascii.Error:
        return make_error('Bad encoding m8')
    except BadSignatureError:
        return make_error('No fraud m8')
    try:
        j = json.loads(valid)
    except json.JSONDecodeError:
        return make_error('Invalid encoding m8')
    if 'optid' not in j or not isinstance(j['optid'], int):
        return make_error('Option not found')
    v = Vote()
    v.ts = time.time()
    v.origin = o
    v.message = valid
    v.signature = data.signature
    v.save()
    return make_success('Nice, vote registered')
