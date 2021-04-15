# auth.py
# By: Adam Kraft

from hashlib import sha256

class Authenticator:
    ''' used for authentication with a key '''

    def __init__(self,key_file):
        self._key_file = key_file
        with open(key_file,'r') as infile:
            self._hashed_key = infile.readline().strip()

    def authenticate(self, key):
        ''' returns comparison of pre-hashed key and key given '''
        hashed = sha256(key.encode('ascii')).hexdigest()

        return self._hashed_key == hashed
