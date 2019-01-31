''' utils for json r/w '''

import json
import os

__all__ = [
    'write_to_json', 'read_from_json', 'save_as_json', 'load_json',
    'write_to_log_json'
]

def write_to_json(path, data):
    ''' write json to current dir, path="out path", data="json serializable data" '''
    parent_path = os.path.dirname(path)
    if not (os.path.exists(parent_path) and os.path.isdir(parent_path)):
        os.makedirs(parent_path)
    with open(path, 'w+') as outfile:
        json.dump(data, outfile)

save_as_json = write_to_json

def read_from_json(path):
    ''' return data from json, path="read path" '''
    with open(path, 'rb') as infile:
        return json.load(infile)

load_json = read_from_json


# write error data in json format to log
def write_to_log_json( path, data ):
    write_to_json( path, data )


if __name__ == '__main__':
    pass
