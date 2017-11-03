from marshmallow import Schema, fields
from .validation import ensure_valid, make_error, make_success
from .nid import DummyNID
from .models import TwoFARToken


class AHSchema(Schema):
    national_id = fields.String(required=True)
    pass


@ensure_valid(AHSchema)
def auth_handler(data):
    print(data)
    try:
        nid = DummyNID.get_nid(data.national_id)
    except DummyNID.DoesNotExist:
        return make_error('National ID doesn\'t exist')
    twofaexp = nid.auth_2fa()
    tok = TwoFARToken(complete=False, success=False, wanted=twofaexp)
    tok.save()
    print('Saved 2fa token with id: {}'.format(tok.id))
    return make_success(str(tok.id))


@ensure_valid(AHSchema)
def twofa_handler(data):
    pass
