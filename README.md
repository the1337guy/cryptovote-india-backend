### Cryptovoting proof of concept.

#### Theory (?)
This is a proof of concept very simplified cryptovoting software that I wrote a few years ago. Recently polished, and works, somewhat.

The procedure generally is:
1. (ONLY FOR TESTING) The user first asks to update the public key (this shouldn't even be required with a real NID).
2. (ONLY FOR TESTING) The server challenges it with a 2FA, if succeeded, the database public key is updated.
3. User requests to make a vote on the server, with a message signed with the aforementioned public key.
4. Server verifies it with the key, if succeeded, puts it in the database and sets the redeemed field to true.
***
#### Structure of the code
1. cvi/auth.py contains the code for authentication and 2FA code to update the public key. (**TODO(?): Add SMS support with Textlocal**)
2. cvi/models.py contains the database models that are relevant
3. cvi/routes.py contains a description of the routes that are exposed via the API.
4. cvi/validation.py contains utilities for validating requests (if only validating requests was easier)
5. cvi/voting.py contains the API route for actual voting, as described in steps 3 & 4.