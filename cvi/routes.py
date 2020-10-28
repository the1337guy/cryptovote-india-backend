# How this works
# 1. User makes a API request to authenticate using NID
# 2. API sends challenge and re-requests to verify with 2FA
# 3. User sends response to 2FA challenge
# 3b. API finds out if the User is eligible to vote by using the NID's address
# 4. API sends the User the new public key and private key, private key being immediately disposed # noqa
# 5. User selects whom to vote and signs the request with the aforementioned private key # noqa
# 6. API verifies it with the aforementioned public key
# 7. Record is saved in database.
from .auth import auth_handler, twofa_handler
# from .voting import vote_handler

routes = (
    ('post', '/api/auth', auth_handler),
    ('post', '/api/2faresp', twofa_handler),
    # ('post', '/api/vote', vote_handler),
)
