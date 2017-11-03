from mongoengine import Document, connect, fields
from .nid import DummyNID


class CVA(Document):
    pin_code = fields.IntField()
    voteOptions = fields.DictField()
    pass


class Vote(Document):
    ts = fields.DateTimeField()
    origin = fields.ReferenceField(DummyNID)
    message = fields.StringField()  # Both base64-encoded bytestrings
    signature = fields.StringField()
    pass


class TwoFARToken(Document):
    complete = fields.BooleanField()
    success = fields.BooleanField()
    wanted = fields.IntField()
    pass


def init():
    connect()
    pass


init()
