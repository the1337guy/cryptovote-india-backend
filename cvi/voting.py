from marshmallow import Schema, fields
from .validation import ensure_valid, make_error, make_success
from .models import DummyNID, Vote
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
import binascii
import json
import datetime


class VHSchema(Schema):
    nid = fields.String(required=True)
    message = fields.String(required=True)
    signature = fields.String(required=True)
    pass


@ensure_valid(VHSchema)
def vote_handler(data):
    user = None
    try:
        user = DummyNID.objects.get(id=data.nid)
    except DummyNID.DoesNotExist:
        return make_error('NOTOKEN', 'No token found')

    if user.redeemed:
        return make_error('ALREADYREDEEMED', 'Already redeemed')
    vk = VerifyKey(user.pub, encoder=HexEncoder)
    user.redeemed = True
    user.save()

    try:
        valid = vk.verify(data.message.encode(),
                          binascii.unhexlify(data.signature))
    except binascii.Error:
        return make_error('BADENCODING', 'Invalid encoding.')
    except BadSignatureError:
        return make_error('INVALIDSIG', 'Invalid signature.')
    try:
        j = json.loads(valid)
    except json.JSONDecodeError:
        return make_error('BADENCODING', 'Invalid encoding.')

    if 'optid' not in j or not isinstance(j['optid'], int):
        return make_error('INVALIDSCHEMA', 'Option not found')
    v = Vote()
    v.ts = datetime.datetime.now()
    v.origin = user
    v.message = valid.decode()
    v.signature = data.signature
    v.save()
    return make_success({
        'success': True
    })
