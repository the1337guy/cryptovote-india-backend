from mongoengine import Document, connect, fields


class CVA(Document):
    pin_code = fields.IntField()
    voteOptions = fields.DictField()
    pass


# Dummy NID
class DummyNID(Document):
    cva = fields.ReferenceField(CVA)
    pub = fields.StringField()  # hex-encoded 32-byte public key
    redeemed = fields.BooleanField()

    @staticmethod
    def is_valid_id(id):
        return True

    def auth_2fa(self):
        # This returns the expected 2FA response
        return 0

    def get_address(self):
        # This returns the PIN code for the address
        return 0

    @classmethod
    def get_nid(cls, id):
        return cls.objects.get(id=id)
        # return cls()

    pass


class Vote(Document):
    ts = fields.DateTimeField()
    origin = fields.ReferenceField(DummyNID)
    message = fields.StringField()  # Both base64-encoded bytestrings
    signature = fields.StringField()
    pass


class TwoFARToken(Document):
    origin = fields.ReferenceField(DummyNID)
    complete = fields.BooleanField()
    success = fields.BooleanField()
    wanted = fields.IntField()
    pass


def init():
    connect(db='CVI')
    pass


init()
