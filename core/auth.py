# auth.py
# By: Adam Kraft

from hashlib import sha256
from util import load_config

class Authenticator:
    ''' used for authentication with a key '''

    def __init__(self,key_name=None):
        self._key_name = key_name
        if key_name:
            json_dic = load_config()
            self._hashed_key = json_dic[key_name]

    def authenticate(self, key):
        ''' returns comparison of pre-hashed key and key given '''
        if not self._key_name:
            raise Exception("Failed to provide a key name")

        hashed = self.hash(key)

        return self._hashed_key == hashed

    def hash(self, instring):
        ''' returns a hashed version of instring '''
        return sha256(instring.encode('ascii')).hexdigest()

if __name__ == '__main__':
    from sys import argv
    auth = Authenticator()
    print(auth.hash(argv[1]))
