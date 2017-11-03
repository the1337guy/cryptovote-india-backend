from mongoengine import Document, connect, fields


class CVA(Document):
    pin_code = fields.IntField()
    voteOptions = fields.ListField()
    pass


def init():
    connect()
    pass


init()
