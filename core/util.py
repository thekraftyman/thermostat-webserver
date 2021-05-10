# util.py
# By: thekraftyman

import json

'''
A set of functions used in various other core files/classes
'''

def load_config():
    ''' loads from the base "config.json" file and returns a dic '''
    with open('config.json', 'r') as infile:
        json_dic = json.load(infile)

    return json_dic

def load_state():
    ''' loads the state from the save-state.json file '''
    try:
        with open('save-state.json','r') as infile:
            json_dic = json.load(infile)
    except:
        json_dic = {
            "mode": None,
            "temp": None,
            "fan" : None
        }
    return json_dic

def save_state(out_dic):
    ''' saves a dictionary to the save-state.json file '''
    with open('save-state.json','w') as outfile:
        outfile.write(json.dumps(out_dic))