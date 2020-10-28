from marshmallow import Schema, fields
from .validation import ensure_valid, make_error, make_success
from .models import DummyNID, TwoFARToken
import nacl.encoding
import nacl.signing


class AHSchema(Schema):
    national_id = fields.String(required=True)
    pass


# This generates a 2FA challenge, that must be answered with 2FA handler (see below)
@ensure_valid(AHSchema)
def auth_handler(data):
    print(data)
    try:
        nid = DummyNID.get_nid(data.national_id)
    except DummyNID.DoesNotExist:
        return make_error('INVALIDNID', 'National ID doesn\'t exist')
    twofaexp = nid.auth_2fa()
    tok = TwoFARToken(complete=False, success=False, wanted=twofaexp)
    tok.origin = nid
    tok.save()
    print('Saved 2fa token with id: {}'.format(tok.id))
    return make_success(str(tok.id))


class THSchema(Schema):
    tokid = fields.String(required=True)
    cresp = fields.Int(required=True)
    pass


# On validation of 2FA this generates the initial keypair. This is temporary so far.
@ensure_valid(THSchema)
def twofa_handler(data):
    tok = TwoFARToken.objects.get(id=data.tokid)
    if tok.wanted != data.cresp:
        return make_error('Fail! Try again.')
    else:
        tok.complete = True
        tok.success = True
        tok.save()

        nationalid = tok.origin
        lvd = nationalid.lvd

        sk = nacl.signing.SigningKey.generate()
        nationalid.pub = sk.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()  # noqa
        nationalid.save()

        return make_success({
            'options': lvd.voteOptions,
            'keypair': {
                'pub': sk.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode(),
                'priv': sk.encode(encoder=nacl.encoding.HexEncoder).decode(),
            }
        })
    pass
