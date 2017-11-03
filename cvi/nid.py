from mongoengine import Document, fields


# Dummy NID
class DummyNID(Document):
    pub = fields.StringField()  # base64-encoded 32-byte public key
    redeemed = fields.BoolField()

    @staticmethod
    def is_valid_id(id):
        return True

    def auth_2fa(self):
        # This returns the expected 2FA response
        return 0

    def get_address(self):
        # This returns the PIN code for the address
        return 0

    def setpub(self, pub):
        self.pub = pub
        self.redeemed = True
        pass

    @classmethod
    def get_nid(cls, id):
        # return cls.objects.get(id=id)
        return cls()

    pass
