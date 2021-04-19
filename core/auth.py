# auth.py
# By: Adam Kraft

from hashlib import sha256
from util import load_config

class Authenticator:
    ''' used for authentication with a key '''

    def __init__(self,key_name):
        self._key_name = key_name
        json_dic = load_config()
        self._hashed_key = json_dic[key_name]

    def authenticate(self, key):
        ''' returns comparison of pre-hashed key and key given '''
        hashed = sha256(key.encode('ascii')).hexdigest()

        return self._hashed_key == hashed
