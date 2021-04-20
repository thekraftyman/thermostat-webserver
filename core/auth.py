# auth.py
# By: Adam Kraft

from hashlib import sha256
from core.util import load_config
from secrets import token_urlsafe as tokengen

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

    def generate_key(self):
        '''
        returns a randomly generated api key with format:
        xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        8-4-4-4-12 (length)
        '''
        return f'{tokengen(8)}-{tokengen(4)}-{tokengen(4)}-{tokengen(4)}-{tokengen(12)}'


if __name__ == '__main__':
    from sys import argv
    auth = Authenticator()
    print(auth.hash(argv[1]))
