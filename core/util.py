# util.py
# By: Adam Kraft

from json import dumps

'''
A set of functions used in various other core files/classes
'''

def load_config():
    ''' loads from the base "config.json" file and returns a dic '''
    with open('config.json', 'r') as infile:
        json_dic = json.load(infile)

    return json_dic
